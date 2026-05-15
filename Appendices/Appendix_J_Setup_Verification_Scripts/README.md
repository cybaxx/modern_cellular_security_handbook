# Appendix J: Setup Verification Scripts

## Introduction

The handbook describes what to configure. This appendix provides tooling to verify that the configuration is actually in place. Security configurations drift — system updates change defaults, apps request new permissions, and manual configuration steps get missed. These scripts give you a repeatable, auditable way to check your setup rather than relying on memory.

Three tools are provided:

1. **`verify_grapheneos.sh`** — Audits a GrapheneOS device (Phone B) for correct privacy configuration via ADB
2. **`threat_model.sh`** — Interactive CLI questionnaire that identifies your threat tier and outputs a personalized recommendation
3. **`opsec_checklist.sh`** — Generates a per-operation checklist (border crossing, protest, legal matter, standard day) based on threat level input

All scripts require a Unix-like system (Linux, macOS). The device audit script additionally requires Android Debug Bridge (ADB) and a connected device with USB debugging enabled.

---

## Script 1: GrapheneOS Privacy Audit (`verify_grapheneos.sh`)

This script connects to a GrapheneOS device via ADB and checks 18 privacy-relevant settings. Each check outputs PASS, FAIL, or WARN with a brief explanation. A final score summarizes the result.

**Prerequisites:**
- ADB installed (`brew install android-platform-tools` on macOS; `apt install adb` on Debian/Ubuntu)
- USB debugging enabled on the target device (Settings > Developer options > USB debugging)
- Device connected via USB and ADB authorized

```bash
#!/usr/bin/env bash
# verify_grapheneos.sh
# GrapheneOS privacy configuration audit
# Version 1.0 — 2026-05-14
# Usage: bash verify_grapheneos.sh
# Requires: adb, connected GrapheneOS device with USB debugging enabled

set -euo pipefail

PASS=0
FAIL=0
WARN=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}[PASS]${NC} $1"; ((PASS++)); }
fail() { echo -e "${RED}[FAIL]${NC} $1"; ((FAIL++)); }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; ((WARN++)); }
header() { echo -e "\n=== $1 ==="; }

check_adb() {
    if ! command -v adb &>/dev/null; then
        echo "ERROR: adb not found. Install with: brew install android-platform-tools"
        exit 1
    fi
    if ! adb devices | grep -q "device$"; then
        echo "ERROR: No device connected or USB debugging not authorized."
        echo "Enable: Settings > Developer options > USB debugging"
        exit 1
    fi
}

adb_setting() {
    adb shell settings get "$1" "$2" 2>/dev/null | tr -d '[:space:]'
}

adb_prop() {
    adb shell getprop "$1" 2>/dev/null | tr -d '[:space:]'
}

echo "=================================================="
echo " GrapheneOS Privacy Configuration Audit"
echo " $(date)"
echo "=================================================="

check_adb

# ── Device Info ─────────────────────────────────────────────────────────────
header "Device Information"
MODEL=$(adb_prop ro.product.model)
BUILD=$(adb_prop ro.build.display.id)
ANDROID=$(adb_prop ro.build.version.release)
echo "  Model:        $MODEL"
echo "  Build:        $BUILD"
echo "  Android:      $ANDROID"

if echo "$BUILD" | grep -qi "grapheneos"; then
    pass "GrapheneOS confirmed"
else
    warn "Build string does not confirm GrapheneOS — verify manually"
fi

# ── Network Settings ─────────────────────────────────────────────────────────
header "Network Privacy"

# Wi-Fi scanning always-on
SCANNING=$(adb_setting global wifi_scan_always_enabled)
if [ "$SCANNING" = "0" ] || [ "$SCANNING" = "null" ]; then
    pass "Wi-Fi always-on scanning: DISABLED"
else
    fail "Wi-Fi always-on scanning: ENABLED — disable in Settings > Location > Wi-Fi scanning"
fi

# Bluetooth scanning
BT_SCAN=$(adb_setting global ble_scan_always_enabled)
if [ "$BT_SCAN" = "0" ] || [ "$BT_SCAN" = "null" ]; then
    pass "Bluetooth background scanning: DISABLED"
else
    fail "Bluetooth background scanning: ENABLED — disable in Settings > Location > Bluetooth scanning"
fi

# Captive portal detection (pings Google by default — privacy leak)
CAPTIVE=$(adb_setting global captive_portal_detection_enabled)
if [ "$CAPTIVE" = "0" ]; then
    pass "Captive portal detection: DISABLED (no Google ping on network join)"
else
    warn "Captive portal detection: ENABLED — may ping Google servers on Wi-Fi join"
    echo "       Disable: Settings > Network & internet > Internet connectivity checks"
fi

# Private DNS (DNS-over-TLS)
PRIVATE_DNS=$(adb_setting global private_dns_mode)
PRIVATE_DNS_HOST=$(adb_setting global private_dns_specifier)
if [ "$PRIVATE_DNS" = "hostname" ] && [ -n "$PRIVATE_DNS_HOST" ]; then
    pass "Private DNS (DoT): ENABLED — provider: $PRIVATE_DNS_HOST"
elif [ "$PRIVATE_DNS" = "opportunistic" ]; then
    warn "Private DNS: OPPORTUNISTIC (upgrades when available, not enforced)"
else
    fail "Private DNS: DISABLED — all DNS queries visible to network operator"
    echo "       Enable: Settings > Network & internet > Private DNS"
fi

# ── Location Settings ────────────────────────────────────────────────────────
header "Location Privacy"

LOCATION=$(adb_setting secure location_mode)
if [ "$LOCATION" = "0" ] || [ "$LOCATION" = "null" ]; then
    pass "System location: DISABLED"
else
    warn "System location: ENABLED (mode $LOCATION) — verify only essential apps have access"
fi

# ── Bluetooth & NFC ──────────────────────────────────────────────────────────
header "Short-Range Radio"

BT_STATE=$(adb shell settings get global bluetooth_on 2>/dev/null | tr -d '[:space:]')
if [ "$BT_STATE" = "0" ]; then
    pass "Bluetooth: OFF"
else
    warn "Bluetooth: ON — ensure this is intentional; disable when not in use"
fi

NFC_STATE=$(adb shell settings get secure nfc_on 2>/dev/null | tr -d '[:space:]')
if [ "$NFC_STATE" = "0" ] || [ "$NFC_STATE" = "null" ]; then
    pass "NFC: DISABLED"
else
    warn "NFC: ENABLED — NFC can be used for proximity tracking; disable if not needed"
fi

# ── Developer Options ────────────────────────────────────────────────────────
header "Developer Options"

ADB_ENABLED=$(adb_setting global adb_enabled)
if [ "$ADB_ENABLED" = "0" ] || [ "$ADB_ENABLED" = "null" ]; then
    warn "ADB: currently DISABLED (expected; this audit ran anyway — check connection method)"
else
    warn "ADB: ENABLED — disable after completing this audit (Settings > Developer options > USB debugging)"
fi

# ── Auto Updates ─────────────────────────────────────────────────────────────
header "Update Status"

AUTO_UPDATE=$(adb_setting global auto_update_enabled 2>/dev/null || echo "null")
if [ "$AUTO_UPDATE" = "1" ] || [ "$AUTO_UPDATE" = "null" ]; then
    pass "Auto-updates: appears ENABLED or managed by GrapheneOS updater"
else
    fail "Auto-updates: may be DISABLED — keeping GrapheneOS updated is critical for security"
fi

# ── Sensitive Permissions Audit ──────────────────────────────────────────────
header "Sensitive App Permissions"

echo "  Checking apps with LOCATION (fine/coarse/background) permission..."
LOCATION_APPS=$(adb shell pm list packages -g 2>/dev/null \
    | grep -i "android.permission.ACCESS_FINE_LOCATION\|android.permission.ACCESS_COARSE_LOCATION" \
    | sed 's/package://g' | sed 's/ .*//g' | sort -u 2>/dev/null || echo "")

if [ -z "$LOCATION_APPS" ]; then
    pass "No apps found with declared location permission (or listing unavailable)"
else
    warn "Apps with location permission declared:"
    echo "$LOCATION_APPS" | while read -r pkg; do
        echo "       • $pkg"
    done
    echo "       Review each in Settings > Privacy > Permission manager > Location"
fi

echo ""
echo "  Checking for known high-risk packages..."
HIGH_RISK_PACKAGES=(
    "com.google.android.gms"
    "com.google.android.gsf"
    "com.facebook.katana"
    "com.instagram.android"
    "com.tiktok.android"
    "com.whatsapp"
    "com.snapchat.android"
)

FOUND_RISK=0
for pkg in "${HIGH_RISK_PACKAGES[@]}"; do
    if adb shell pm list packages 2>/dev/null | grep -q "$pkg"; then
        fail "HIGH-RISK PACKAGE INSTALLED: $pkg"
        FOUND_RISK=1
    fi
done
if [ "$FOUND_RISK" = "0" ]; then
    pass "No known high-risk packages detected"
fi

# ── Screen Lock ──────────────────────────────────────────────────────────────
header "Device Lock"

# Note: locksettings get-quality is unreliable on Android 12+ and GrapheneOS;
# it may return "unexpected null" or fail without root. We use a best-effort
# check and fall back to a manual reminder.
LOCK_TYPE=$(adb shell locksettings get-quality 2>/dev/null | tr -d '[:space:]' || echo "unknown")

if echo "$LOCK_TYPE" | grep -qE "^[0-9]+$"; then
    # Quality values: 0=none, 32768=pin, 65536=alpha password, 196608=biometric+pin
    if echo "$LOCK_TYPE" | grep -qE "^(32768|65536|196608|327680)"; then
        pass "Screen lock: CONFIGURED (quality code $LOCK_TYPE)"
    elif [ "$LOCK_TYPE" = "0" ]; then
        fail "Screen lock: NONE — set a PIN or passphrase immediately"
    else
        warn "Screen lock quality code: $LOCK_TYPE — verify manually in Settings > Security"
    fi
else
    # locksettings not available without elevated access on this device/version
    warn "Screen lock: Cannot read via ADB on this Android version — verify manually"
    echo "       Check: Settings > Security > Screen lock (should be PIN or password, NOT biometric only)"
    echo "       Reason: Biometric unlock can be physically compelled; PIN cannot"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "=================================================="
echo " AUDIT SUMMARY"
echo "=================================================="
echo -e " ${GREEN}PASS: $PASS${NC}  |  ${YELLOW}WARN: $WARN${NC}  |  ${RED}FAIL: $FAIL${NC}"
echo ""

TOTAL=$((PASS + WARN + FAIL))
SCORE=$(( (PASS * 100) / TOTAL ))

echo " Score: $SCORE% ($PASS of $TOTAL checks passed)"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo -e " ${RED}Action required: $FAIL failing check(s). Review FAIL items above.${NC}"
elif [ "$WARN" -gt 0 ]; then
    echo -e " ${YELLOW}Review recommended: $WARN warning(s). Some settings may need attention.${NC}"
else
    echo -e " ${GREEN}Configuration looks good. Run this audit monthly.${NC}"
fi
echo ""
echo " Note: This script audits configuration settings only."
echo " It cannot detect compromised firmware, zero-day exploits,"
echo " or network-level surveillance. A passing score means your"
echo " settings are correct — not that your device is uncompromised."
echo "=================================================="
```

---

## Script 2: Threat Model Questionnaire (`threat_model.sh`)

This interactive script asks eight questions and outputs a specific threat tier with tailored recommendations. It takes under three minutes to complete.

```bash
#!/usr/bin/env bash
# threat_model.sh
# Interactive threat tier assessment
# Version 1.0 — 2026-05-14
# Usage: bash threat_model.sh

set -euo pipefail

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

ask() {
    local question="$1"
    local var_name="$2"
    echo -e "\n${CYAN}${question}${NC}"
    echo -n "  [y/n]: "
    read -r response
    eval "$var_name=$(echo "$response" | tr '[:upper:]' '[:lower:]')"
}

yn_yes() { [[ "$1" == "y" || "$1" == "yes" ]]; }

echo ""
echo -e "${BOLD}=================================================="
echo " Threat Tier Assessment"
echo " Privacy Researcher's Handbook — Chapter 47"
echo -e "==================================================${NC}"
echo ""
echo " Answer yes/no to each question. Be honest."
echo " This assessment is only as useful as your answers."
echo ""

ask "Q1. Are you currently under investigation by a federal agency, or have you received a federal subpoena or National Security Letter?" Q1
ask "Q2. Do you handle information that could be subject to a national security classification or foreign intelligence interest?" Q2
ask "Q3. Are you a journalist who regularly covers government corruption, law enforcement, or national security topics?" Q3
ask "Q4. Are you an activist, organizer, or dissident in a jurisdiction where your activities could result in criminal charges?" Q4
ask "Q5. Are you a domestic violence survivor or do you have reason to believe a specific individual has installed monitoring software on your device?" Q5
ask "Q6. Do you regularly cross international borders with sensitive data or in circumstances where your device may be inspected?" Q6
ask "Q7. Does your employer have a Mobile Device Management (MDM) profile installed on your primary personal phone?" Q7
ask "Q8. Are you involved in civil litigation or a contentious legal dispute where your communications could be subject to discovery?" Q8

echo ""
echo -e "${BOLD}=================================================="
echo " ASSESSMENT RESULTS"
echo -e "==================================================${NC}"
echo ""

TIER=0
REASONS=()

if yn_yes "$Q1" || yn_yes "$Q2"; then
    TIER=3
    REASONS+=("Federal investigation or national security interest")
fi

if yn_yes "$Q3" || yn_yes "$Q4" || yn_yes "$Q6"; then
    [ "$TIER" -lt 2 ] && TIER=2
    REASONS+=("Journalism, activism, or border risk identified")
fi

if yn_yes "$Q5"; then
    [ "$TIER" -lt 1 ] && TIER=1
    REASONS+=("Potential stalkerware or intimate partner surveillance")
fi

if yn_yes "$Q7" || yn_yes "$Q8"; then
    [ "$TIER" -lt 1 ] && TIER=1
    REASONS+=("Employer MDM or civil litigation exposure")
fi

case $TIER in
0)
    echo -e " ${GREEN}TIER 0: Passive Commercial Surveillance${NC}"
    echo ""
    echo " Your primary adversary is the advertising and data broker ecosystem."
    echo " You do not need two phones, Faraday bags, or burner SIMs."
    echo ""
    echo " Recommended actions (Citizen Max Stack):"
    echo "   1. Install Signal and replace WhatsApp/SMS for sensitive conversations"
    echo "      (Signal retains only phone number + last connection date — proven by"
    echo "       2016 Eastern District of Virginia grand jury subpoena; signal.org/bigbrother/)"
    echo "   2. Install uBlock Origin or switch to Brave browser"
    echo "   3. Revoke location permissions from all non-essential apps"
    echo "   4. Use a VPN (Mullvad or ProtonVPN) — \$5–10/month"
    echo "   5. Enable encrypted DNS (Cloudflare 1.1.1.1 or Quad9)"
    echo "   6. Use GrapheneOS or iOS Lockdown Mode if you want maximum protection"
    echo ""
    echo " Reference: Chapter 28 (The Citizen's Guide), Appendix I (Minimum Viable Privacy)"
    ;;
1)
    echo -e " ${YELLOW}TIER 1: Targeted Personal Surveillance${NC}"
    echo ""
    echo " Identified risks:"
    for r in "${REASONS[@]}"; do echo "   • $r"; done
    echo ""
    echo " Recommended actions (Citizen Max + Device Hygiene):"
    echo "   1. All Tier 0 actions apply"
    echo "   2. Get a separate personal device for private communications"
    echo "      if your employer has MDM installed on your current phone"
    echo "   3. Use a strong PIN — not biometric — for device unlock"
    echo "   4. Audit installed apps for stalkerware (unknown apps, high battery usage)"
    echo "   5. If stalkerware is suspected: factory reset without restoring backup"
    echo "   6. Secure your carrier account with a port-out PIN"
    if yn_yes "$Q5"; then
        echo ""
        echo -e "   ${RED}Domestic violence concern detected.${NC}"
        echo "   Contact the National DV Hotline: 1-800-799-7233"
        echo "   or the Safety Net project at techsafety.org"
        echo "   before making changes — abusers can detect sudden privacy changes."
    fi
    echo ""
    echo " Reference: Chapter 47 (Tier 1), Appendix I"
    ;;
2)
    echo -e " ${YELLOW}TIER 2: Institutional Surveillance (Local/State Level)${NC}"
    echo ""
    echo " Identified risks:"
    for r in "${REASONS[@]}"; do echo "   • $r"; done
    echo ""
    echo " Recommended actions (Two-Phone Strategy):"
    echo "   1. All Tier 0 and Tier 1 actions apply"
    echo "   2. Implement the full two-phone architecture (Volume 6)"
    echo "      Phone A: prepaid flip phone, cash SIM, no apps"
    echo "      Phone B: GrapheneOS Pixel, Wi-Fi only, no SIM, no Google accounts"
    echo "   3. Never carry both phones simultaneously"
    echo "   4. Never connect Phone B to home or work Wi-Fi"
    echo "   5. Use Faraday bags for both phones during transport"
    echo "   6. Replace Phone A SIM every 30–90 days"
    echo "   7. Run the GrapheneOS audit script (Appendix J Script 1) monthly"
    echo ""
    echo " Annual cost estimate: ~\$1,800"
    echo " Weekly effort: 5+ hours of OpSec discipline required"
    echo ""
    echo " IMPORTANT: Read Volume 6 in full before implementing."
    echo " Partial implementation is worse than no implementation."
    echo ""
    echo " Legal counsel recommended for your specific situation."
    echo " Reference: Volume 6, Chapter 47 (Tier 2), Appendix G"
    ;;
3)
    echo -e " ${RED}TIER 3: Federal / Intelligence Surveillance${NC}"
    echo ""
    echo " Identified risks:"
    for r in "${REASONS[@]}"; do echo "   • $r"; done
    echo ""
    echo " IMPORTANT:"
    echo " Contact a qualified attorney BEFORE taking any technical action."
    echo " The legal landscape at this tier matters as much as the technical one."
    echo ""
    echo " Organizations that can help:"
    echo "   • Electronic Frontier Foundation: eff.org/issues/national-security"
    echo "   • ACLU: aclu.org"
    echo "   • Freedom of the Press Foundation: freedom.press"
    echo "   • Reporters Committee for Freedom of the Press: rcfp.org"
    echo ""
    echo " Technical posture:"
    echo "   1. Implement full Tier 2 two-phone strategy with maximum discipline"
    echo "   2. Assume any single device may be targeted for exploitation"
    echo "   3. Do not rely on technical measures alone — legal protection is primary"
    echo "   4. Compartmentalize: minimum number of people know anything"
    echo "   5. Review Chapter 47 Tier 3 section and Chapter 42 (Residual Risks)"
    echo ""
    echo " Expected protection against Tier 3 adversaries: 40–60%"
    echo " A state actor with zero-day capabilities and a legal mandate"
    echo " cannot be defeated by configuration alone."
    ;;
esac

echo ""
echo -e "${BOLD}=================================================="
echo " This assessment is a starting point, not a guarantee."
echo " Reassess whenever your situation changes significantly."
echo -e "==================================================${NC}"
echo ""
```

---

## Script 3: Operation Checklist Generator (`opsec_checklist.sh`)

This script generates a pre-operation checklist for four scenario types: border crossing, protest/demonstration, legal matter/interaction with law enforcement, and standard high-threat travel. Pass the scenario as an argument.

```bash
#!/usr/bin/env bash
# opsec_checklist.sh
# Pre-operation OpSec checklist generator
# Version 1.0 — 2026-05-14
# Usage: bash opsec_checklist.sh [border|protest|legal|travel]

set -euo pipefail

BOLD='\033[1m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

SCENARIO="${1:-}"

if [ -z "$SCENARIO" ]; then
    echo ""
    echo "Usage: bash opsec_checklist.sh [SCENARIO]"
    echo ""
    echo "Available scenarios:"
    echo "  border   — International border crossing"
    echo "  protest  — Protest, demonstration, or public political action"
    echo "  legal    — Interaction with law enforcement or legal matter"
    echo "  travel   — High-threat domestic or international travel"
    echo ""
    echo "Example: bash opsec_checklist.sh border"
    exit 0
fi

DATE=$(date '+%Y-%m-%d %H:%M')

print_header() {
    echo ""
    echo -e "${BOLD}=================================================="
    echo " OpSec Checklist: $1"
    echo " Generated: $DATE"
    echo -e "==================================================${NC}"
    echo ""
}

print_section() {
    echo -e "\n${CYAN}── $1 ──${NC}"
}

item() {
    echo "  [ ] $1"
}

warn_item() {
    echo -e "  ${YELLOW}[!]${NC} $1"
}

crit_item() {
    echo -e "  ${RED}[CRITICAL]${NC} $1"
}

case "$SCENARIO" in
border)
    print_header "International Border Crossing"
    echo " Threat: Border agents have broad authority to inspect devices."
    echo " Strategy: Present Phone A (clean). Phone B stays hidden and off."
    echo ""
    echo -e " ${RED}IMPORTANT: Do NOT cross a border with Phone B powered on"
    echo -e " in your home country. Activate Phone B only after clearing customs"
    echo -e " in a secure location on the other side.${NC}"

    print_section "48 Hours Before Departure"
    item "Verify Phone A contains no apps, no accounts, no sensitive data"
    item "Verify Phone A SIM is not linked to your identity (cash purchase confirmed)"
    item "Verify Phone B is fully charged and in Faraday bag"
    item "Verify Phone B has never connected to home or work Wi-Fi"
    item "Back up any critical Phone B data to encrypted offline storage before travel"
    item "Review destination country's border search policies and legal rights"
    item "Note the name and number of a local attorney in destination country"
    item "Inform a trusted contact of your travel itinerary"

    print_section "Day of Departure"
    item "Phone A: charged, active, in accessible location (to present if asked)"
    item "Phone B: powered OFF, in Faraday bag, in checked luggage or deep in carry-on"
    item "Confirm you are NOT carrying both phones in the same bag"
    item "Remove any notes, cards, or documents linking you to Phone B"
    crit_item "Do NOT power on Phone B until you have cleared customs"

    print_section "At Border / Customs"
    item "If asked to unlock a phone, present Phone A only"
    item "Do not volunteer information about other devices"
    item "If asked directly about other devices, consult legal advice before responding"
    item "If Phone A is seized: it contains nothing sensitive. Cooperate and move on."
    warn_item "Refusal to unlock at a US border can result in device seizure and detention"
    warn_item "Know your rights in the specific jurisdiction — they vary significantly"

    print_section "After Clearing Customs"
    item "Reach a secure location before powering on Phone B"
    item "Power on Phone B only on a trusted network (not airport or hotel lobby Wi-Fi)"
    item "Verify Phone B's VPN connects before any communications"
    item "Check in with your trusted contact"
    ;;

protest)
    print_header "Protest / Demonstration"
    echo " Threat: Law enforcement may conduct tower dumps, capture MAC addresses,"
    echo " deploy IMSI catchers, or conduct physical device seizure."
    echo " Strategy: Minimize digital footprint. Know your rights."

    print_section "Day Before"
    item "Decide which phone you are bringing — ideally Phone A only"
    item "If bringing Phone B: verify it is in Faraday bag when not actively communicating"
    item "Write the phone number of a legal observer or lawyer on your ARM in permanent marker"
    item "Do not bring Phone B if you cannot maintain Faraday bag discipline throughout"
    item "Turn off Face ID and fingerprint unlock — use PIN only (cannot be compelled)"
    item "Enable full-disk encryption if not already enabled"
    item "Remove or disable non-essential apps that may run location telemetry"
    item "Consider using a burner phone purchased with cash for this specific event"

    print_section "Day Of — Before Leaving Home"
    item "Log out of social media apps (or uninstall them)"
    item "Clear browser history and cached location data"
    item "Verify VPN is connected"
    item "Write down: legal observer hotline, trusted contact, your own phone number"
    item "Leave Phone B at home if you are at Tier 0 or Tier 1"
    crit_item "Never use biometric unlock at a demonstration. Use PIN only."

    print_section "At the Event"
    item "Keep phone in pocket or Faraday bag when not in active use"
    item "Do not photograph or video other attendees without consent"
    item "Use Signal for all communications — not SMS"
    item "If police approach: do not unlock your phone. Invoke your rights."
    item "If arrested: say nothing. Ask for a lawyer. Do not consent to searches."
    warn_item "If photographed or detained with your phone: assume tower dump occurred"

    print_section "After the Event"
    item "Review app location permissions — revoke any that activated during the event"
    item "Check for unfamiliar apps that may have been installed"
    item "If detained and phone was seized: contact a lawyer before getting a replacement"
    item "If phone was returned after detention: treat it as potentially compromised"
    crit_item "A returned device may have been imaged or implanted. Consider replacing it."
    ;;

legal)
    print_header "Law Enforcement Interaction / Legal Matter"
    echo " Threat: Device seizure, forensic extraction, account subpoenas."
    echo " Strategy: Know what is on each device. Know your rights."
    echo ""
    echo -e " ${RED}IMPORTANT: If you have received a subpoena or search warrant,"
    echo -e " contact a lawyer BEFORE taking any action. Do not delete anything."
    echo -e " Destroying evidence is a separate crime.${NC}"

    print_section "If Contacted by Law Enforcement"
    item "Do not consent to a phone search — you have the right to refuse"
    item "Do not unlock your phone for law enforcement without a warrant"
    item "If a warrant is presented: do not resist, but do not assist beyond compliance"
    item "Say: 'I am invoking my right to remain silent and my right to an attorney'"
    item "Call your attorney immediately"
    crit_item "Do NOT delete any data. Do NOT factory reset. Do NOT 'clean up' your phone."
    crit_item "Evidence destruction is a crime. Spoliation has severe legal consequences."

    print_section "If You Anticipate Legal Proceedings"
    item "Identify which device (Phone A or Phone B) is most likely to be subject to discovery"
    item "Ensure Phone B has never been at the same location as Phone A (co-location)"
    item "Review what communications are on Phone A — anything there is potentially discoverable"
    item "Contact a lawyer to understand the scope of any anticipated subpoena or search"
    item "Do not make any changes to devices or accounts without legal advice"

    print_section "After a Device Seizure"
    item "Notify all Signal contacts that your account/device was seized"
    item "Rotate passwords for all accounts that were accessible on the seized device"
    item "Contact your carrier to flag the device IMEI if you want to prevent unauthorized use"
    item "Contact Signal (if applicable) — note Signal retains only registration date and last connection"
    item "Work with your attorney to understand what was obtained and what it reveals"
    warn_item "Assume the forensic extraction captured everything on the device, including deleted files"
    ;;

travel)
    print_header "High-Threat Domestic or International Travel"
    echo " Threat: Device theft, physical surveillance, opportunistic data capture."
    echo " Strategy: Minimize what you carry. Protect what you keep."

    print_section "Before Departure"
    item "Audit what is on each phone — remove anything you do not need for the trip"
    item "Note serial numbers and IMEIs of both phones (store in secure location at home)"
    item "Ensure full-disk encryption is enabled on both devices"
    item "Verify PIN/passphrase is set (not biometric only)"
    item "Test Faraday bags — call each phone while bagged to confirm no signal"
    item "Verify VPN client is configured and tested"
    item "Back up critical data to encrypted offline storage before departure"
    item "Inform a trusted contact of itinerary and check-in schedule"

    print_section "During Travel"
    item "Keep Phone B in Faraday bag during transit (trains, airports, hotels)"
    item "Do not leave either device unattended in hotel rooms"
    item "Use hotel safe for Phone B storage when not in use"
    item "Avoid charging phones via USB at public charging stations (juice jacking risk)"
    item "Use your own charger and a USB data blocker at any public charging port"
    item "Connect only to known, trusted Wi-Fi networks with Phone B"
    warn_item "Hotel Wi-Fi is not trusted. Use VPN on any hotel or public network."

    print_section "If Device Is Lost or Stolen"
    item "Notify carrier to suspend service on Phone A SIM immediately"
    item "Remotely wipe Phone A if possible (Find My Device / Find My iPhone)"
    item "Notify all contacts that device was compromised"
    item "Change passwords for all accounts accessible on the device"
    item "File a police report (required for insurance; useful for documentation)"
    item "If Phone B is lost: treat all communications as potentially exposed"
    crit_item "Do not use a replacement device until you have reached a secure location"
    ;;

*)
    echo "Unknown scenario: $SCENARIO"
    echo "Valid options: border, protest, legal, travel"
    exit 1
    ;;
esac

echo ""
echo -e "${BOLD}=================================================="
echo " Complete all items before proceeding."
echo " Sign off: ________________________  Date: __________"
echo -e "==================================================${NC}"
echo ""
echo " References:"
echo "   • Chapter 32 (When Two Phones Are Actually Necessary)"
echo "   • Chapter 38 (The Unbreakable OpSec Rules)"
echo "   • Chapter 47 (Threat Tier Matrix)"
echo "   • Appendix G (Quick Reference Cards)"
echo ""
```

---

## Running the Scripts

### Quick start (macOS / Linux)

```bash
# Make scripts executable
chmod +x verify_grapheneos.sh threat_model.sh opsec_checklist.sh

# Run threat model assessment
bash threat_model.sh

# Audit a connected GrapheneOS device
bash verify_grapheneos.sh

# Generate a pre-operation checklist
bash opsec_checklist.sh border
bash opsec_checklist.sh protest
bash opsec_checklist.sh legal
bash opsec_checklist.sh travel
```

### Notes on the GrapheneOS audit script

The audit script performs read-only operations. It does not modify any device settings. All ADB commands are shell-based queries (`settings get`, `getprop`, `pm list packages`). No data is exfiltrated; all output goes to stdout.

USB debugging must be enabled to run the audit. **Disable USB debugging immediately after the audit is complete** — the script's WARN output reminds you of this. USB debugging left enabled is an unnecessary attack surface.

The audit script does not detect:
- Compromised firmware or bootloader
- Zero-day exploits targeting userspace processes
- Network-level surveillance (your ISP, the access point you are connected to)
- Hardware implants

A passing audit score means your configuration settings are correct. It does not certify that your device is uncompromised at the firmware or hardware level.
