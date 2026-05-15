# Chapter 34: Phone B — The Private Wi-Fi Hub

## The Role of Phone B

Phone B is the device that matters. Everything sensitive happens here. Signal conversations with sources, attorneys, and trusted contacts. Secure email. Research into sensitive topics. All of the communications that must never be exposed to surveillance, seizure, or subpoena.

The design of Phone B reflects this purpose. Unlike Phone A, which is designed to be surrendered, Phone B is designed to remain hidden. It is never seen by border agents, never connected to your home network, never linked to your identity. It is the device that must survive every search, every seizure, and every investigation.

The philosophy behind Phone B is that cellular networks are inherently hostile. The cellular baseband is a proprietary black box running closed firmware over which you have no visibility. It communicates with towers that log your location, your device identifiers, and your call metadata.[^1] The solution is to eliminate the cellular attack surface entirely.

## Device: Google Pixel with GrapheneOS

The choice of hardware and operating system for Phone B is critical. It must be a device that you can fully control, with an operating system that minimizes telemetry, and a hardware platform that supports disabling the cellular radio without compromise.

**Google Pixel** is the recommended hardware for a specific reason: it is the only device family that supports GrapheneOS with full hardware security features. The Pixel's Titan security chip, verified boot, and strong isolation between the baseband and the application processor all contribute to a platform that can be locked down effectively.

Older Pixel models (Pixel 4 through Pixel 7) are ideal because they are available used at reasonable prices and have mature GrapheneOS support. Newer Pixels work as well but cost more. The Pixel hardware does not need to be fast or have a good camera. In fact, the camera should ideally be disabled.

**GrapheneOS** is the operating system of choice because it is the most secure and privacy-respecting Android-based OS available. It removes Google Play Services by default, provides Google Play Sandbox as an optional install, and implements significant security hardening including hardened memory allocator, MAC address randomization, and network permission toggle per app.[^2]

The key GrapheneOS features for this use case:

- **Cellular radio can be permanently disabled.** This is not just turning on airplane mode. GrapheneOS allows you to disable the cellular modem in a way that persists across reboots and cannot be accidentally re-enabled.

- **Network permissions per app.** You can control which apps have internet access, preventing data leaks from applications that should not be phoning home.

- **MAC address randomization by default.** The device presents a randomized MAC address to each Wi-Fi network, preventing long-term tracking via MAC address.[^3]

- **No Google Play Services.** The primary source of telemetry and tracking on Android is removed. The device does not report to Google.

## Cellular Disabled Permanently

This is the single most important configuration choice for Phone B. The cellular radio must be disabled at the hardware level, not just put into airplane mode.

**Why this matters.** The cellular baseband is a separate processor running its own operating system. It has direct memory access (DMA) to the main processor on most devices, meaning a compromised baseband can read data from the main OS. The baseband firmware is proprietary and cannot be audited. It communicates with cell towers that log IMSI, IMEI, location, and call metadata.[^4]

By disabling the cellular radio, you eliminate this entire attack surface. Phone B becomes a Wi-Fi-only device. It never registers with a tower, never transmits an IMSI, and never generates CDRs (Call Detail Records). From the cellular network's perspective, Phone B does not exist.

**How to disable it.** In GrapheneOS, go to Settings > Network & Internet > SIMs and remove any SIM card. Then go to Settings > Network & Internet > Mobile network and disable the mobile data toggle. For complete disablement, use the GrapheneOS radio toggle in the quick settings panel or use an ADB command to fully power down the modem. Verify the disablement by checking that the device shows no signal and that the IMEI is not broadcast.[^5]

**What you lose.** Without cellular, Phone B cannot make or receive standard phone calls or SMS. This is intentional. Communication on Phone B happens exclusively over data channels: Signal, Wire, or other encrypted messengers over Wi-Fi + VPN. The inability to make cellular calls is a feature, not a bug. It prevents the device from generating cellular metadata and eliminates the risk of accidental carrier registration.

## Wi-Fi: Public Wi-Fi Only

Phone B never connects to a network you control. It never connects to your home Wi-Fi, your work Wi-Fi, or the Wi-Fi at any location that can be linked to your identity.

**Acceptable networks.** Coffee shops. Public libraries. Hotel lobbies. Airport terminals. Coworking spaces. Retail stores with free Wi-Fi. Any network that is open to the public and where you pay in cash and do not register your identity.

**Why not your own Wi-Fi.** Connecting to your home Wi-Fi would link your home's IP address to Phone B. Your ISP logs that assignment. If an investigator obtains those logs, your home address is linked to Phone B. That single connection destroys the entire compartmentalization strategy.

**MAC randomization.** Before connecting to any public Wi-Fi, ensure MAC randomization is enabled. GrapheneOS enables this by default, but you should verify.[^6] Each connection should use a different randomized MAC address so that even the coffee shop's Wi-Fi logs cannot track your device across visits.

**Never save networks.** Do not save public Wi-Fi networks as known networks. Each session should be a fresh connection. Saving networks creates a history that can be extracted from the device if it is ever seized.

## VPN: Mullvad, Always On

A VPN is not optional for Phone B. Every connection to the internet must go through the VPN.

**Mullvad** is the recommended VPN provider because it can be paid with cash, requires no email address to sign up, and has a strong no-logging policy that has been tested in court. Other VPNs with similar anonymity properties may also work, but Mullvad's cash payment option is difficult to beat.

**Cash payment.** Send cash in an envelope to Mullvad's office. No credit card, no PayPal, no cryptocurrency that can be traced back to an exchange where you verified your identity. The cash payment generates an account number that you use to activate the service. No name, no email, no identifying information.

**Always on.** The VPN must be configured to connect automatically on any network and to block all traffic if the VPN disconnects. GrapheneOS supports this through its built-in VPN configuration. The kill switch prevents IP leaks if the VPN connection drops unexpectedly.

**Split tunneling disabled.** Do not use split tunneling. All traffic goes through the VPN. No exceptions.

## Tor: Orbot for High-Risk Communications

For the highest-risk communications, adding Tor as an additional layer provides defense against VPN compromise and traffic analysis.

**Orbot** is the Tor proxy for Android. It can be configured as a proxy that all apps route through, or as a VPN-mode app that tunnels all device traffic through Tor.

**When to use Tor.** If you are communicating with a source in a highly monitored environment, if you are researching topics that could attract attention, or if you have reason to believe your VPN provider is compromised, add Tor. The combination of VPN + Tor provides defense in depth. The VPN sees only that you are connecting to Tor, not your destination. Tor sees only the VPN exit IP, not your real IP.

**When not to use Tor.** Tor adds significant latency and can trigger suspicion on networks that monitor for Tor usage. For routine communications over Signal, the VPN alone is sufficient. Reserve Tor for the highest-sensitivity operations.

## Signal with a Burner Number

Signal is the primary communication tool on Phone B. It provides end-to-end encryption, forward secrecy, and minimal metadata retention. But Signal still requires a phone number for registration, and that phone number is the link between your Signal identity and the carrier network.

**Burner number.** The number used to register Signal on Phone B must never be linked to your identity. Options include:

- A prepaid SIM purchased with cash, used only for Signal registration, then discarded. The SIM does not need to maintain service after registration. Signal will continue working over Wi-Fi even without an active SIM.

- A VoIP number from a provider that accepts anonymous payment. Skype numbers, Google Voice (if accessible), or similar services can work, but must be obtained anonymously.

- A temporary number service that provides a real phone number for SMS verification. These services vary in reliability and legal status. Research the service carefully before using it.

**Never the same account as Phone A.** Do not use the same Signal account on both phones. If Signal sees both devices registered to the same account, it knows they belong to the same person. This creates a data point that can be revealed through legal process.

## Photos Disabled, Location Services Off

**Photos disabled.** The camera on Phone B should be disabled if possible, or at minimum never used. Cameras embed EXIF metadata in photos including GPS coordinates (if location services are on), device serial number, camera sensor fingerprint, and timestamp.[^7] A photo taken on Phone B and shared could identify the device and its location.

On GrapheneOS, the camera can be blocked at the permission level. You can deny the camera permission to all apps. For maximum security, physically cover the camera lens or use a device with no camera.

**Location services off.** All location services must be disabled. This includes GPS, Wi-Fi scanning, and Bluetooth scanning. GrapheneOS provides granular location permission controls. Verify with ADB that no app has location access and that the GPS hardware is not being polled.

Use the following verification commands:

```
adb shell dumpsys location | grep "Location Providers"
adb shell settings get global wifi_scan_always_enabled
adb shell settings get global bluetooth_scan_always_enabled
```

All three should show location providers as disabled and scanning as not always enabled.

## Mitigated Architecture Reference

The mitigated architecture from the forensic analysis defines these revised requirements for Phone B:

| Original | Revised Requirement | Rationale |
|---|---|---|
| Moto G / Pixel (cellular capable) | Pixel + GrapheneOS, cellular radio disabled (Wi-Fi only) | Eliminates baseband tracking |
| Residential ISP Wi-Fi | Never connected to home or work Wi-Fi | Prevents ISP identity link |
| Public Wi-Fi (coffee shop) | Public Wi-Fi only, with MAC randomization + VPN + Tor | Breaks Wi-Fi geolocation |
| Standard Signal setup | Signal with burner phone number (VoIP or prepaid SIM used once) | Prevents Signal metadata linking to identity |
| Used anywhere | Never within 1km of home or work | Prevents physical correlation |
| Carried freely | Faraday bag when traveling to/from use locations | Prevents passive scanning |

Phone B is the crown jewel of the two-phone strategy. Protect it accordingly.

[^1]: Every time a phone registers with a cell tower, it transmits its IMSI and IMEI to the network; see 3GPP TS 22.261, "Service Requirements for the 5G System," and GSMA PRD TS.06, "IMEI Allocation and Approval Guidelines."
[^2]: GrapheneOS documentation, grapheneos.org — describes per-network MAC randomization, hardened memory allocator, and network permission controls implemented in the OS.
[^3]: GrapheneOS per-network MAC randomization is documented at grapheneos.org; see also Jeremy Martin et al., "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *PoPETs* 2017, on the limits of randomization on standard Android.
[^4]: The IMEI is transmitted to the network even before a SIM is inserted; see 3GPP TS 22.261 and GSMA PRD TS.06, "IMEI Allocation and Approval Guidelines."
[^5]: IMEI transmission and baseband tracking are addressed in GSMA PRD TS.06, "IMEI Allocation and Approval Guidelines" (GSMA).
[^6]: MAC address randomization failures on Android are documented in Jeremy Martin et al., "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *PoPETs* 2017; GrapheneOS addresses many of these failures per grapheneos.org documentation.
[^7]: EXIF metadata including GPS coordinates and device identifiers is embedded in photos by default on most devices; Cellebrite UFED and similar forensic tools extract this metadata from seized devices (Cellebrite UFED capabilities documentation).
