# Appendix F: Recommended Hardware and Software

## Introduction

This appendix provides specific, tested hardware and software recommendations for implementing the two-phone strategy. These recommendations are based on forensic analysis, community testing, and practical operational experience.

Each recommendation includes the rationale, known limitations, and alternatives. The goal is not to provide a single "best" configuration but to enable informed choices based on your specific threat model, budget, and technical comfort level.

## Phones

### Phone A: The Burner Public Face

#### Primary Recommendation: Nokia 225 4G

| Feature | Detail |
|---|---|
| Network | 4G LTE (no 5G) |
| Operating System | Nokia Series 30+ (proprietary, no apps) |
| GPS | Not present |
| Wi-Fi | Not present |
| Bluetooth | Basic, can be disabled |
| Camera | Yes (can be removed or taped) |
| Battery | Removable |
| Approximate Cost | $40–60 |

**Rationale:** The Nokia 225 4G has no Wi-Fi, no GPS, and no app ecosystem. It runs a proprietary feature phone OS that cannot install tracking software. The removable battery allows physical power isolation. 4G-only operation avoids 5G Multi-RTT positioning.

**Limitations:** The camera is a potential EXIF leakage vector. Physically remove or permanently tape the camera lens. The phone still transmits IMSI, IMEI, and Timing Advance to the carrier.

#### Alternative: Alcatel Go Flip 4

| Feature | Detail |
|---|---|
| Network | 4G LTE |
| Operating System | KaiOS (smart-feature phone) |
| GPS | Present (can be disabled) |
| Wi-Fi | Present (can be disabled) |
| Approximate Cost | $50–80 |

**Note:** KaiOS supports lightweight apps and has built-in Google services (Google Assistant, Google Maps). These must be disabled or the phone should not be used if apps are installed.

#### Alternative: Any 4G dumb phone without Wi-Fi

The critical requirement is no Wi-Fi. Wi-Fi on Phone A creates a BSSID geolocation vector. Any 4G-only feature phone without Wi-Fi is acceptable.

### Phone B: The Private Hub

#### Primary Recommendation: Google Pixel 6a / 7a

| Feature | Detail |
|---|---|
| Network | 4G/5G (cellular radio disabled in software) |
| Operating System | GrapheneOS (recommended) or LineageOS |
| Wi-Fi | 802.11 a/b/g/n/ac/ax (Wi-Fi 6 on 7a) |
| Bluetooth | Bluetooth 5.2 (disabled for privacy) |
| Camera | Yes (disabled in GrapheneOS via Camera toggle or physical tape) |
| Secure Element | Titan M2 chip |
| Approximate Cost | $350–500 (new) |

**Rationale:** Google Pixel devices have the best GrapheneOS support, timely security updates, and a verified boot chain (Titan chip). The bootloader can be re-locked after GrapheneOS installation for physical tamper protection.

**Limitations:** Pixel devices use Qualcomm basebands (proprietary, closed-source). While the cellular radio can be disabled in GrapheneOS, the baseband firmware is still present on the device. Physical removal of the cellular radio is not feasible for most users.

#### Alternative: Google Pixel 8 / 8a

Newer Pixel devices offer improved hardware security (Titan M2 chip, improved IOMMU for baseband isolation). The trade-off is higher cost ($500–700). GrapheneOS support is generally available within weeks of Pixel release.

#### Avoid for Phone B:

| Device | Reason to Avoid |
|---|---|
| Samsung Galaxy series | Knox security limits custom OS installation; Exynos basebands (non-Qualcomm) are less audited |
| Motorola Moto G | Delayed security updates, poor GrapheneOS support, questionable long-term support |
| OnePlus | Declining custom OS support, inadequate security update commitment |
| Xiaomi / Huawei | Chinese baseband firmware, potential backdoor concerns, poor GrapheneOS support |

## Operating Systems

### Phone B: GrapheneOS

| Feature | Detail |
|---|---|
| Base | Android Open Source Project |
| Google Services | Completely removed (optional sandboxed Google Play) |
| Security features | Hardened memory allocator, hardened kernel, verified boot |
| Privacy features | Network permission toggle, sensor permission toggle, MAC randomization, Wi-Fi/BT scanning disabled by default |
| Update model | Over-the-air updates, usually within days of Android security patch release |
| Bootloader | Can be re-locked after installation |
| Cost | Free |

**Installation:** Requires a Google Pixel device. Installation takes approximately one hour using the web installer at https://grapheneos.org/install.

**Key configurations after installation:**
- Disable cellular radio (Settings → Network & Internet → SIMs → Disable)
- Enable MAC randomization (for each Wi-Fi network)
- Disable Wi-Fi and Bluetooth scanning
- Deny location permissions to all apps by default
- Set a strong alphanumeric passphrase (20+ characters)
- Do not install Google Play Services (use sandboxed version only if absolutely needed)
- Disable camera hardware (in GrapheneOS settings)

### Phone B Alternative: LineageOS

| Feature | Detail |
|---|---|
| Base | Android Open Source Project |
| Google Services | Not included (can be added via MicroG) |
| Security features | Basic Android security, no specialized hardening |
| Update model | Community-driven, delayed compared to GrapheneOS |
| Bootloader | Remains unlocked after installation |
| Cost | Free |

LineageOS is acceptable for medium-risk users but does not provide the same level of security as GrapheneOS. The unlocked bootloader is a physical attack vector. Updates may be delayed for weeks or months.

### Computer: Tails OS

| Feature | Detail |
|---|---|
| Base | Debian Linux |
| Design | Amnesiac — leaves no trace on the host computer |
| Network | Routes all traffic through Tor |
| Applications | Tor Browser, Thunderbird (with Enigmail), LibreOffice, KeePassXC |
| Persistence | Optional encrypted persistent storage |
| Boot method | USB drive or DVD |
| Cost | Free |

**Installation:** Requires a USB drive (8 GB minimum). Installation from the Tails website takes approximately 30 minutes.

### Computer Alternative: Qubes OS

| Feature | Detail |
|---|---|
| Base | Xen hypervisor with Linux dom0 |
| Design | Compartmentalized — each application runs in a separate virtual machine (AppVM) |
| Network | VPN or Tor per-AppVM |
| Security | Strong isolation between compartments via hardware virtualization |
| Hardware | Requires modern Intel or AMD CPU with virtualization support |
| Cost | Free |

Qubes is the gold standard for computer security but has a steeper learning curve and higher hardware requirements than Tails.

## VPN Providers

### Primary Recommendation: Mullvad

| Feature | Detail |
|---|---|
| Cost | €5/month (approximately $5.50) |
| Payment | Cash (by mail), Monero, Bitcoin, bank transfer, credit card |
| Account system | Random account number (no email, no username required) |
| Logging policy | Audited no-log (multiple independent audits) |
| Jurisdiction | Sweden |
| Protocols | WireGuard, OpenVPN |
| Apps | Windows, macOS, Linux, Android, iOS |
| Port forwarding | Available on request |

**Rationale:** Mullvad is the only major VPN that allows completely anonymous account creation (no email, no username). Cash payment by mail eliminates all digital payment trails. Multiple audits confirm the no-log policy.

### Alternative: IVPN

| Feature | Detail |
|---|---|
| Cost | From $100/year |
| Payment | Cash (by mail), Monero, credit card, PayPal |
| Account system | Account ID (no email required) |
| Logging policy | Audited no-log (multiple audits) |
| Jurisdiction | Gibraltar (UK overseas territory) |
| Protocols | WireGuard, OpenVPN |
| Anti-tracking | Built-in tracker and ad blocking |

IVPN is more expensive than Mullvad but offers stronger anti-tracking features and a similar privacy posture.

### Alternative: ProtonVPN

| Feature | Detail |
|---|---|
| Cost | Free tier (limited) or paid from $48/year |
| Payment | Credit card, PayPal, Bitcoin |
| Account system | ProtonMail account (email required) |
| Logging policy | No-log (Swiss jurisdiction) |
| Jurisdiction | Switzerland |
| Protocols | WireGuard, OpenVPN, IKEv2 |

ProtonVPN's free tier is acceptable for low-risk users. The paid tier provides better performance and supports Tor over VPN. The requirement for a ProtonMail account creates an identity link.

## Faraday Bags

### Testing Requirement

Any faraday bag used for this strategy must be tested (see Chapter 45, Experiment 3). Bags that claim 90 dB or better attenuation should block cellular, Wi-Fi, and Bluetooth frequencies.

### Recommended Brands

| Brand | Approximate Cost | Notes |
|---|---|---|
| Mission Darkness | $30–50 | Dual-layer, independently tested, available in various sizes |
| Silent Pocket | $40–60 | Stylish, tested, but expensive |
| DefenderPad | $20–30 | Simple pouch, good for a single phone |
| OFF Pocket | $25–35 | Small, good for key fobs and small phones |

### Testing Protocol

1. Place the phone inside the bag, seal completely.
2. Call the phone from another device.
3. If the call goes to voicemail, the bag is blocking cellular.
4. Test at least three times with different phone orientations.
5. Test with Wi-Fi enabled and check for successful connections.

### Replacement Schedule

- Inspect monthly for fabric wear, especially at zipper seams.
- Replace every 6–12 months.
- Replace immediately if a test call rings through.

## Privacy Applications

### Signal

| Feature | Detail |
|---|---|
| Primary use | Encrypted messaging and voice calls |
| Encryption | Signal Protocol (X3DH, Double Ratchet) |
| Metadata collection | Minimal (registration timestamp, last-seen) |
| Registration | Requires phone number (use burner) |
| Platform | Android, iOS, Desktop |
| Cost | Free |

**Key settings:**
- Enable registration lock PIN
- Disable read receipts (Privacy → Advanced)
- Enable censorship circumvention (if required)
- Use a burner number for registration

### Orbot (Tor for Android)

| Feature | Detail |
|---|---|
| Purpose | Routes app traffic through Tor |
| Integration | VPN mode routes all device traffic through Tor |
| Cost | Free |

**Use case:** Orbot can be used on Phone B to route Signal traffic through Tor, adding an anonymity layer. Performance may be degraded.

### Tor Browser

| Feature | Detail |
|---|---|
| Purpose | Anonymous browsing |
| Privacy features | Blocks trackers, isolates cookies per-site, resists browser fingerprinting |
| Platform | Android, Desktop |
| Cost | Free |

### Bitwarden

| Feature | Detail |
|---|---|
| Purpose | Password manager |
| Encryption | AES-256, zero-knowledge architecture |
| Platform | All major platforms |
| Cost | Free tier available, paid tier from $10/year |

**Note:** Do not store passwords that link to your identity in the same Bitwarden vault as anonymous accounts. Use separate vaults or instances for compartmentalization.

### Aegis Authenticator

| Feature | Detail |
|---|---|
| Purpose | Two-factor authentication (TOTP) |
| Platform | Android |
| Encryption | AES-256 encrypted backup |
| Cost | Free |

**Note:** Aegis is open source and does not require network permissions. It is the preferred 2FA app for privacy-focused users.

## Data Broker Removal Services

### DeleteMe

| Feature | Detail |
|---|---|
| Service | Continuous removal from 50+ data broker sites (Whitepages, Spokeo, BeenVerified, etc.) |
| Cost | $129/year (individual) |
| Effectiveness | High — ongoing removal prevents re-listing |
| Platform | Web-based |

### OneRep

| Feature | Detail |
|---|---|
| Service | Removal from 190+ data broker and people-search sites |
| Cost | $99/year (individual) |
| Effectiveness | High |
| Platform | Web-based |

### Manual Opt-Out Resources

For those who prefer not to pay for data broker removal:

- **Privacy Rights Clearinghouse:** Maintains a list of opt-out instructions for major data brokers.
- **Michael Bazzell's "Extreme Privacy"**: Contains detailed manual opt-out instructions.
- **r/privacy wiki:** Community-maintained list of opt-out resources.
