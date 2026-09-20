# 🐲 dragonpilot (Custom Fork)

本專案為基於 openpilot / dragonpilot (`v0.11.1`) 的客製化分支，專為 Comma 3 / 3X 裝置設計，重點針對實際駕駛環境進行了方向盤手動定位、繁體中文多國語言在地化、字型點陣圖修復與介面穩定性強化。

---

## 🚀 本專案客製功能與更新重點

### 1. 🎡 方向盤位置手動設定 (Wheel on Left or Right?)
* **自訂設定項目**：
  * 於裝置端 dp 設定選單最後一項，新增「方向盤在左或在右？（Wheel on Left or Right?）」開關。
  * 提供 `Left` 與 `Right` 切換（預設為 `Left`）。
  * 說明：*Wheel on left, such as US, TW. Wheel on right like HK, JP.*
* **移除動態感知與猜測**：
  * 徹底拔除原版 `policy.py` 透過駕駛鏡頭持續動態猜測左右駕的統計過濾演算法。
  * 改為直接讀取手動設定值（`dp_dev_is_rhd`），避免因夜間逆光、駕駛坐姿或視角造成的動態誤判。
  * 設定永久儲存（`PERSISTENT`），跨國行駛亦不會隨意跳動。

### 2. 🇹🇼 完整繁體中文在地化與多語系系統支援
* **翻譯引擎重構**：
  * 重寫 `multilang.py`，支援直接解析與載入 `dragonpilot_{lang}.po` 語言檔，無需預編譯為二進位 `.mo`。
* **100% 繁體中文支援**：
  * 完整補齊 `dragonpilot_zh-CHT.po` 中所有 dp 設定字串的在地化翻譯。
  * 徹底解決系統語言切換至繁體中文時，dp 設定選單依然顯示英文的問題。

### 3. 🔤 點陣字型圖集烘焙 (解決問號 `?` 缺字問題)
* **字型處理工具升級**：
  * 更新 `selfdrive/assets/fonts/process.py`，能自動抽取所有翻譯檔中的漢字字集。
* **CJK Bitmap Font Atlas 重新烘焙**：
  * 在裝置端使用 Raylib 重新烘焙高解析度點陣字型圖檔（`OpFont-*.fnt` / `OpFont-*.png`）。
  * 徹底解決介面上中文繁體字元顯示為問號 `?` 的缺字渲染問題。

### 4. ⚡ 介面穩定性修復 (UI Crash Fix)
* **防止選單崩潰**：
  * 修復 `dragonpilot.py` 在解析布林參數時引發 `ValueError`（`int("False")`），導致點擊進入 dp 選單閃退（畫面跳回逗號 Logo）的問題。

### 5. 🔄 快速部署與熱重載工作流 (Fast Hot Reload)
* **免等 10-15 分鐘重新開機**：
  * 針對 Python 程式碼、翻譯檔與字型圖檔更新，建立快速熱重載流程。
  * 透過背景重新啟動 `selfdrive.ui`，在 1 秒內無縫套用最新變更。