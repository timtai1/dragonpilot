# Dragonpilot Development & Device Management Guide

## Overview
This repository contains a custom fork of `dragonpilot` (based on openpilot 0.11.1) tailored for the user's Comma 3 / 3X device.

## Device Connection Profile
- **Target Device**: Comma 3 / 3X
- **IP Address**: `<COMMA_IP>` (Configured in local agent rules; subject to local Wi-Fi DHCP assignment)
- **SSH User**: `comma`
- **SSH Private Key**: `<SSH_KEY_PATH>` (Stored in local SSH config / agent rules)
- **SSH Base Command**:
  ```bash
  ssh -i <SSH_KEY_PATH> -o StrictHostKeyChecking=no comma@<COMMA_IP>
  ```
- **Remote Openpilot Path**: `/data/openpilot`
- **Remote Python venv**: `/usr/local/venv/bin/python3`
- **Local Repository**: `<LOCAL_REPO_PATH>`
- **Active Git Branch**: `0.11.1`
- **GitHub Origin**: `https://github.com/<GITHUB_USER>/dragonpilot.git`

> [!IMPORTANT]
> **Privacy & Security Notice**:
> Do NOT hardcode personal credentials, private key paths, or internal IP addresses in git-tracked repository files (e.g. `GEMINI.md`, `README.md`, or source code).
> All actual connection parameters are maintained strictly within local uncommitted agent rules (`~/.agents/rules/comma-dragonpilot.md`).

## Fallback Procedure When Device is Unreachable
If SSH commands return `Connection timed out`, `Host is down`, or `No route to host`:
1. Do not repeat failed connections.
2. Prompt the user to verify that the Comma device is powered on and connected to local Wi-Fi.
3. If the IP address has changed via DHCP, request the new IP from the user and update connection commands.

---

## Key Technical Architectures & Customizations

### 1. Manual Wheel Position ("Wheel on Left or Right?")
- **Parameter**: `dp_dev_is_rhd` (Boolean, `PERSISTENT`)
  - `Left` (`0` / `False`): Left-hand drive (LHD, default for TW, US, etc.)
  - `Right` (`1` / `True`): Right-hand drive (RHD, for JP, HK, UK, etc.)
- **Configuration Files**:
  - `dragonpilot/settings/min-feat.dev.z-wheel-position.py`
  - `dragonpilot/settings/min-feat.dev.z-wheel-position.yaml`
  - Registered in `common/params_keys.h` (`dp_dev_is_rhd`, `BOOL`, `PERSISTENT`)
- **Driver Monitoring Logic**:
  - In `selfdrive/monitoring/policy.py`, the dynamic camera/facial feature statistical model for guessing wheel position was removed.
  - The driver monitor now purely uses `self.wheel_on_right = self.params.get_bool("dp_dev_is_rhd")`.
  - Also updated in `selfdrive/monitoring/dmonitoringd.py` and `selfdrive/ui/onroad/driver_camera_dialog.py`.
- **Behavior**: The setting is completely manual and **will never automatically change** across borders or countries.

### 2. Multi-language Localization
- **Implementation**: `dragonpilot/system/ui/lib/multilang.py` loads `dragonpilot_{lang}.po` files directly at runtime using a pure-Python PO parser (no compilation into `.mo` needed).
- **Translations Directory**: `dragonpilot/system/ui/translations/`
- **Traditional Chinese**: `dragonpilot_zh-CHT.po` has 100% string coverage.

### 3. CJK Bitmap Font Baking
- Openpilot UI renders text using Raylib bitmap fonts: `selfdrive/assets/fonts/OpFont-*.fnt` and `OpFont-*.png`.
- Any characters not in the atlas render as `?`.
- `selfdrive/assets/fonts/process.py` extracts all strings from `dragonpilot_{code}.po` to build character sets.
- Generating the atlas requires `pyray`, which is installed on the Comma device in `/usr/local/venv`.
- To re-bake fonts when adding new Chinese characters:
  ```bash
  ssh -i <SSH_KEY_PATH> comma@<COMMA_IP> "cd /data/openpilot/selfdrive/assets/fonts && /usr/local/venv/bin/python3 process.py"
  ```
  Then copy `OpFont-*` back to local repo, commit, and push.

---

## Fast Operations Runbook

### Sync Changes to Comma (Fast UI Hot Reload)
For changes to Python scripts, `.po` translations, or font assets (no C++ compile required):
```bash
# 1. Local push
git push origin 0.11.1

# 2. Remote pull & restart UI (takes ~1 second, avoids 10-minute reboot)
ssh -i <SSH_KEY_PATH> -o StrictHostKeyChecking=no comma@<COMMA_IP> "cd /data/openpilot && git pull origin 0.11.1 && pkill -f 'selfdrive.ui'"
```

### Inspecting UI Crash Logs
```bash
ssh -i <SSH_KEY_PATH> comma@<COMMA_IP> "cat /tmp/log_ui.log"
```

### Reading / Writing Openpilot Params
```bash
# Read param
ssh -i <SSH_KEY_PATH> comma@<COMMA_IP> "/usr/local/venv/bin/python3 -c \"from openpilot.common.params import Params; p = Params(); print(p.get('dp_dev_is_rhd', encoding='utf-8'))\""

# Write param (e.g. set wheel to Left)
ssh -i <SSH_KEY_PATH> comma@<COMMA_IP> "/usr/local/venv/bin/python3 -c \"from openpilot.common.params import Params; p = Params(); p.put_bool('dp_dev_is_rhd', False)\""
```

### Restarting the Entire Openpilot Stack
```bash
ssh -i <SSH_KEY_PATH> comma@<COMMA_IP> "pkill -f 'system.manager.manager'"
```
