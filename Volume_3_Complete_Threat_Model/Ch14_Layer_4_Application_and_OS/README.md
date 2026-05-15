# Chapter 14: Layer 4 — Application & OS (Phone B & Computer)

## Overview

Layer 4 addresses vulnerabilities at the application and operating system level. Even if network-layer protections are perfect — encrypted DNS, VPN, no residential ISP — the applications running on Phone B and the Computer can leak identifying information through multiple channels. Google Play Services tracks device location and usage. Signal metadata reveals communication patterns. Camera EXIF data embeds GPS coordinates in photos. Browser fingerprinting builds a persistent profile from screen resolution, fonts, timezone, and canvas hashes.

Layer 4 is the most complex vulnerability layer because it encompasses dozens of distinct attack surfaces across multiple operating systems, applications, and protocols. The unifying principle is simple: applications are not designed for privacy. Every application has telemetry, logging, analytics, and debugging features that can be repurposed for surveillance. Controlling Layer 4 requires understanding which applications to trust, how to configure them, and what data they expose.

---

## Vulnerability 1: Google Play Services / Firebase Cloud Messaging

**Severity: Critical (if present)**

Google Play Services is a proprietary background service on Android devices that provides APIs for location, push notifications (Firebase Cloud Messaging / FCM), account management, device registration, and usage analytics. On a standard Android phone, Play Services has system-level privileges and continuous network access.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Precise location, device ID, usage patterns, installed applications |
| Collection Method | Google servers (accessible via warrant or subpoena) |
| Mitigation | Use GrapheneOS, remove all Google services |

Google Play Services collects and transmits to Google:[^1]
- Device location (GPS, Wi-Fi, cellular)
- Device identifiers (Android ID, advertising ID, device serial)
- Installed application list
- Usage patterns (when apps are opened, how long they are used)
- Network connectivity data (Wi-Fi BSSIDs, cellular tower IDs)

This data is stored on Google's servers and is accessible via legal process. Google receives thousands of subpoenas and warrants annually from US law enforcement, and the company provides data in response to valid legal requests. For an adversary investigating a target, Google data provides a complete timeline of device activity and location.

GrapheneOS eliminates this vulnerability by removing Google Play Services entirely.[^2] Without Play Services, the device has no Google telemetry, no FCM, no advertising ID, and no Google location services. This is the single most impactful privacy measure for an Android device.

However, removing Google Play Services breaks applications that depend on its APIs. Signal works fine without Play Services (it uses WebSocket for push notifications). But many other applications will not function. Phone B should be configured with only the applications that are essential and that function without Google services.

---

## Vulnerability 2: Signal Metadata

**Severity: High**

Signal is widely regarded as the gold standard for end-to-end encrypted messaging. The content of Signal messages — text, images, files — is encrypted and inaccessible to Signal's servers. However, metadata is not encrypted. Signal's servers see:[^3]

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Who you communicate with, when, how often, approximate location (IP-based) |
| Collection Method | Signal servers (court order) |
| Mitigation | Burner phone number, no contact sync, use via Tor |

The metadata that Signal's servers observe includes:
- The phone numbers of both parties in a communication
- The timestamps of messages and calls
- The approximate duration of voice/video calls
- The IP address of each participant (for message routing)

A court order served on Signal can compel the company to produce all metadata associated with a target phone number. While Signal has fought such orders and publicly disclosed them in transparency reports, the company does comply with valid legal process.[^4]

The key risk for the two-phone strategy is that Signal metadata reveals the social graph — who communicates with whom, when, and how often. If an adversary identifies Phone B's Signal number (through a leak, a compromised contact, or an associate's compromised device), they can obtain the entire communication pattern for that account.

Mitigations include:
- Registering Signal with a burner phone number (VoIP or prepaid SIM used once, then discarded)
- Disabling contact synchronization (preventing Signal from uploading your address book)
- Using Signal over Tor to mask the IP address
- Avoiding linking Signal to any identity-linked account (email, phone number, payment method)

---

## Vulnerability 3: Camera EXIF Data

**Severity: High**

Exchangeable Image File Format (EXIF) data is metadata embedded in digital photographs. Modern smartphones embed extensive EXIF data including GPS coordinates, timestamp, device make and model, camera settings, and orientation.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | GPS coordinates, timestamp, device model, unique camera sensor identifiers |
| Collection Method | Shared photos distributed digitally or posted online |
| Mitigation | Disable location tagging, strip metadata before sharing |

When a photo is taken with Phone B, the EXIF data records:
- Latitude and longitude of the location where the photo was taken
- Precise timestamp (often accurate to milliseconds)
- Device make and model (e.g., "Google Pixel 7 Pro")
- Camera serial number or sensor identifier (in some implementations)
- Camera settings (aperture, shutter speed, ISO, focal length)

If a photo taken with Phone B is shared — via Signal, email, or social media — the EXIF data travels with the image unless explicitly stripped. An adversary who obtains the photo can extract the GPS coordinates and determine where the user was when the photo was taken.

The forensic danger is compounded by the existence of databases that correlate camera sensor patterns to specific devices. The "camera fingerprint" — fixed-pattern noise unique to each camera sensor — can identify which specific device took a photo, even after EXIF metadata has been removed.

Mitigations:
- Disable location tagging in the camera application settings
- Use metadata stripping tools (e.g., EXIF Purge) before sharing any photo
- Avoid taking photos with Phone B entirely; use a dedicated camera if photos are needed
- On GrapheneOS, the built-in camera app has an option to disable location storage[^5]

---

## Vulnerability 4: Browser Fingerprinting

**Severity: Medium**

Browser fingerprinting is a technique used by websites to identify and track users based on the unique configuration of their browser and device. Unlike cookies, which are stored on the device and can be cleared, browser fingerprints are derived from characteristics inherent to the device.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Screen resolution, installed fonts, timezone, canvas hash, WebGL renderer |
| Collection Method | JavaScript executed by any website visited |
| Mitigation | Tor Browser, Tails OS, resistFingerprinting in Firefox |

The elements that contribute to a browser fingerprint include:
- Screen resolution and color depth
- Installed system fonts (one of the most entropy-rich signals)
- Timezone and language settings
- Canvas fingerprint (rendering a hidden image and hashing the result)
- WebGL renderer and graphics card model
- CPU core count and hardware concurrency
- Browser version, user agent, and installed extensions
- Touch support and input device capabilities

Research has shown that 83–90% of desktop browsers have unique fingerprints. Mobile browsers have marginally less entropy but are still highly distinguishable. Browser fingerprinting is used by advertising networks, analytics platforms, and fraud detection systems.

The most effective mitigation is Tor Browser, which is specifically designed to resist fingerprinting. All Tor Browser users have the same fingerprint (same window size, same fonts, same canvas behavior), making individual users indistinguishable. Tails OS goes further by running Tor Browser in an amnesiac environment with no persistent state.

GrapheneOS's Vanadium browser provides improved privacy compared to Chrome, but does not provide the same level of fingerprinting resistance as Tor Browser.[^6] For sensitive communications, Phone B should use Tor Browser for web browsing.

---

## Vulnerability 5: Hostname / Device Name Leakage

**Severity: Medium**

The device hostname (see Layer 2, Chapter 12) is set during initial setup and often includes identifying information. The hostname is visible in DHCP logs, network scans, and certain application interactions.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | User-set device identifiers (e.g., "Johns-Private-Phone") |
| Collection Method | Network scans, router logs, application telemetry |
| Mitigation | Change hostname to a generic identifier |

The hostname is a persistent identifier that leaks in multiple contexts:
- DHCP requests to Wi-Fi networks
- mDNS/Bonjour service announcements
- Application telemetry that includes device model information
- Network scan tools (Nmap, Fing)

Changing the hostname to "android-device" or "linux-device" removes the identifying information. On GrapheneOS, this is configurable in developer settings.[^7]

---

## Vulnerability 6: Misconfigured App Permissions

**Severity: High**

Android and modern desktop operating systems use permission-based access control for application resources. However, many applications request — and users grant — permissions that are not required for the application's core functionality.[^8]

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Precise GPS location, contact list, file storage, camera, microphone |
| Collection Method | Application developer servers (via telemetry) |
| Mitigation | Deny all permissions by default, grant only what is necessary |

Common permission abuses include:
- Weather apps requesting precise GPS location (for "personalized forecasts")
- Flashlight apps requesting camera and microphone access
- Messaging apps requesting contact list access (uploading contacts to servers)
- Games requesting file storage access

On GrapheneOS, the permission model is enhanced with:[^9]
- Network permission toggle (per-app network access control)
- Sensors permission toggle (controls camera, microphone, accelerometer)
- Storage scoping (prevents apps from accessing files they did not create)
- Permission auto-reset (revokes permissions when app is not in use)

The operational rule for Phone B: deny all permissions by default. Grant permissions only when an application demonstrably requires them for a specific function, and revoke them when the function is complete.

---

## Vulnerability Summary Table

| Vulnerability | Data Exposed | Collection Method | Severity | Mitigation |
|--------------|-------------|-------------------|----------|------------|
| Google Play Services | Location, device ID, usage | Google servers (warrant) | Critical | GrapheneOS, remove Google |
| Signal metadata | Who, when, how often, location | Signal servers (court order) | High | Burner number, no sync |
| Camera EXIF data | GPS, timestamp, device model | Shared photos | High | Disable location, strip metadata |
| Browser fingerprinting | Screen, fonts, timezone, canvas | Any website visited | Medium | Tor Browser, Tails |
| Hostname / device name | User-set identifiers | Network scans, router logs | Medium | Change to generic name |
| Misconfigured permissions | GPS, contacts, files | App developer servers | High | Deny all by default |

---

## Severity Ratings

| Vulnerability | Severity | Rationale |
|--------------|----------|-----------|
| Google Play Services | Critical | Complete device telemetry accessible via legal process |
| Signal metadata | High | Reveals social graph and communication patterns |
| Camera EXIF data | High | GPS-precision location embedded in shared files |
| Misconfigured permissions | High | Direct access to sensitive device resources |
| Browser fingerprinting | Medium | Persistent tracking without cookies |
| Hostname / device name | Medium | Low-entropy identifier, easily changed |

---

## Conclusion

Layer 4 is the most varied vulnerability layer because it encompasses the entire application ecosystem. Unlike Layer 1 (cellular) and Layer 2 (Wi-Fi), which involve fundamental network protocols, Layer 4 vulnerabilities are largely design choices — features that prioritize convenience over privacy.

GrapheneOS eliminates the single most critical Layer 4 vulnerability (Google Play Services). But it does not protect against Signal metadata, EXIF leakage, browser fingerprinting, or application permissions. These require active configuration and behavioral discipline.

The operational principle for Layer 4 is "least privilege in all domains." The device should have the minimum possible number of applications. Each application should have the minimum possible permissions. The browser should be Tor Browser. Photos should never be taken with Phone B. Signal should use a burner number. And no Google service — not even a logged-out YouTube view or Google search from the Vanadium browser — should ever touch Phone B.

Layer 4 leaks are subtle and cumulative. A browser fingerprint here, a Signal metadata record there, an EXIF tag in a shared photo — each leak individually may seem insignificant, but together they build a picture that an adversary can use to identify, locate, and correlate the user across devices.

---

[^1]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software," IEEE Symposium on Security and Privacy (IEEE S&P 2020). Documents data collected by Google Play Services and pre-installed Android components, including device identifiers, location, and usage patterns. https://ieeexplore.ieee.org/document/9152763

[^2]: GrapheneOS Project, "Features — Privacy and Security Enhancements," grapheneos.org/features. Documents the removal of Google Play Services and its tracking components from the GrapheneOS build. https://grapheneos.org/features

[^3]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Documents the metadata Signal servers observe and retain in response to legal process. https://signal.org/bigbrother/

[^4]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Describes Signal's response to a 2016 grand jury subpoena, listing the only data producible: account creation date and last connection date. https://signal.org/bigbrother/

[^5]: GrapheneOS Project, "Features," grapheneos.org/features. Notes the Camera app's option to suppress location metadata in captured images. https://grapheneos.org/features

[^6]: GrapheneOS Project, "Features," grapheneos.org/features. Describes Vanadium's hardening against fingerprinting while noting it does not achieve the uniform fingerprint pool of Tor Browser. https://grapheneos.org/features

[^7]: GrapheneOS Project, "Features," grapheneos.org/features. Documents developer-settings access to device hostname configuration. https://grapheneos.org/features

[^8]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software," IEEE S&P 2020. Catalogs over-privileged permission requests by pre-installed and third-party Android applications. https://ieeexplore.ieee.org/document/9152763

[^9]: GrapheneOS Project, "Features," grapheneos.org/features. Describes the enhanced permission model including per-app network access toggle, sensors toggle, storage scoping, and permission auto-reset. https://grapheneos.org/features
