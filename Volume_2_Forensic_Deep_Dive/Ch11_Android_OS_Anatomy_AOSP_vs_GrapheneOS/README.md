# Chapter 11: Android OS Anatomy — AOSP vs. GrapheneOS

## Introduction

The operating system is the foundation of all privacy and security properties on a mobile device. It controls which applications can access which data, how hardware resources are isolated, what information leaves the device, and who has authority over the system's behavior. In the two-phone strategy, Phone B is almost always an Android device running a de-Googled custom OS. Understanding what this means at the architectural level — what is removed, what is hardened, and what remains exposed — is essential to evaluating the strategy's actual security.

This chapter provides a forensic analysis of the Android operating system architecture across three configurations: the Android Open Source Project (AOSP) as the baseline, Google's production Android (with Google Mobile Services), and GrapheneOS as the most hardened privacy-focused implementation. It covers the kernel, the hardware abstraction layer, the runtime, the application framework, the cellular baseband interface, and the firmware attack surface that no OS modification can fully address.

---

## Part 1: The Android Software Stack

### 1.1 Architectural Layers

Android is a layered operating system built on a Linux kernel.[^1] Each layer abstracts the layer below and provides services to the layer above. The forensic significance of each layer depends on what data it handles and what security boundaries it enforces.

**Layer 1 — Linux Kernel:** The kernel manages hardware resources — CPU scheduling, memory management, process isolation, file systems, and device drivers. Android uses a long-term-support (LTS) Linux kernel with additional Android-specific patches: wake locks (power management), binder (inter-process communication), ashmem (shared memory), and paranoid networking (restricting network access by UID). The kernel enforces the fundamental security boundary between applications through Linux user IDs (UIDs) and discretionary access control (DAC). Every app runs as a separate Linux user, isolated by the kernel's process isolation.[^1]

**Layer 2 — Hardware Abstraction Layer (HAL):** The HAL provides a standardized interface between the Android framework and hardware-specific drivers. Camera, sensors, audio, GPS, Wi-Fi, Bluetooth, and the cellular modem are all accessed through HAL modules. The HAL is vendor-provided and proprietary for most components. The forensic implication: the HAL is closed-source on every Android device, including those running GrapheneOS. The user cannot audit what the camera HAL, sensor HAL, or GNSS HAL actually does.

**Layer 3 — Android Runtime (ART):** ART compiles Android applications from bytecode (DEX) to native machine code at install time. It manages garbage collection, memory allocation, and thread scheduling for Java/Kotlin applications. ART enforces the application sandbox through the UID-based isolation inherited from the kernel.[^1]

**Layer 4 — Application Framework:** This is the set of Java APIs that applications use to interact with the system: the activity manager (app lifecycle), content providers (data sharing), location manager, notification manager, package manager, and the permission system. The framework is where most privacy-relevant controls exist — permission grants, location access, camera access, and network policy.[^1]

**Layer 5 — System Applications:** Pre-installed applications that provide core phone functionality: the dialer, SMS messenger, contacts, camera, email client, and — in Google's Android — Google Play Services, Google Play Store, Google Services Framework, and Google Backup Transport.

### 1.2 The Binder IPC Mechanism

Binder is Android's inter-process communication (IPC) system and is arguably the most security-critical component in the entire stack. All communication between applications, between applications and the system server, and between the system server and hardware services passes through Binder.[^1]

Binder operates through a kernel driver (`/dev/binder`). When an application makes a system call — requesting location, accessing the camera, querying contacts — the request is serialized into a Binder transaction and delivered to the target service. The kernel mediates this transaction, checking that the calling process has permission to communicate with the target.

**Forensic significance:** Binder transactions are logged in the kernel's buffer and can be dumped via `dmesg` or extracted through forensic tools. A forensic analyst with physical access to a device can reconstruct a timeline of which applications accessed which system services, including location queries, camera activations, and contact database reads.

### 1.3 The Permission System

Android's permission system has evolved significantly across versions. Understanding its current state is critical for evaluating what a de-Googled OS can and cannot control.

**Install-time permissions (pre-Android 6):** Permissions were granted at install time. Users had to accept all requested permissions or not install the app. This model made privacy protection nearly impossible.[^1]

**Runtime permissions (Android 6+):** Permissions are granted while the app is running. The user can deny individual permissions. Apps must request permissions at the point of use, and the user can revoke them at any time. This is the baseline for all modern Android versions, including AOSP and GrapheneOS.[^1]

**Permission auto-reset (Android 11+):** If an app is not used for several months, Android automatically revokes its runtime permissions. This reduces the exposure of rarely-used applications.[^1]

**Permission revocations (AOSP baseline):** AOSP allows users to grant, deny, or revoke most dangerous permissions (location, camera, microphone, SMS, contacts). However, AOSP does not include Google's advanced permission features:

- No Privacy Dashboard (visibility into which apps accessed what, when)
- No permission-based app hibernation (Google Play Protect's auto-revoke)
- No granular scoped storage enforcement (varies by OEM implementation)

**GrapheneOS permission enhancements:**[^2]

- **Storage Scopes:** Rather than granting full storage access, GrapheneOS allows users to grant access to specific directories or files. This prevents apps from scanning the entire filesystem.
- **Contact Scopes:** Similar scoped access for contacts — apps receive only the specific contact information they request, not the entire contact database.
- **Calendar and Call Log Scopes:** Same scoping model for calendar events and call logs.
- **Network and Sensors Permissions:** GrapheneOS adds new permission types not present in AOSP: `NETWORK` (control which apps have network access at all), `SENSORS` (control which apps can access non-location sensors like accelerometer, gyroscope, magnetometer), and `NFC` (control NFC access).
- **Permission Hub:** A centralized interface showing every permission grant across all apps, with the ability to revoke and audit.
- **Expired Permissions:** Permissions can be set to auto-expire after a configurable time period.

---

## Part 2: AOSP vs. Google Android

### 2.1 What AOSP Provides

The Android Open Source Project is the core operating system that Google releases under an open-source license.[^1] It includes:

- The Linux kernel with Android patches
- The HAL interfaces (but not the proprietary HAL implementations)
- ART and the core libraries
- The application framework (activity manager, package manager, permission system, notification manager)
- Basic system applications (dialer, SMS, browser, camera, calendar, calculator)
- The security model (UID isolation, SELinux policies, permission system, verified boot)

AOSP is functionally complete as a mobile operating system. It runs applications, connects to cellular networks, accesses Wi-Fi, manages permissions, and provides the standard Android user experience — minus Google's proprietary services.

### 2.2 What Google Adds

Google's production Android includes everything in AOSP plus a layer of proprietary components collectively known as Google Mobile Services (GMS). These components are what transform AOSP from a privacy-neutral OS into a data collection platform.

**Google Play Services (GMS Core):** This is the single most privacy-relevant component in Google's Android. It runs as a system application with the highest possible privilege level (UID `com.google.android.gms`).[^3] It holds permissions that no user application can obtain:

- `ACCESS_FINE_LOCATION` and `ACCESS_BACKGROUND_LOCATION` (continuous location access)
- `READ_EXTERNAL_STORAGE` and `WRITE_EXTERNAL_STORAGE` (full filesystem access)
- `GET_ACCOUNTS` (access to all registered Google accounts)
- `READ_CONTACTS` and `WRITE_CONTACTS` (full contact database access)
- `RECORD_AUDIO` and `CAMERA` (sensor access)
- `INTERNET` with no firewall restrictions
- `BIND_ACCESSIBILITY_SERVICE` (ability to observe all UI interactions)

Play Services runs as a persistent background process. It cannot be disabled by the user without root access. It communicates with Google servers over encrypted channels that the user cannot inspect or block without modifying the device's trust store.[^3]

The data Play Services collects:[^3]

| Data Type | Collection Frequency | Forensic Value |
|-----------|---------------------|----------------|
| Wi-Fi BSSID scan results | Every 60 seconds | Geolocation via Google's BSSID database (accuracy within 10-20 meters) |
| Cell tower IDs (serving + neighboring) | Every 60 seconds | Location via tower triangulation, even with GPS disabled |
| GPS coordinates | On demand (apps requesting location) | Precise location history |
| Bluetooth beacon scans | Every 60 seconds | Additional geolocation signal |
| Accelerometer/gyroscope samples | Continuous (for step counting, activity detection) | Activity recognition, movement patterns |
| Application usage statistics | Periodic | App install list, usage frequency, behavioral profiling |
| Network connectivity status | On change | Connection type, carrier, IP address range |
| Device identifiers (Advertising ID, Firebase ID, GCM token) | Persistent | Cross-app tracking correlation |

**Firebase Cloud Messaging (FCM):** FCM is Google's push notification service. Every application that uses push notifications registers with FCM and receives a unique token. FCM maintains a persistent connection to Google's servers, providing a continuous metadata channel even when no messages are being sent. The FCM connection reveals the device's IP address, the list of installed applications (each registered app has a unique channel), and the timing of message delivery.[^3]

**Google Play Store:** The Play Store collects app installation and update history, search queries, payment information, and device compatibility data. It also enforces Google's application verification (Play Protect), which scans installed applications and reports results to Google.[^4]

**Google Backup Transport:** Android's built-in backup system, when using Google's transport, uploads application data, SMS messages, call history, device settings, Wi-Fi passwords, and — critically — location history to Google's servers. This data is encrypted with the device's screen lock key for some categories, but the metadata (what was backed up, when, from which device) is visible to Google.[^1]

**Google Location History (formerly Google Latitude):** When enabled, this service records the device's precise location at regular intervals and stores it in the user's Google account.[^3] The data is accessible through Google Maps Timeline and is retained indefinitely. Even if the user disables Location History, Play Services' Wi-Fi and cell tower scanning continues to collect location data for "network quality" purposes.

### 2.3 The Tracking Infrastructure

Google's Android tracking infrastructure is not a single service but a coordinated system of services that collectively provide comprehensive surveillance capability:[^3]


> *See the figure generated below.*


Each service feeds data into Google's user profiling infrastructure. The location service sends BSSID scans. Firebase sends app usage events. AdMob sends ad interaction data. SafetyNet sends device integrity attestations. Google correlates all of these through the user's Google account (cross-service authentication) or through the Advertising ID (cross-app tracking without account login).[^4]

### 2.4 What Cannot Be Removed

Even on a de-Googled AOSP build, certain tracking-adjacent components remain because they are part of the hardware vendor's firmware, not the Android OS:

- **The Wi-Fi chipset firmware (Broadcom/Qualcomm/MediaTek):** This firmware scans for access points and communicates with the Wi-Fi HAL. Even if the Android framework never requests a scan, the firmware may perform background scans for roaming purposes.
- **The cellular baseband firmware:** This is a completely independent real-time operating system running on the modem processor. It communicates with the cellular network independently of the Android OS.
- **The sensor hub firmware:** A low-power microcontroller that processes sensor data (accelerometer, gyroscope, barometer) even when the main application processor is suspended.
- **The boot ROM:** This is mask-programmed into the SoC and cannot be modified. It contains the device's initial trust anchor and determines what code can be loaded at boot.

---

## Part 3: GrapheneOS Architecture

### 3.1 Design Philosophy

GrapheneOS is a privacy and security hardening fork of AOSP.[^2] Unlike other custom ROMs that focus on adding features or removing Google services, GrapheneOS is designed around a specific engineering philosophy: reduce attack surface, harden existing security boundaries, and eliminate unnecessary trust relationships.

GrapheneOS does not start from the premise that Google is malicious. It starts from the premise that every additional code path, every network service, every background process, and every privileged component is a potential vulnerability. The goal is to minimize the trusted computing base — the set of code that must be correct for the system's security properties to hold.

### 3.2 What GrapheneOS Changes

**Baseband Isolation:**

In AOSP, the cellular baseband processor communicates with the application processor through shared memory (SHM) or a serial interface (HSI). The baseband driver in the Linux kernel has access to kernel memory. A vulnerability in the baseband driver — or a malicious baseband firmware — could compromise the entire operating system.

GrapheneOS isolates the baseband by:[^2]
- Moving the baseband driver into a separate, sandboxed process (`gpusermem` and `qrtr` namespaces on Pixel devices)
- Restricting the baseband's access to kernel memory through IOMMU configuration
- Preventing the baseband from initiating DMA to application processor memory
- Placing the RIL (Radio Interface Layer) daemon in a strict SELinux sandbox

**Result:** A compromised baseband cannot directly read application processor memory. However, the baseband can still send arbitrary data to the cellular network, including location and device identifiers that the Android OS cannot intercept.

**Hardened Memory Allocator:**

The standard Android memory allocator (Scudo) is a general-purpose allocator that balances performance and security. GrapheneOS replaces it with a hardened allocator that:[^2]
- Adds guard pages between allocations (detects buffer overflows)
- Randomizes allocation addresses (reduces exploitation reliability)
- Zeroes freed memory immediately (prevents data leakage between processes)
- Validates metadata integrity on every allocation and deallocation

**Result:** Heap-based memory corruption vulnerabilities — the most common class of Android exploits — are significantly harder to exploit. This reduces the risk of both remote and local privilege escalation.

**Kernel Hardening:**

GrapheneOS applies a comprehensive set of kernel hardening patches that are not present in AOSP:[^2]

- Restricts user-space access to kernel pointers through `dmesg_restrict` and `kptr_restrict`
- Enables strict kernel stack buffer overflow detection (stack canaries on all functions)
- Enables kernel page table isolation (KPTI) on all supported devices
- Enables the arm64 address space layout randomization (ASLR) for all kernel modules
- Disables all unnecessary kernel features and drivers (reducing attack surface)
- Compiles the kernel with Control Flow Integrity (CFI) to prevent indirect call hijacking

**Verified Boot with User-Configurable AVB:**

AOSP implements Android Verified Boot (AVB), which verifies the integrity of the boot chain (bootloader, boot image, system partition, vendor partition) before allowing the device to boot. GrapheneOS extends this by:[^2]

- Allowing the user to set a custom verified boot key (not relying on Google's keys)
- Requiring the bootloader to be re-locked after installation (preventing unauthorized OS modifications)
- Implementing rollback protection (preventing an attacker from flashing an older, vulnerable OS version)

**Network and Sensors Permissions:**

As described in Part 1, GrapheneOS adds several permission types that do not exist in AOSP:[^2]

- `NETWORK` permission: Controls which applications can access the network at all. This is a fundamental security boundary that AOSP does not enforce at the permission level.
- `SENSORS` permission: Controls access to non-location sensors (accelerometer, gyroscope, magnetometer, barometer, proximity). These sensors can be used for side-channel attacks, activity recognition, and device fingerprinting.
- `NFC` permission: Controls NFC access separately from other radios.

**Forensic significance:** The `NETWORK` permission, in particular, is a powerful tool for compartmentalizing applications. An app that cannot reach the network cannot exfiltrate data, regardless of any other permissions it holds.

**Application Sandbox Strengthening:**

GrapheneOS hardens the standard Android application sandbox:[^2]

- Enables kernel-based exploit mitigations for all applications (not just system apps)
- Prevents applications from using hardware acceleration for untrusted content (reduces GPU attack surface)
- Restricts application access to `/proc` and `/sys` (reduces information leakage for device fingerprinting)
- Blocks non-SDK API access (applications cannot use hidden Android APIs to bypass permission controls)

**Network Stack Hardening:**[^2]

- Enables DNS over TLS system-wide (when supported by the network)
- Blocks legacy VPN protocols (PPTP, L2TP/IPsec with weak ciphers)
- Restricts ICMP and other network protocols that could be used for side-channel attacks
- Implements MAC address randomization per network (prevents Wi-Fi tracking across networks)

### 3.3 What GrapheneOS Does Not Change

GrapheneOS operates within the constraints of the existing hardware. Several critical components are outside its control:

**The Baseband Processor (Modem):**

The baseband is a separate computer running its own operating system (typically ThreadX, Nucleus RTOS, or a Qualcomm proprietary RTOS). It has its own CPU, memory, network stack, and radio interface. The baseband must communicate with the cellular network independently to register, maintain connectivity, and handle calls and data.

While GrapheneOS isolates the baseband from the application processor, it cannot:[^2]

- Prevent the baseband from transmitting the IMEI to the cellular network (required for network registration)
- Prevent the baseband from reporting location (timing advance, cell ID) to the network
- Control what the baseband firmware does internally (the firmware is proprietary and the baseband's internal state is inaccessible to the application processor)
- Prevent the baseband from leaking data through RF side channels

**The Boot ROM:**

The boot ROM is the first code executed when the device powers on. It is mask-programmed into the SoC during manufacturing and cannot be modified. The boot ROM contains the device's hardware root of trust — the public keys used to verify the bootloader's signature. A vulnerability in the boot ROM is unpatcheable. Devices with known boot ROM vulnerabilities (such as Qualcomm's LAF or Samsung's Exynos boot ROM bugs) cannot be fully secured regardless of OS.

**The Wi-Fi and Bluetooth Firmware:**

Like the baseband, the Wi-Fi and Bluetooth controllers run their own firmware. This firmware handles the low-level radio protocols (802.11, Bluetooth LE) and communicates with the main processor through shared memory or SDIO. GrapheneOS can restrict the host driver interface but cannot audit or modify the firmware running on the radio controllers.

**Secure Element / TEE (Trusted Execution Environment):**

Modern Android devices include a Trusted Execution Environment — typically ARM TrustZone on Qualcomm devices. The TEE runs a separate secure OS (QSEE on Qualcomm, Trusty on Pixel devices) that handles cryptographic operations, keystore management, and DRM. The TEE has access to memory that the application processor cannot read. A vulnerability in the TEE can leak cryptographic keys (including full-disk encryption keys) without the OS being able to detect the compromise.

**Hardware Identifiers:**

GrapheneOS cannot change the device's IMEI, MEID, serial number, or the MAC addresses burned into the Wi-Fi and Bluetooth radios. These identifiers are written to one-time-programmable (OTP) fuses or stored in reserved memory regions that the application processor cannot modify.[^2]

### 3.4 AOSP vs. GrapheneOS Comparison Table

| Component | AOSP | Google Android | GrapheneOS |
|-----------|------|----------------|------------|
| Google Play Services | Not included | Included, privileged | Not included |
| Baseband isolation | Standard driver | Standard driver | IOMMU-restricted, sandboxed |
| Memory allocator | Scudo | Scudo | Hardened allocator |
| Kernel hardening | Baseline LTS | Baseline LTS + Google patches | Full hardening (CFI, KPTI, ASLR) |
| Network permission | Not available | Not available | Available |
| Sensors permission | Not available | Not available | Available |
| Verified boot | AVB with Google keys | AVB with Google keys | AVB with user keys |
| MAC randomization | Per-network (optional) | Per-network (optional) | Per-network (default enabled) |
| DNS encryption | Not configured | DoH with Google DNS | DoT (configurable) |
| Storage scopes | Not available | Not available | Available |
| Contact scopes | Not available | Not available | Available |
| Auto-expire permissions | Not available | Not available | Available |
| Background app management | Standard | Standard + Play Protect | Enhanced |
| Cellular baseband visibility | No | No | No (hardware limitation) |
| Boot ROM patching | No | No | No (hardware limitation) |

---

## Part 4: Forensic Implications for the Two-Phone Strategy

### 4.1 The De-Googled Phone B

For the two-phone strategy, Phone B running GrapheneOS (or another hardened AOSP derivative) provides meaningful privacy improvements over a standard Android device:[^2]

- Google Play Services and all GMS components are absent. The continuous location scanning, BSSID reporting, Firebase messaging, and advertising ID collection do not occur.
- The hardened application sandbox reduces the risk of a malicious app escaping isolation and accessing data from other applications.
- The additional permission controls (network, sensors, storage scopes) allow finer-grained control over what applications can do.
- MAC address randomization by default reduces Wi-Fi tracking across networks.

However, these improvements operate within the hardware constraints described in Section 3.3. The baseband continues to transmit identifiers. The Wi-Fi chipset firmware continues to scan. The TEE continues to operate outside the OS's visibility.

### 4.2 Remaining Google Infrastructure

Even on GrapheneOS, some Google-adjacent infrastructure may remain depending on the device:

- **Device drivers and HALs:** Pixel devices (GrapheneOS's primary supported hardware) include Google-written drivers for the camera, sensors, and other hardware. These drivers are proprietary and are not audited by the GrapheneOS project.
- **Firmware updates:** Pixel devices receive firmware updates (baseband, Wi-Fi, bootloader, TEE) from Google. These updates are signed by Google and are applied through Google's update infrastructure. GrapheneOS cannot independently verify the contents of these firmware blobs.
- **Initial device configuration:** The device's IMEI, serial number, and hardware attestation keys are set during manufacturing and are registered with Google's device databases. A forensic analyst can query Google's databases to link a device's IMEI to its sales channel, warranty status, and (if the user ever signed into a Google account on any device) the user's identity.

### 4.3 Application-Level Risk

The OS is only one component of the privacy stack. Applications running on the OS can leak data through multiple channels that the OS cannot fully control:[^4]

- **Network-level fingerprinting:** Application TLS libraries send Client Hello messages that include the list of supported ciphers, TLS extensions, and elliptic curves. This handshake fingerprint is unique enough to identify the application and often the OS version.
- **Third-party SDKs:** Many applications include third-party analytics, advertising, and crash-reporting SDKs (Google Firebase, Google AdMob, AppsFlyer, Adjust). These SDKs send device identifiers, IP addresses, and usage data to their servers. On GrapheneOS, without Google Play Services, Firebase SDKs cannot use the Advertising ID or FCM token, but they can fall back to device fingerprinting using hardware and network characteristics.
- **Behavioral profiling:** Application usage patterns — which apps are used, when, for how long — are visible at the network level through traffic analysis. Signal usage produces a distinct traffic pattern regardless of the OS.

### 4.4 The GrapheneOS Trade-off

GrapheneOS provides stronger security guarantees than AOSP or Google Android, but these guarantees come with trade-offs:[^2]

**Loss of convenience:** Many applications depend on Google Play Services for push notifications, location, maps, and payment APIs. Banking apps, ride-sharing apps, and some messaging apps may not function correctly or at all without Play Services. Signal works without Play Services (using its own WebSocket-based push mechanism), but many other apps do not.

**Smaller device selection:** GrapheneOS supports only Google Pixel devices (Pixel 4a and newer). This limits the user's choice of hardware and means the device's supply chain is controlled by Google — the same company whose services the OS is designed to avoid.

**No reduction in legal exposure:** GrapheneOS does not protect against legal compulsion. A court order served on the user to unlock the device, or a subpoena served on the cellular carrier for tower logs, bypasses all OS-level protections equally.[^5]

**No protection against physical access:** GrapheneOS's verified boot and encryption provide strong protection against unauthorized OS modification and data extraction. But a sufficiently equipped adversary with physical access — border agents, police, intelligence operatives — can use forensic tools (Cellebrite, GrayKey) to attempt extraction. The device's security depends on the strength of the user's passphrase and the absence of unpatched boot ROM vulnerabilities.

---

## Part 5: Architecture Diagrams

### 5.1 Android Software Stack — AOSP Baseline


> *See the figure generated below.*


### 5.2 Google Android Additions


> *See the figure generated below.*


### 5.3 GrapheneOS Security Boundaries


> *See the figure generated below.*


---

## Chapter Summary

| Topic | Key Finding |
|-------|-------------|
| AOSP baseline | Provides core Android functionality without Google services; privacy-neutral but not hardened |
| Google Android additions | Play Services, FCM, Play Store, and backup create a comprehensive data collection infrastructure operating with system-level privileges |
| Tracking architecture | Coordinated multi-service system (location, analytics, ads, device integrity) feeding into Google's user profiling pipeline |
| GrapheneOS hardening | Baseband isolation, hardened memory allocator, kernel hardening, additional permissions (network, sensors, NFC), storage/contact scopes, auto-expiring permissions, verified boot with user keys |
| What GrapheneOS cannot fix | Boot ROM (unpatcheable), baseband firmware (proprietary, unverifiable), Wi-Fi/Bluetooth firmware, TEE/TrustZone, hardware identifiers (IMEI, MAC) |
| Two-phone implications | GrapheneOS on Phone B eliminates Google tracking but does not eliminate cellular carrier, Wi-Fi chipset, or ISP-level metadata collection |
| Key trade-off | Stronger security isolation vs. reduced app compatibility and limited hardware selection (Pixel only) |

---

[^1]: Android Open Source Project, "Platform Architecture" (source.android.com), https://source.android.com/docs/core/architecture. Documents the Android software stack layers, the Linux kernel base, ART, the Binder IPC mechanism, the permission system, and the evolution from install-time to runtime permissions.

[^2]: GrapheneOS Project, "Features" (grapheneos.org), https://grapheneos.org/features. Primary documentation for GrapheneOS security hardening including baseband isolation, hardened memory allocator, kernel patches, Network/Sensors permissions, Storage Scopes, Contact Scopes, auto-expiring permissions, MAC randomization defaults, and hardware identifier constraints.

[^3]: Google LLC, "Google Play Services" and related API documentation (developers.google.com). Describes the privileges held by Google Play Services, the Firebase Cloud Messaging infrastructure, and the Location History data collection model.

[^4]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software," IEEE Symposium on Security and Privacy (2020). Documented that pre-installed GMS components and third-party SDKs collect device identifiers, location, and behavioral data with system-level privileges on Android devices.

[^5]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court held that compelled government acquisition of historical cellular location data constitutes a Fourth Amendment search, confirming that OS-level protections do not affect a carrier's obligation to produce records in response to lawful process.
