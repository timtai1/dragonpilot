# 🐲 dragonpilot (Custom Fork)

This repository is a customized fork based on openpilot / dragonpilot (`v0.11.1`), tailored for Comma 3 / 3X devices. It focuses on manual steering wheel position control, full Traditional Chinese localization, CJK bitmap font atlas regeneration, and UI stability improvements.

---

## 🚀 Key Custom Features & Updates

### 1. 🎡 Manual Wheel Position Setting ("Wheel on Left or Right?")
* **Custom Settings Toggle**:
  * Added "Wheel on Left or Right?" toggle at the end of the dp settings menu.
  * Options: `Left` (default) and `Right`.
  * Description: *Wheel on left, such as US, TW. Wheel on right like HK, JP.*
* **Eliminated Dynamic Sensor Guesswork**:
  * Completely removed the dynamic facial/posture statistical filtering algorithm in `policy.py` that previously attempted to guess wheel position via the driver camera.
  * Directly reads the manual setting (`dp_dev_is_rhd`), avoiding misdetections caused by night driving, backlight, or driver posture.
  * Setting is permanently stored (`PERSISTENT`) and will never automatically change when crossing borders.

### 2. 🇹🇼 Full Traditional Chinese & Multilingual UI Support
* **Localization Engine Refactor**:
  * Rewrote `multilang.py` to directly parse and load `dragonpilot_{lang}.po` files at runtime without requiring precompiled `.mo` binaries.
* **100% Traditional Chinese Translation**:
  * Completed full translation coverage for `dragonpilot_zh-CHT.po`.
  * Resolved the issue where dp settings remained in English even when system language was set to Traditional Chinese.

### 3. 🔤 Bitmap Font Atlas Baking (Resolves '?' Glyph Rendering)
* **Font Processing Tooling**:
  * Updated `selfdrive/assets/fonts/process.py` to automatically harvest all Chinese characters from `.po` files.
* **Regenerated CJK Bitmap Font Atlases**:
  * Re-baked Raylib font atlases (`OpFont-*.fnt` / `OpFont-*.png`) on the Comma device.
  * Completely resolved missing Chinese glyphs rendering as question marks (`?`).

### 4. ⚡ UI Stability Fixes (Crash Prevention)
* **Fixed Menu Crashes**:
  * Resolved `ValueError` caused by string-to-int conversion on boolean parameters (`int("False")`), which previously caused the UI to crash back to the comma boot logo when opening dp settings.

### 5. 🔄 Fast Hot-Reload Deployment Workflow
* **No 10-15 Minute Device Reboot**:
  * Established hot-reload deployment for pure Python, translation, and asset changes.
  * UI restarts and reloads changes via `selfdrive.ui` in ~1 second.
