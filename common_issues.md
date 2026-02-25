# Maslow 4 Common Issues & Troubleshooting Guide

## Overview
The Maslow 4 is a belt-driven CNC router that uses four retractable belts anchored to the corners of a work surface to position the router sled. This guide covers the most common technical issues encountered by users.

---

## 1. Connection and Network Setup

### Cannot Connect to Maslow 4 WiFi
- The Maslow 4 broadcasts its own WiFi network named **"maslow"**.
- Default WiFi password: **12345678**
- Once connected, access the web interface at **192.168.0.1** in your browser.
- If the interface doesn't load, try a different browser or device.
- Restart the Maslow 4 to reset the WiFi connection.

### Connecting Maslow 4 to Your Home Network
- In the web interface, go to the **Config** section.
- Enter your home WiFi network name (SSID) and password.
- Save settings and restart the machine.
- After connecting to your home network, the Maslow 4 may be accessible at a different IP address assigned by your router.
- The machine will still broadcast the "maslow" hotspot as a fallback if it cannot reach the configured network.

### Web Interface Not Loading
- Ensure you are connected to the correct network.
- Clear browser cache or try incognito/private mode.
- Try accessing http://192.168.0.1 (with http, not https).
- Check if the machine's status LED indicators are on and the controller board is powered.

---

## 2. Belt and Sled Issues

### Belts Not Retracting at Power-On
- At startup, the Maslow 4 **fully retracts all four belts** to find its home/zero position.
- If a belt does not retract, check that it is not snagged, tangled, or obstructed.
- Verify that each belt motor LED is illuminated green (indicating proper connection).
- Check cable connections between the motor and the controller board.
- If a specific motor is unresponsive, try swapping motor cables to isolate whether the problem is the motor or the port.

### Sled Falls or Drops During Use
- Ensure all four belts are properly tensioned and attached to the sled.
- Check that the belt anchors are securely fastened to the frame corners.
- Verify belt direction and mounting — belts must pull in the correct direction for the sled to stay in place.
- Recalibrate the machine if the sled loses position during operation.

### Belt Slippage or Jumping
- Confirm that belt ends are properly seated in the sled attachment points.
- Belts should be free to rotate in the XY plane but held firmly in the Z direction.
- Inspect the belt spools for smooth retraction and extension.
- Check that belt tension is adequate — neither too loose nor overly tight.

### One or More Belt Motors Not Responding
- Verify that the motor LED for that axis is illuminated.
- Check all cable connections between motors and the controller board.
- Try swapping motor connectors to determine if the issue is the motor or the controller port.
- Inspect the motor cable for damage or loose pins.

---

## 3. Calibration Issues

### Calibration Not Completing or Looping
- Access the calibration routine from **Actions** or **Calibration** in the web interface.
- Ensure the calibration grid is within recommended bounds and the machine is not obstructed.
- Recent firmware (v1.17+) auto-detects grid orientation and terminates unrecoverable loops after 10 tries.
- If calibration hangs, restart the machine and try again.
- Take a video of the calibration process to share with the community if the problem persists.

### Inaccurate Cuts After Calibration
- Re-run calibration if the machine has been moved or the frame has shifted.
- Ensure anchor measurements are correct — inaccurate anchor position data is the most common cause of poor cut accuracy.
- Firmware v1.17+ discards obviously incorrect anchor data to improve reliability.
- Verify that the work surface (spoilboard) is flat and the frame is square.
- Check belt tension is consistent across all four belts.

### Machine Loses Position Mid-Job
- Power interruptions cause the Maslow 4 to lose its position (belt lengths are not stored in non-volatile memory in all firmware versions).
- Always complete the homing/retract sequence before starting a new job after a power cycle.
- Inspect for belt slippage or any physical obstruction that may have moved the sled.

### Calibration Grid Orientation Issues
- Confirm that the orientation of the calibration grid matches the physical orientation of the machine (vertical vs. horizontal).
- If the grid is rotated or mirrored, cuts will be incorrect. Check the **orientation setting** in the Config menu.

---

## 4. Firmware Issues

### How to Update Firmware
- Connect to the Maslow 4 web interface.
- Navigate to the **Firmware Update** section.
- Upload the new **firmware.bin**, **index.html.gz**, and **maslow.yaml** files.
- Always back up your **maslow.yaml** configuration file before updating.
- For updates from firmware versions before 1.0 to versions after 1.0, a **USB cable** must be used instead of the web interface.

### Firmware Update Fails or Machine Becomes Unresponsive
- If the web-based update fails, use a USB cable to flash firmware directly.
- Download the latest firmware files from the [official GitHub releases](https://github.com/MaslowCNC/Maslow_4/releases).
- Use the USB flashing procedure described in the official documentation.

### Lost Configuration After Update
- Firmware updates may overwrite **maslow.yaml**.
- Always back up maslow.yaml before updating.
- Re-enter anchor positions and calibration data if they are lost.

### Firmware Versions and What Changed
- **v1.17**: Added automatic WiFi reconnection, improved anchor data validation, auto-detects calibration grid orientation, stops calibration after 10 failed attempts.
- Always check the [GitHub releases page](https://github.com/MaslowCNC/Maslow_4/releases) for the latest changes and bugfixes.

---

## 5. Cutting and Movement Problems

### Machine Moves Erratically
- Re-calibrate the machine.
- Verify belt connections and anchor positions.
- Check for loose or damaged cables.
- Inspect belt paths for snags or obstructions.

### Z-Axis (Router Depth) Not Moving Correctly
- Check the Z-axis cable connection to the controller.
- Verify the Z-axis motor is functioning.
- Inspect for physical obstructions along the Z-axis travel.
- In the web interface, test Z-axis movement manually using the jog controls.

### Cuts Are Not Square or Dimensions Are Wrong
- Perform a full recalibration.
- Double-check anchor measurements (the distance from each anchor to the center of the work area).
- Ensure the work piece is secured and not moving during the cut.
- Verify the toolpath and G-code use correct units (mm vs. inches) matching the machine configuration.

### Router Bit Plunges Too Deep or Doesn't Reach Material
- Check the Z-axis zero position setting (tool length offset).
- Verify the Z-axis motor and coupling are secure.
- Ensure the router collet is properly tightened and the bit is not slipping.

---

## 6. Software and G-Code Issues

### Generating G-Code for Maslow 4
- The Maslow 4 runs **FluidNC** firmware and accepts standard G-code.
- Common CAM tools: **Estlcam**, **Fusion 360**, **FreeCAD**, **Carbide Create**.
- Use a post-processor appropriate for a generic 3-axis router.
- The Maslow 4 uses millimeters by default; verify your CAM output matches.

### Uploading G-Code Jobs
- G-code files can be uploaded through the web interface.
- Access the **Files** or **Jobs** section of the web interface to upload and run files.
- Maximum recommended file size varies; split large jobs if necessary.

### Job Stops Mid-Cut
- Check for WiFi connection drops (newer firmware auto-reconnects).
- Ensure the browser tab running the web interface remains open and active.
- Check power supply stability.
- Review G-code for any commands the firmware may not support.

---

## 7. Hardware and Assembly

### Frame and Anchor Setup
- The Maslow 4 works with frames from approximately **4×8 feet** (standard sheet stock) and larger.
- Anchors should be positioned at the four corners, as far apart as possible for best accuracy.
- The official recommended frame dimensions and anchor positions are detailed in the [Quick Start Guide](https://maslowcnc.github.io/Maslow_4/QuickStart.html).

### Router Compatibility
- The Maslow 4 sled is designed to hold a standard trim router (e.g., Makita RT0701, DeWalt DWP611).
- Check the official documentation for compatible router models and mounting adapters.

### Dust and Chip Management
- Use a dust shoe or vacuum attachment to manage chips during cutting.
- Keep the belts and pulleys clear of sawdust accumulation.

---

## 8. Resources and Community

- **Official Documentation**: https://maslowcnc.github.io/Maslow_4/
- **Quick Start Guide**: https://maslowcnc.github.io/Maslow_4/QuickStart.html
- **Community Forums**: https://forums.maslowcnc.com/
- **Troubleshooting Thread**: https://forums.maslowcnc.com/t/the-big-bad-m4-troubleshooting-problems-solutions-thread/21000
- **GitHub (Firmware & Releases)**: https://github.com/MaslowCNC/Maslow_4/releases
- **User Guide**: https://www.maslowcnc.com/user-guide
