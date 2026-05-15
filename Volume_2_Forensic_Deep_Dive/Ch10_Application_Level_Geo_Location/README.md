# Chapter 10: Application-Level Geo-Location

## Introduction

Application-level geo-location operates at a fundamentally different layer than cellular or Wi-Fi tracking. Where cellular tracking is a function of the carrier network and Wi-Fi tracking is a function of the 802.11 protocol, application-level geo-location is a function of the software running on the device — the operating system services, the installed applications, and the user's interaction with them.

Even on a de-Googled custom operating system, application-level geo-location remains a significant attack surface. The phone leaks location through every sensor, every API call, and every passive scan that applications can access. Understanding these mechanisms is essential to building a complete threat model.

## Google Play Services and Firebase Cloud Messaging

On a standard Android phone — one with Google Play Services installed — Google collects location data through multiple parallel mechanisms.

### Google Location Services (GLS)

GLS is the most comprehensive collection system on Android. Every 60 seconds, the device scans for nearby Wi-Fi access points, cell towers, and Bluetooth beacons, tags them with the device's GPS coordinates, and reports the mapping to Google's servers.[^1] This feeds Google's Wi-Fi geolocation database, but it also creates a historical record of exactly where the device has been. A standard Android phone with Google apps installed reports its location approximately 1,440 times per day.

Beyond foreground reporting, Google Location Services operates as a persistent background process. Even when no application is actively requesting location, GLS continues scanning and reporting. This data is retained by Google indefinitely and is available to law enforcement through a warrant, a National Security Letter, or a subpoena to Google's legal compliance team.[^2]

### Google Maps and Google Search

When Google Maps is opened, the device transmits precise GPS coordinates along with street view context, search queries, and interaction data. Google Search logs each query with the device's approximate location derived from IP, Wi-Fi, or GPS.[^1] This creates a searchable timeline of where the user was and what they were looking for at each location.

### Android Device Manager

Android Device Manager transmits the last known location of the device even when GPS is off, using Wi-Fi and cell tower triangulation. This transmission occurs every 4 hours by default and is designed to enable remote device finding. It also creates a forensic record of device location at regular intervals.

### The "De-Googled" Escape

Installing GrapheneOS (or another de-Googled operating system) without Google Play Services removes GLS entirely. The phone does not report location to Google.[^3] This is effective for the OS-level tracking vectors.

However, there is a persistent forensic hole: the Wi-Fi chipset firmware continues to scan for BSSIDs independently of the OS. If a user ever installs an application that requests location permission — a weather app, a camera app, a navigation app — that application can read the chipset's scan results. On GrapheneOS, the permission system prevents unauthorized access, but the user must be diligent about granting location permissions only to applications that genuinely need them.

## Apple Find My Network

While the two-phone strategy typically does not involve Apple devices, the Find My network is relevant for comparison and for scenarios where an iPhone is present alongside the strategy's devices.

### Offline Finding

The Find My network operates even when the iPhone has no internet connection. The iPhone broadcasts a rotating public encryption key via Bluetooth Low Energy. Any nearby Apple device — any iPhone, iPad, or Mac running recent software — that has an internet connection picks up this beacon and relays it, along with its own GPS location, to Apple's servers. The owner can then query Apple's servers from another device and see the approximate location of their lost phone.

The forensic implication is profound: even a powered-off, air-gapped iPhone can be tracked through strangers' devices. The only defense is faraday isolation.

### Significant Locations and Frequent Locations

iOS maintains an internal cache of Significant Locations — places where the user has spent more than 10 minutes. This cache is encrypted but stored on the device. Forensic extraction tools like Cellebrite and GrayKey can access this cache from a locked iPhone. The cache reveals GPS coordinates, timestamps, visit duration, and in many cases, labeled locations such as "Home" and "Work."

Frequent Locations extends this by storing routine destinations: the gym visited every Tuesday evening, the grocery store visited every Saturday morning, the friend's house visited irregularly. This data is direct evidence of identity and routine.

## In-Application Tracking

Individual applications collect and transmit location data through their own code paths, often without the user's awareness and often through third-party libraries that share data with advertising networks and data brokers.[^4]

### Weather Applications

Weather apps that request "precise location" access GPS coordinates every time they refresh. The location data is sent to the app's own servers and to advertising networks integrated via SDKs — typically Google AdMob, Facebook Audience Network, or similar. The ad networks store this data and use it for behavioral profiling. A user checking the weather daily is providing a daily GPS fix to multiple data brokers.[^5]

### Camera Applications and EXIF Metadata

Standard camera applications embed GPS coordinates in the EXIF metadata of every photograph taken, unless location permissions are specifically revoked. The EXIF data includes latitude, longitude, altitude, timestamp, camera make and model, and device identifier.

The forensic risk extends beyond the device. A user takes a photograph with Phone B (the private device) and shares it via Signal to a contact. That contact later uploads the photograph to social media, email, or a cloud service. Law enforcement obtains the photograph through a subpoena or warrant. The EXIF data reveals the GPS coordinates of the user's home, the date and time the photograph was taken, and the camera make and model — matching Phone B. The compartmentalization collapses through a single photograph.

Mitigation requires multiple layers: disable camera location permissions entirely, use an application like Scrambled EXIF or the Metadata Anonymisation Toolkit (MAT2) to strip metadata before sharing any file, and avoid taking photographs with a device that is intended to be private.

### Web Browsers

Browsers expose location through three mechanisms. First, IP geolocation — any website the user visits can look up the approximate geographic location of the device's IP address. Second, the HTML5 Geolocation API — if the user grants permission, the website receives precise GPS coordinates. Third, and most insidiously, JavaScript code on websites can scan for visible Wi-Fi access points using APIs exposed by some browsers and operating systems, and then query geolocation databases to determine the device's location.

Even on privacy-focused browsers with tracker blocking, the HTML5 Geolocation API is accessible to any site the user explicitly grants permission to. On less scrupulous browsers, location may be available without explicit permission.

### Social Media Geotagging

Social media applications represent a distinct forensic category because they actively encourage location sharing as a feature. Twitter, Instagram, Facebook, and similar platforms allow users to attach precise GPS coordinates to posts, either explicitly through check-ins or implicitly through geotagged content. Even when the user does not intentionally geotag a post, the platform can infer location from IP address, Wi-Fi BSSIDs, Bluetooth beacons, or EXIF metadata in uploaded photographs.

The forensic value of social media location data is magnified by its public nature. A user's geotagged posts over months or years provide a comprehensive location history that requires no warrant to access. Law enforcement can scrape publicly available social media data to determine a target's home, workplace, social circles, and routine movements. This data is often admissible as evidence because it was voluntarily published.

### Advertising ID and Location Correlation

Both Android and iOS expose an advertising identifier — the Google Advertising ID on Android and the Identifier for Advertisers (IDFA) on iOS. These identifiers are designed for ad tracking and are accessible to all installed applications. When an application shares location data with an ad network, the ad network associates the location with the advertising ID. The ad network can then correlate location data across multiple applications used by the same device.[^6]

The forensic implication is that an investigator who obtains the advertising ID can query ad network databases to retrieve the device's location history across all applications that use that ad network. This provides a unified timeline that combines data from weather apps, maps, games, shopping apps, and any other application that integrates the ad network's SDK. The advertising ID may also be shared with data brokers who combine it with offline data sources including credit card transactions, loyalty programs, and public records.[^7]

### Google Location History / Timeline

Google's Location History (accessible to users as Google Timeline) stores a continuous record of device location independent of individual application usage.[^1] When enabled, the device logs position at frequent intervals — every few minutes when the device is moving, less frequently when stationary. The data includes GPS coordinates, estimated accuracy, activity detection (walking, driving, cycling, stationary), and place identification.

This data is stored in the user's Google account and is accessible through a warrant or subpoena to Google.[^2] Even if the user has deleted the Google Maps application, Location History continues collecting if the setting is enabled in the system-level Google account settings. The data retention period is configurable by the user (3 months, 18 months, or until manually deleted), but auto-deleted data may persist in backups for additional periods.

## Sensor-Based Location Inference

Modern smartphones contain an array of sensors that, individually, do not reveal location but, collectively, enable location inference. This is sometimes called "sensor fusion" and is an active area of forensic research.

### Accelerometer and Gyroscope

The accelerometer and gyroscope measure device motion and orientation. These sensors do not require location permissions to access in most operating systems. An application can read accelerometer data to determine when the user is walking, running, driving, or stationary. By analyzing the pattern of accelerometer readings, the application can infer the user's transportation mode and, in some cases, the specific route taken based on turn patterns.

### Magnetometer

The magnetometer (compass) measures magnetic field strength. It can detect the device's orientation relative to magnetic north. In urban environments, the magnetometer also detects magnetic anomalies caused by nearby structures, power lines, and metal objects. These anomalies can serve as location fingerprints — a device at a specific location will observe a specific magnetic field signature.

### Barometer

The barometer measures atmospheric pressure, which correlates directly with altitude. A barometer reading determines the device's floor within a building. Combined with Wi-Fi BSSID mapping, this provides three-dimensional location: which building and which floor.

### Ambient Light and Proximity Sensors

The ambient light sensor measures illumination levels, which can indicate whether the device is indoors or outdoors. The proximity sensor detects when the device is near the user's face (during a call). These readings, while low-resolution, contribute to activity classification models that infer location context.

## Cloud Synchronization as a Location Vector

Many applications synchronize data to cloud services in the background. This synchronization includes metadata that reveals location implicitly. For example, a note-taking application that syncs via iCloud or Google Drive transmits the timestamp and originating IP address of each sync event, even if the note content contains no location data. A calendar application syncs event locations. A photo backup service uploads images with EXIF GPS coordinates.

These cloud sync events are logged by the service provider and are accessible through legal process.[^2] The cumulative effect is that every cloud-synced application creates a timestamped record of device activity that can be correlated with location.

## IP-Based Geolocation at the Application Level

When an application connects to a remote server, the server receives the device's public IP address. IP geolocation databases map IP addresses to geographic regions with varying precision. In urban areas, IP geolocation can identify the correct city and often the correct neighborhood. Some IP geolocation providers claim accuracy within a few hundred meters for mobile IP addresses in dense urban environments.

Applications that periodically "phone home" — checking for updates, reporting usage statistics, fetching configuration — transmit the device's IP address with each connection. A log of these connections, correlated with IP geolocation data, produces a timeline of the device's approximate location across time.

## Wi-Fi and Bluetooth Geolocation Databases

This tracking vector is among the most underappreciated in mobile forensics. Multiple organizations maintain comprehensive databases that map Wi-Fi BSSIDs (access point MAC addresses) and Bluetooth MAC addresses to precise GPS coordinates.

### The Major Databases

Google Location Services is the largest, populated by every Android device with Google Play Services.[^1] Every 60 seconds, each device scans for nearby Wi-Fi access points and Bluetooth beacons, records their BSSIDs, tags them with the device's GPS location, and reports the mapping to Google. As of 2026, this database contains hundreds of billions of BSSID-to-GPS mappings covering the vast majority of the world's populated areas.

Apple Location Service operates identically using iPhone scans. Skyhook Wireless, now part of Loc-Aid, has been mapping Wi-Fi access points since the early 2000s and maintains agreements with OEMs including Samsung and LG for data collection. Mozilla Location Service, though no longer active, contributed significant data during its operation. HERE Location Suite (formerly Nokia Here) aggregates location data from automotive and mobile OEMs.

### The Forensic Attack

An investigator can determine where your phone has been without ever accessing its GPS. The process is straightforward. First, the investigator obtains your phone's observed BSSID list — either through a forensic extraction of the device's Wi-Fi scan cache, by capturing probe requests and association frames over the air, or by seizing a router that maintained a neighbor list. Second, they extract the BSSIDs of access points the device detected. Third, they query a geolocation API such as Google's Geolocation API with those BSSIDs. The API returns estimated GPS coordinates with 10 to 20 meter accuracy.[^1]

### The Passive Variant

Even without accessing the device, the attack works in reverse. A user walks past a coffee shop whose Wi-Fi access point is mapped in Google's database. Later, an adversary with a Wi-Fi sniffer captures the user's probe requests, which include the BSSID of the coffee shop's access point. The adversary looks up the BSSID in Google's database and learns the user was at that coffee shop at the captured time.[^8]

## Mitigation Strategies

Against Google Play Services, the only complete mitigation is to use a de-Googled operating system like GrapheneOS that removes Google Play Services entirely.[^3] Against Apple Find My, the only mitigation is to not carry Apple devices.

Against in-app tracking, deny location permissions to all applications. Use the operating system's privacy dashboard to verify that no application has background location access. For camera applications specifically, disable location permissions entirely and use an EXIF stripping tool before sharing any photograph.

Against Wi-Fi geolocation databases, disable both "Wi-Fi scanning" and "Bluetooth scanning" in the operating system's location settings. On custom operating systems, verify via `adb shell dumpsys` that these settings actually disable the underlying radio scanning. Use MAC randomization for probe requests. Accept the fundamental limitation that passing through the range of any public access point that is in a geolocation database leaves a forensic trace.

Against sensor-based inference, remove or restrict sensor permissions for all applications that do not explicitly need them. On GrapheneOS, the Sensors toggle in Quick Settings disables all non-system sensors globally.[^3] For high-risk scenarios, a device with physical sensor kill switches (such as the Purism Librem 5 or modified smartphones) provides hardware-level assurance.

Against the Google advertising ID, reset the identifier regularly or disable it entirely on custom operating systems. On GrapheneOS, the advertising ID is not available to applications by default.[^3]

Against Google Location History / Timeline, verify that the setting is disabled in the system-level Google account settings, not just in the Google Maps application. On a de-Googled operating system, this setting does not exist, which is the most complete mitigation.

Against cloud synchronization as a location vector, minimize the number of applications with cloud sync enabled. For each synced application, understand what metadata is transmitted and to whom. Consider using offline-only applications that store data locally and do not communicate with remote servers.

The comprehensive mitigation strategy for application-level geo-location is to reduce the number of applications that have network access, remove location permissions from all applications that do not absolutely require them, use a de-Googled operating system as the foundation, and treat every application as a potential location surveillance vector. In the high-risk threat model, the device should be configured so that no application can access location data, sensor data, or network metadata that reveals the user's physical position.

---

[^1]: Google LLC, "Google Location Services" (Google APIs documentation), https://developers.google.com/maps/documentation/geolocation/overview. Describes how Android devices scan nearby BSSIDs and cell towers, tag them with GPS coordinates, and report to Google's servers to populate the Wi-Fi geolocation database.

[^2]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court held that the government's warrantless acquisition of historical cell-site location information constitutes a Fourth Amendment search, recognizing that such records are retained by providers and can reveal detailed location history accessible through legal process.

[^3]: GrapheneOS Project, "Features" (grapheneos.org documentation), https://grapheneos.org/features. Documents the removal of Google Play Services, the Sensors permission toggle, and the absence of the Google Advertising ID on GrapheneOS.

[^4]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software" (IEEE Symposium on Security and Privacy, 2020). Found that pre-installed and third-party SDK components in Android apps collect and transmit location data and device identifiers, often without adequate user disclosure.

[^5]: New York Times Investigative Team, "Twelve Million Phones, One Dataset, Zero Privacy," The New York Times (December 19, 2019). Documented how location data brokers aggregate GPS fixes from apps such as weather applications and sell precise movement histories to third parties.

[^6]: Motherboard (Vice), "How the U.S. Military Buys Location Data from Ordinary Apps," Vice/Motherboard (January 22, 2020). Reported that advertising-network location data tied to device advertising IDs is purchased by government and military contractors, demonstrating cross-app location aggregation at scale.

[^7]: Zubair Shafiq et al., "A First Look at Third-Party Internet Tracking in Mobile Apps" and related work on location data broker ecosystems. Academic work documenting how advertising IDs are combined with offline data sources to build user profiles.

[^8]: Mathy Vanhoef and Frank Piessens, "Why MAC Address Randomization is Not Enough: An Analysis of Wi-Fi Network Discovery Mechanisms," Proceedings of the 11th ACM Asia Conference on Computer and Communications Security (AsiaCCS), 2016. Demonstrated that probe requests and BSSID observations can be used to track devices and infer location history even when MAC randomization is partially implemented.
