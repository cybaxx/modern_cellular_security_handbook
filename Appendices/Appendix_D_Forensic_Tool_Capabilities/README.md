# Appendix D: Forensic Tool Capabilities

## Introduction

This appendix catalogs the major forensic tools used by law enforcement and private investigators to extract data from mobile devices. Understanding what these tools can and cannot do is essential for threat modeling. If your device is ever seized, one or more of these tools will be used against it.

The goal is not to provide a "how-to" for defeating forensic tools (that is a separate, legal, and context-dependent topic). Rather, this appendix documents capabilities so that you can make informed decisions about device selection, encryption, and operational security.

## Cellebrite UFED (Universal Forensic Extraction Device)

### Overview

Cellebrite is the industry standard for mobile device forensics. Used by law enforcement agencies worldwide, it supports thousands of device models and can extract data from locked, damaged, or otherwise inaccessible devices.

### Extraction Types

| Extraction Level | What It Recovers | Success Rate |
|---|---|---|
| Logical extraction | Call logs, SMS/MMS, contacts, photos, app data (unprotected) | ~90% on unlocked devices |
| File system extraction | Full file system including deleted files, app databases, system logs | ~70–80% on supported devices |
| Physical extraction | Bit-for-bit copy of storage, including deleted and hidden data | ~50–60% (varies by device/OS) |
| BFU (Before First Unlock) extraction | Data accessible before device is unlocked after reboot | ~10–20% on modern iOS |
| Cloud extraction | Data from iCloud, Google Drive, other cloud services | ~80% if credentials available |

### Supported Devices

- iOS: All current iPhone models. GrayKey integration enables extraction from locked iOS devices.
- Android: Most Samsung, Pixel, OnePlus, LG, Motorola devices. Limited support for Chinese brands (Xiaomi, Huawei, Oppo) in some regions.
- Feature phones: Extensive support for Nokia, Alcatel, and other dumb phones.

### Key Capabilities

- **Lock state bypass:** Cellebrite can bypass locks on some Android devices via bootloader exploits or recovery mode.
- **App data extraction:** Decrypts or extracts data from Signal, WhatsApp, Telegram, Facebook Messenger, and thousands of other apps. The success rate depends on OS security features.
- **Deleted data recovery:** Recovers deleted messages, photos, and call logs from unallocated storage space.
- **Timeline analysis:** Creates a chronological timeline of all device activity.
- **Cloud extraction:** If the device is unlocked, Cellebrite can extract data from connected cloud accounts.

### Limitations

- **GrapheneOS:** Full-disk encryption with a strong passphrase significantly resists Cellebrite extraction. File-based encryption combined with a long passphrase (20+ characters) makes physical extraction infeasible.
- **Signal on GrapheneOS:** If Signal uses the OS-level file-based encryption and a strong passphrase, Cellebrite cannot extract Signal messages in plaintext.
- **Locked devices:** Modern iOS and Pixel devices with secure elements resist extraction when locked.
- **iCloud/Google account:** If cloud sync is disabled, cloud extraction returns nothing.

### Forensic Value Against Two-Phone Strategy

| Device | Extraction Likelihood | Notes |
|---|---|---|
| Phone A (dumb flip) | ~100% | No encryption, all data accessible |
| Phone B (GrapheneOS, locked) | ~5–20% | Strong passphrase + secure element defeat most extraction |
| Phone B (GrapheneOS, unlocked) | ~50–70% | If device is unlocked when seized, file system is accessible |

## GrayKey

### Overview

GrayKey is a specialized iOS forensic tool developed by GrayShift. It is the primary method for extracting data from locked iPhones. Law enforcement agencies purchase or lease GrayKey units.

### Capabilities

| Feature | Details |
|---|---|
| Lock state bypass | Can brute-force iPhone passcodes (4- and 6-digit PINs faster, complex passcodes slower or impossible) |
| Extraction speed | Depends on passcode complexity. Simple PINs: hours. Complex passcodes: weeks or infeasible |
| Data recovered | All iOS data accessible to the OS: messages, photos, app data, keychain, health data, location history |
| iOS version support | GrayKey exploits iOS vulnerabilities. Each iOS update may close the exploit, requiring GrayKey updates |

### Limitations

- **Complex passcodes:** An alphanumeric passcode with 10+ characters is effectively immune to GrayKey brute force.
- **New iOS versions:** GrayKey exploits are specific to iOS versions. Updated iOS devices may be protected for weeks or months.
- **Lockdown Mode:** iOS Lockdown Mode (introduced in iOS 16) reduces the attack surface available to GrayKey.
- **USB Restricted Mode:** iOS automatically disables USB data access if the device has not been unlocked within the last hour. This blocks GrayKey.

### Relevance to Two-Phone Strategy

GrayKey is only relevant if you carry an iPhone. The two-phone strategy as defined in this handbook does not recommend iOS for Phone B. If an iPhone is used for any purpose, understand that GrayKey makes extraction of a locked iPhone feasible for law enforcement.

## Magnet AXIOM

### Overview

Magnet AXIOM is a comprehensive digital forensics platform that processes data from mobile devices, computers, cloud services, and drones. It is used by law enforcement and corporate investigators.

### Capabilities

| Feature | Details |
|---|---|
| Multi-platform | iOS, Android, Windows, macOS, Linux, cloud |
| Artifact categories | 500+ artifact types including app usage, location, web history, file activity |
| Cloud collection | Extracts from iCloud, Google, Microsoft, Dropbox, and social media accounts |
| Timeline analysis | Cross-device timeline creation |
| AI-powered analysis | Automated categorization and prioritization of relevant data |
| Reporting | Court-admissible report generation |

### Key Artifacts for Forensics

- **Location history:** Magnet AXIS (Magnet AXIOM Cloud) can extract Google Maps timeline data, iPhone Significant Locations, and other cloud-based location records.
- **App usage:** Installed apps, usage statistics, last-used timestamps.
- **Messaging:** Extracts message databases from Signal, WhatsApp, Telegram, Facebook Messenger (if physical extraction is successful).
- **File operations:** Recently opened, modified, or deleted files.
- **Network connections:** Known Wi-Fi networks, Bluetooth pairings, cellular tower data.

### Limitations

- **Encryption:** Like Cellebrite, AXIOM cannot bypass strong encryption provided by GrapheneOS or iOS with a complex passcode.
- **Cloud access:** Cloud extraction requires the user's credentials or an unlocked device with authenticated cloud sessions.
- **Physical access required:** AXIOM requires physical possession of the device or credentials for cloud accounts.

## Wireshark for Cellular Analysis

### Overview

Wireshark is a free, open-source network protocol analyzer. While primarily used for IP network analysis, it can be extended to analyze cellular protocols.

### Capabilities for Cellular Forensics

| Feature | Details |
|---|---|
| 3GPP protocol dissection | NAS (TS 24.301, 24.501), S1AP (TS 36.413), NGAP (TS 38.413), RRC (with plugins) |
| LTE capture | Requires specialized hardware (via S1-MME interface, not over the air) |
| 5G capture | Via NGAP interface, requiring access to the N2 reference point |
| Wi-Fi capture | Monitor mode adapters for 2.4 GHz and 5 GHz, full 802.11 management frame analysis |
| Traffic analysis | Packet timing, size distribution, protocol identification |

### How It Is Used

Wireshark for cellular analysis is typically used by:

- **Network engineers:** Troubleshooting protocol issues
- **Forensic analysts:** Correlating intercepted traffic with known user activity
- **Researchers:** Analyzing network behavior and identifying data leaks
- **Lawful intercept monitoring:** Reviewing intercepted communications

### Limitations

- **Over-the-air capture:** Standard Wireshark cannot capture 4G/5G over-the-air signals. This requires software-defined radio hardware and specialized decoding tools.
- **Encrypted channels:** Most modern cellular traffic is encrypted at the NAS layer (5G) or transport layer (HTTP/TLS).
- **Access required:** Capturing S1AP or NGAP traffic requires access to carrier infrastructure, which is generally only available to network operators or lawful intercept programs.

### Value for Researchers

Wireshark is invaluable for Wi-Fi analysis experiments (Chapter 45). With a monitor-mode adapter, researchers can capture:

- Probe requests from their own devices
- Beacon frames from nearby access points
- Association and authentication frames
- DHCP and DNS traffic

## SnoopSnitch

### Overview

SnoopSnitch is an Android app that analyzes mobile network security. It requires root access and a Qualcomm-based device.

### Capabilities

| Feature | Details |
|---|---|
| IMSI catcher detection | Detects when a fake base station (Stingray) is present |
| Network security analysis | Tests for encryption downgrade attacks, null cipher usage |
| Signaling analysis | Logs NAS and RRC messages for forensic review |
| Baseband monitoring | Tracks baseband firmware behavior |
| Cell ID logging | Records all observed cell towers |

### How It Works

SnoopSnitch uses Qualcomm's DIAG interface to access baseband-level logging. This gives visibility into:

- What the baseband is transmitting and receiving
- Which network requests are being made
- Whether encryption is active or has been downgraded
- Whether unexpected identity requests are being received

### Limitations

- **Qualcomm-only:** Requires a Qualcomm baseband. Samsung Exynos, MediaTek, and other basebands are not supported.
- **Root required:** The device must be rooted to access the DIAG interface.
- **GrapheneOS compatibility:** GrapheneOS runs on Pixel devices, which use Qualcomm basebands. However, root access is not typical on GrapheneOS, and some DIAG access may be restricted.
- **Passive detection only:** SnoopSnitch can detect IMSI catchers but cannot prevent them.

## Data Extraction Comparison by Device

| Device / OS | Extraction Resistance | Recommended Tool | Notes |
|---|---|---|---|
| Flip phone (no OS security) | None | Cellebrite UFED | All data accessible |
| Stock Android (locked, PIN) | Low–Medium | Cellebrite UFED | Simple PINs bypassable |
| Stock Android (locked, strong passphrase) | Medium | Cellebrite UFED | File-based encryption with >20 chars resists |
| GrapheneOS (locked, strong passphrase) | High | Limited by encryption | Physical extraction not feasible |
| GrapheneOS (unlocked or after unlock) | Medium | Cellebrite UFED | File system accessible if unlocked |
| iOS (locked, simple PIN) | Low | GrayKey | PIN brute-force feasible |
| iOS (locked, complex passcode) | High | GrayKey limited | Complex passcodes may be infeasible |
| iOS (Lockdown Mode, complex passcode) | Very high | GrayKey severely limited | Reduced attack surface |
| Deleted Signal messages (GrapheneOS) | Very high | Cannot recover | File-based encryption overwrites |

## Key Takeaways for Threat Modeling

1. **Phone A (dumb flip) has no forensic protection.** It can be fully extracted by any tool within minutes. This is acceptable because Phone A contains no sensitive data.

2. **Phone B (GrapheneOS) is resistant to forensic extraction only if it is locked with a strong passphrase when seized.** If the device is unlocked, all data is accessible.

3. **Remote wipe is essential.** If Phone B is at risk of seizure, remote wipe capability (via a trusted network trigger) should be configured.

4. **Never use biometric unlock.** Biometrics (fingerprint, face) can be compelled by law enforcement in most jurisdictions. Use a strong alphanumeric passphrase only.

5. **Cloud sync is the enemy.** If GrapheneOS syncs data to any cloud service, forensic tools can access that data via cloud extraction. Disable all cloud synchronization.
