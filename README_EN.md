# 🐲 dragonpilot (Custom Fork)

This repository is a customized fork based on openpilot / dragonpilot (`v0.11.1`), tailored for Comma 3 / 3X devices. It focuses on offline GPS country-based steering wheel initialization with permanent manual locking, full Traditional Chinese localization, CJK bitmap font atlas regeneration, and UI stability improvements.

---

## 🚀 Key Custom Features & Updates

### 1. 🛰️ Steering Wheel Position: Offline GPS Country Auto-Initialization + Permanent Manual Lock (Featured)
* **First-Time GPS Country Auto-Detection**:
  * When freshly installed and **not yet manually modified** by the user, once the Comma device acquires its initial GPS fix (`hasFix`), it instantly compares coordinates against an ultra-lightweight offline geographic boundary map.
  * In **Right-Hand Drive (RHD) countries/territories** (Japan, Hong Kong, Macau, UK, Ireland, Australia, New Zealand, Singapore, Thailand, Malaysia, Indonesia, South Africa, etc.), the system **automatically presets the wheel to Right (`Right`)**.
  * In **Left-Hand Drive (LHD) countries** (Taiwan, USA, Canada, Continental Europe, Mainland China, etc.), the system **automatically presets the wheel to Left (`Left`)**.
  * 100% offline calculation with zero network dependencies or privacy risks; works with no SIM card required.
* **Permanent Manual Override Lock**:
  * As soon as the user touches and selects `Left` or `Right` in the dp settings menu, the manual flag is permanently saved (`dp_dev_wheel_position_manually_set = True`).
  * **From that point on, GPS will NEVER override the setting again**, regardless of international travel, tunnels, or GPS signal jitter.
* **Eliminated Dynamic Sensor Misdetection**:
  * The original `policy.py` algorithm that constantly guessed wheel position using the driver camera was completely stripped out, preventing driver monitoring instability caused by backlight, night driving, or body posture.

### 2. 🎡 Manual Wheel Position Toggle ("Wheel on Left or Right?")
* **Custom Settings Toggle**:
  * Added "Wheel on Left or Right?" toggle at the end of the dp settings menu.
  * Options: `Left` (default) and `Right`.
  * Description: *Wheel on left, such as US, TW. Wheel on right like HK, JP.*
  * Settings are persistently stored (`PERSISTENT`) across reboots.

### 3. 🍃 Gentle Acceleration & Early Smooth Deceleration
* **Gentle Acceleration Setting**:
  * Added "Gentle Acceleration" setting under dp Longitudinal menu.
  * Four configurable maximum launch acceleration limits: `1.0`, `1.2`, `1.4`, `1.6` m/s² (Default is **`1.2` m/s²**).
  * Eliminates harsh takeoff punch (stock is 1.6 m/s²), providing silky smooth acceleration from a stop.
* **Early Smooth Braking (2x Distance, 1/2 Deceleration)**:
  * Eliminates abrupt late braking when approaching stopped or slow-moving lead vehicles at red lights.
  * Initiates gentle deceleration at twice the original distance, halving the required deceleration to ~1.25 m/s² (compared to stock 2.5 m/s²).

### 4. 🇹🇼 Full Traditional Chinese & Multilingual UI Support
* **Localization Engine Refactor**:
  * Rewrote `multilang.py` to directly parse and load `dragonpilot_{lang}.po` files at runtime without requiring precompiled `.mo` binaries.
* **100% Traditional Chinese Translation**:
  * Completed full translation coverage for `dragonpilot_zh-CHT.po`.
  * Resolved the issue where dp settings remained in English even when system language was set to Traditional Chinese.

### 5. 🔤 Bitmap Font Atlas Baking (Resolves '?' Glyph Rendering)
* **Font Processing Tooling**:
  * Updated `selfdrive/assets/fonts/process.py` to automatically harvest all Chinese characters from `.po` files.
* **Regenerated CJK Bitmap Font Atlases**:
  * Re-baked Raylib font atlases (`OpFont-*.fnt` / `OpFont-*.png`) on the Comma device.
  * Completely resolved missing Chinese glyphs rendering as question marks (`?`).

### 6. ⚡ UI Stability Fixes (Crash Prevention)
* **Fixed Menu Crashes**:
  * Resolved `ValueError` caused by string-to-int conversion on boolean parameters (`int("False")`), which previously caused the UI to crash back to the comma boot logo when opening dp settings.

### 7. 🔄 Fast Hot-Reload Deployment Workflow
* **No 10-15 Minute Device Reboot**:
  * Established hot-reload deployment for pure Python, translation, and asset changes.
  * UI restarts and reloads changes via `selfdrive.ui` in ~1 second.
