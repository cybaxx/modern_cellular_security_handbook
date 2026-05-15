# Chapter 48: Empirical Testing and Validation

The claims in this handbook are not theoretical. Every assertion about MAC randomization failures, EID persistence, cellular timing advance precision, and Signal's metadata footprint is grounded in documented behavior — but documented by others, in conditions you have not personally verified. That gap matters. You should not trust this handbook on faith any more than you should trust a carrier's privacy policy on faith. You should test it.

This chapter gives you six reproducible experiments. Each one validates a specific claim made elsewhere in the handbook. Each one is runnable by a motivated researcher with equipment costing under $100 total. None require root access, carrier cooperation, or specialized legal authority. You are testing your own devices on your own network.

---

## Why Empirical Testing Matters

Most privacy guides describe how systems are documented to work. They cite specifications, court filings, and researcher papers. That is necessary but not sufficient. Specifications describe intended behavior. Implementations diverge from specifications. Firmware versions matter. Carrier configurations matter. The Android phone in your pocket may behave differently from the test device used in a 2021 paper.

**Reproducibility** in this context means: given the same equipment, the same preconditions, and the same procedure, you arrive at the same result. Where your result diverges, that divergence is itself a finding worth documenting.

The experiments below are structured consistently:

- **Equipment** — what you need and where to get it
- **Procedure** — numbered steps you can follow without interpretation
- **Expected findings** — what the handbook predicts you will observe
- **What failure looks like** — how to distinguish a failed test from a surprising result

Run these and document your findings. The open research questions in Ch44 depend on exactly this kind of field data.

---

## Experiment 1: Wi-Fi Probe Request Capture and MAC Analysis

The handbook claims in Ch12 that MAC randomization is inconsistently implemented and that probe request content can re-link a randomized MAC to a device even after rotation. This experiment tests both claims.

**Equipment**

- Linux laptop (any distribution)
- Wi-Fi adapter supporting monitor mode — Alfa AWUS036ACH (~$35) is reliable; the internal adapter on many ThinkPads also works
- `tshark` (command-line Wireshark) — `sudo apt install tshark` on Debian/Ubuntu
- Your own Android device with Wi-Fi enabled but not connected to any network

**Procedure**

1. Identify your wireless interface name: `ip link show`
2. Put the interface into monitor mode:
   ```
   sudo ip link set wlan0 down
   sudo iw dev wlan0 set type monitor
   sudo ip link set wlan0 up
   ```
3. Start capturing probe requests only:
   ```
   sudo tshark -i wlan0 -f "subtype probereq" -T fields \
     -e frame.time -e wlan.sa -e wlan.ssid \
     -e wlan_mgt.supported_rates -e wlan_mgt.vs.ie.oui \
     > probe_capture.txt
   ```
4. Set your Android device to airplane mode, then re-enable Wi-Fi only (no cellular). Wait 10 minutes. Walk the device near the antenna.
5. Disable Wi-Fi, wait 2 minutes, re-enable it. Repeat three times to observe MAC rotation behavior.
6. Open `probe_capture.txt` and sort by source MAC. Group consecutive probe requests from the same MAC and note the timestamps between the last appearance of one MAC and the first appearance of the next.

**Expected findings**

- On stock Android 10+, you will observe MAC rotation occurring at irregular intervals — typically between 5 and 30 minutes, not a fixed schedule.
- The probed SSID field will be empty on most modern Android versions (directed probes have been suppressed since Android 10), but the **Information Elements** — particularly supported rates, HT capabilities, and vendor-specific OUIs — will remain consistent across MAC rotations. Two consecutive MACs from the same device produce probe frames with identical IE fingerprints.
- This means an observer capturing continuously can re-link MACs across rotation events without any cooperation from the device.

**What failure looks like**

- If you see no probe requests at all, your adapter is not in monitor mode or is on the wrong channel. Try `sudo tshark -i wlan0 -f "subtype probereq"` without output redirection first to confirm traffic is being received.
- If all MACs are permanent (matching the device's hardware MAC in Settings > About Phone > Wi-Fi MAC), randomization is disabled. Check Settings > Network & Internet > Wi-Fi > [network] > Privacy.

---

## Experiment 2: eSIM EID Persistence Verification

The handbook claims in Ch19 that the eSIM EID is a permanent hardware identifier that persists across profile changes, carrier switches, and factory resets. This experiment confirms that behavior directly.

**Equipment**

- Android device with eSIM capability (Pixel 4 or later, most flagship phones from 2020+)
- USB cable and a computer with ADB installed (`sudo apt install adb` on Linux; Android SDK platform-tools on macOS/Windows)
- Developer Options enabled on the device (Settings > About Phone > tap Build Number 7 times)
- USB Debugging enabled (Settings > Developer Options > USB Debugging)

**Procedure**

1. Connect the device and confirm ADB sees it: `adb devices`
2. Read the current EID:
   ```
   adb shell service call econtroller 3 | grep -oP '(?<=\().*(?=\))'
   ```
   Or, if that returns nothing, try:
   ```
   adb shell getprop gsm.sim.eid
   ```
   Record the EID string.
3. Read the current ICCID (the SIM profile identifier, which changes when you switch profiles):
   ```
   adb shell getprop gsm.sim.ici
   ```
   Record it.
4. Add a second eSIM profile — use any carrier's eSIM QR code (Google Fi, Mint Mobile, or a travel eSIM like Airalo all work). Go through the provisioning flow completely.
5. After provisioning, repeat steps 2 and 3.

**Expected findings**

- The EID you recorded in step 2 is identical after provisioning. It does not change.
- The ICCID changes — it now reflects the new profile's identifier.
- This confirms what Ch19 documents: the EID is a hardware-level identifier assigned at manufacture. Switching carriers or profiles does not create a new hardware identity. Any system that has logged your EID retains the ability to re-identify the device regardless of what profile is installed.

**What failure looks like**

- If `getprop gsm.sim.eid` returns empty, the device either lacks eSIM or the property name differs by manufacturer. On Samsung devices, try `getprop ril.eid1`. On Pixels, the service call method is more reliable.
- If the EID appears to change, you are likely reading a different property. The EID is a 32-character hex string (16 bytes). Shorter strings are ICCIDs or IMEIs.

---

## Experiment 3: Signal Metadata Footprint Verification

The handbook notes in Ch27 that Signal's content encryption is strong but that network-layer metadata — which servers your device contacts, when, and how often — remains visible to a network observer. This experiment quantifies that footprint.

**Equipment**

- Signal installed on your phone, with at least one active conversation
- Wireshark or `tshark` running on the same Wi-Fi network as your phone (or on a laptop sharing a hotspot to the phone)
- Note: Signal uses certificate pinning. You cannot inspect message content via mitmproxy without a custom client build. This experiment tests network-layer metadata only.

**Procedure**

1. Start capturing on your network interface: `sudo tshark -i wlan0 -nn > signal_capture.txt`
2. Put your phone in airplane mode. Re-enable Wi-Fi only. Wait 60 seconds to let background traffic settle.
3. Send five Signal messages to one contact over 2 minutes. Note the exact times.
4. Receive two messages in return. Note the times.
5. Stop capture. Filter for your phone's IP address:
   ```
   tshark -r signal_capture.txt -nn "ip.addr == <your_phone_ip>"
   ```
6. Identify the destination IPs. Run `whois` against each unique destination.

**Expected findings**

- Signal's servers resolve to IP ranges owned by Amazon Web Services (Signal uses AWS infrastructure) and to `signal.org` domains. The 2016 Eastern District of Virginia grand jury subpoena to Signal (publicly released by the Open Whisper Systems legal team) confirmed that Signal's server-side logs contain only: account creation date, and the date of last connection. No message content, no contact graph, no message frequency. Your network capture will show AWS endpoints receiving encrypted traffic at times that correlate precisely with your send events — the timing is visible even though the content is not.
- DNS lookups for `chat.signal.org`, `storage.signal.org`, and `cdsi.signal.org` are typically visible in plaintext unless you are using encrypted DNS.
- Connection frequency is observable: a network-level adversary can determine that your device contacted Signal servers at specific times, inferring communication activity even with no content visibility.

**What failure looks like**

- If you see no Signal traffic at all, your phone may be on a different network than your capture interface. Confirm your phone's IP and the capture interface are on the same subnet.
- If you see traffic that appears to be Signal but resolves to non-AWS IPs, check for a VPN on the phone that is routing traffic differently.

---

## Experiment 4: Cellular Tower Association Logging

The handbook states in Ch8 that timing advance (TA) values give approximately 78-meter radial precision per measurement step, and that simultaneous visibility of three or more towers enables triangulation without GPS. This experiment lets you observe both.

**Equipment**

- Android phone (no root required)
- **Network Cell Info Lite** (free, Google Play) — this app reads values already exposed to unprivileged apps via the Android TelephonyManager API
- 30 minutes in a walkable area (urban works best; dense rural is fine)

**Procedure**

1. Install Network Cell Info Lite. Grant location permission (required to access cell data on Android 10+).
2. Open the app. Navigate to the **Map** tab. Enable logging.
3. Walk a known route for 30 minutes. The app logs Cell ID, LAC/TAC, signal strength (dBm), and timing advance for each tower association.
4. Export the log (CSV format). Open it in a spreadsheet.
5. For each row with a TA value greater than 0, compute the implied distance: `distance_meters = TA × 78.125`. (Each TA unit corresponds to one GSM symbol period ≈ 78.125 meters of two-way propagation, so TA × 78.125 ÷ 2 gives one-way distance.)
6. Cross-reference the Cell IDs against a public cell tower database (OpenCellID, Mozilla Location Services) to get tower coordinates. Plot your implied positions.

**Expected findings**

- In urban areas, you will observe 3–8 towers simultaneously with signal strength readings. This is sufficient for network-based triangulation without any GPS involvement.
- TA values, where visible (LTE exposes TA; UMTS exposes similar round-trip time values), will place you in an annular ring around the serving tower. The ring width is approximately 78 meters. Multiple simultaneous towers reduce the ambiguity significantly.
- Tower changes will occur frequently — every 30–90 seconds during a walk — leaving a continuous trail of cell association records at the carrier.

**What failure looks like**

- If TA values are consistently 0, your carrier or the specific towers in your area may not be exposing TA to the handset. This is a valid null result — document it. LTE TA visibility varies by carrier and network configuration.
- If you see only one tower at a time with no overlap, you are in a rural area with sparse coverage. Triangulation is still possible from historical records but requires more time-separated readings.

---

## Experiment 5: Faraday Bag Effectiveness Test

The handbook recommends Faraday enclosures in Ch33 for situations where a device must be silenced without powering off. This experiment tests whether a given bag actually works — because many commercial bags do not, especially at LTE frequencies above 2 GHz.

**Equipment**

- The Faraday bag you are considering using (or have purchased)
- Two phones: the device under test and a second phone to call it
- Optionally, a third device with Wi-Fi scanning capability (any phone running **WiFi Analyzer**)

**Procedure**

1. Place the device under test in the Faraday bag. Seal it fully according to the manufacturer's instructions.
2. From the second phone, call the device under test. Observe: does it ring? Does it go immediately to voicemail?
3. After 60 seconds, remove the device from the bag. Check whether it shows a missed call. (A missed call appearing confirms the device was isolated during the bag test; if the call rang through, isolation failed.)
4. Repeat the test with the device's Wi-Fi enabled. Use WiFi Analyzer on the third device to check whether the test phone's probe requests or SSID broadcast are visible while it is inside the bag.
5. Repeat with Bluetooth enabled. Use the third phone's Bluetooth scan to check for the test device.

**Expected findings**

- A quality Faraday bag (brands like Silent Pocket, Mission Darkness, or Disklabs) will send the call immediately to voicemail. The device will show a missed call on removal, confirming it received no signal while enclosed.
- Cheaper bags (under ~$15, often sold as "RFID blocking wallets") frequently attenuate signal at 800–900 MHz but fail at LTE bands above 1700 MHz. Your call may ring through on Band 66 (AWS-3, 1710–1755 MHz uplink) even if lower-band calls are blocked.
- Wi-Fi probe requests and Bluetooth advertisements will typically be blocked by a bag that passes the cellular test. Higher-frequency signals are easier to attenuate with the same shielding material.

**What failure looks like**

- If the call rings through (device audibly rings inside the bag), the bag failed. Document the bag brand and model, the carrier, and the band if you can determine it. This is a publishable null result.
- If you cannot get the missed-call indicator to appear even with a known-good bag, the carrier may be holding the call in a queue rather than sending it immediately to voicemail. Allow 90 seconds before concluding failure.

---

## Experiment 6: Data Broker Profile Audit

The handbook documents in Ch6 that data brokers aggregate accurate personal profiles from public records sources. This experiment puts a number on how many brokers have your accurate data and what that data contains.

**Equipment**

- A web browser
- Your own name, current address, and phone number (to verify accuracy of results)
- A notepad for recording findings

**Procedure**

1. Search your full name on each of the following brokers. Where a location field is offered, use your city and state:

   | Broker | URL |
   |---|---|
   | Spokeo | spokeo.com |
   | Radaris | radaris.com |
   | Whitepages | whitepages.com |
   | Intelius | intelius.com |
   | TruePeopleSearch | truepeoplesearch.com |
   | BeenVerified | beenverified.com |
   | FastPeopleSearch | fastpeoplesearch.com |
   | PeopleFinder | peoplefinder.com |
   | ZabaSearch | zabasearch.com |
   | Pipl | pipl.com (may require paid API access) |

2. For each result that appears to match you, record:
   - Current address accuracy (correct / partially correct / wrong)
   - Phone number accuracy
   - Relatives listed
   - Employer listed
   - Historical addresses included
   - Probable source (voter registration, property records, carrier lookup, social media scrape)

3. Note which brokers require payment to see full results — this is itself informative about their business model.

**Expected findings**

- Between 6 and 12 of these brokers will have a profile that accurately reflects your current address, at least one phone number, and 2–4 relatives' names. The handbook's claim is that this data is accurate enough to be operationally useful to an adversary who does not know your address.
- Historical addresses going back 5–10 years are common, sourced from property records and voter registration rolls.
- Employer information is less reliable but often present, typically sourced from LinkedIn scrapes or business registration filings.
- TruePeopleSearch and FastPeopleSearch provide the most complete free results; Intelius and BeenVerified gate full details behind payment but surface enough to confirm a match exists.

**What failure looks like**

- If no profiles appear for your name, you may have a common name causing your record to be de-prioritized in free results, or you may genuinely have low data broker exposure. Try adding your city to narrow results.
- If results are significantly inaccurate (wrong address, no relatives listed), you are a data point for Ch44's open question about data quality variance. Document and share.

---

## Recording and Sharing Results

Document each experiment with the following structure before sharing findings:

| Field | What to record |
|---|---|
| Experiment number | As numbered above |
| Date and location | City/region is sufficient; no street address |
| Device model and OS version | Pixel 8 / Android 14, etc. |
| Carrier | Carrier name and network generation (LTE, 5G NR) |
| Result | Match / No match / Partial / Null result |
| Deviation from expected | Describe specifically what differed |
| Raw data | Attached as separate file; redact your own identifiers before sharing |

Before sharing any capture file, run it through `tshark -r capture.pcap -T fields -e ip.src -e ip.dst | sort -u` to identify what IP addresses are present. Redact or summarize records containing your home IP, personal identifiers, or contact information from other parties captured incidentally.

The open research questions in Ch44 that these experiments most directly address:

- **Q3** (MAC randomization implementation consistency across Android OEMs) — Experiment 1
- **Q7** (EID exposure surface in eSIM provisioning flows) — Experiment 2
- **Q11** (network-layer metadata precision for Signal and similar apps) — Experiment 3
- **Q14** (TA precision variance by carrier and tower density) — Experiment 4
- **Q19** (Faraday shielding effectiveness by frequency band and bag construction) — Experiment 5
- **Q22** (data broker profile accuracy and sourcing by geography) — Experiment 6

Share findings in contexts appropriate to your threat model. Public forums (Reddit r/privacy, PrivacyGuides community) are appropriate for Experiments 1, 5, and 6. Experiments 2, 3, and 4 may produce output that is more sensitive; consider sharing through researcher networks or by filing directly with projects like GrapheneOS or the Privacy Guides documentation team. The research community benefits from your null results as much as from confirmations — the handbook is not infallible, and documented divergences from expected behavior are exactly the kind of signal needed to keep it accurate.
