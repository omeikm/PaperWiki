# Project Specification: Representation Learning PaperWiki

## 1. 專案目的與核心理念
本專案是一個專注於 **Representation Learning（表示學習）** 領域的個人學術論文知識庫（PaperWiki）。
核心目標是建立一套標準化、具備溫度的網頁架構與開發規則，讓 AI Agent（如 GitHub Copilot）在讀取使用者**主動提供（Provided）的原始筆記草稿與論文 PDF** 時，能夠依照統一的視覺風格、互動機制與內容架構，**增量擴充與精準同步**論文導讀頁面，並保持全站風格與結構的 100% 一致性。

---

## 2. 專案檔案結構與命名規範（模組化架構）
所有開發與新增檔案必須嚴格遵守以下目錄架構，且所有關聯檔案（PDF、原始筆記、網頁）必須使用一致的檔名前綴。**JavaScript 必須依功能拆分為獨立模組，禁止將所有邏輯塞入單一檔案**：

```text
/ (專案根目錄)
├── AGENTS.md                  # 本專案開發與協作規則書（Spec）
├── .github/
│   └── copilot-instructions.md # 同步 AGENTS.md 內容，供 GitHub Copilot 自動讀取
├── index.html                 # 網站首頁（包含暖調書房視覺、Tag 互動篩選與論文卡片列表）
├── pdfs/                      # 存放論文原始 PDF 檔案
│   └── [year]-[first-author]-[short-title].pdf
├── notes/                     # 存放使用者提供的原始 Markdown/純文字筆記草稿 (Provided Raw Notes)
│   └── [year]-[first-author]-[short-title].md
├── assets/
│   ├── css/
│   │   └── style.css          # 全站共用樣式表（定義 Warm Academic 色系、字體與便利貼特效）
│   ├── images/                # 存放論文截圖資源
│   │   └── [year]-[first-author]-[short-title]/
│   │       └── figure.png
│   └── js/                    # 模組化 JavaScript（依功能拆分，使用 ES Modules 或獨立引入）
│       ├── filter.js          # 首頁 Tag 即時篩選邏輯
│       ├── progress.js        # 單篇論文頂部閱讀進度條邏輯
│       ├── mood-badge.js      # 研究生「閱讀狀態 / 心情印章」localStorage 狀態管理
│       └── accordion.js       # 論文各章節（H2）展開與收合互動邏輯
└── papers/                    # 存放最終生成的獨立論文筆記網頁
    └── [year]-[first-author]-[short-title].html  # 檔名一律全小寫英文加連字號（例如：2025-lee-example-paper.html）

```

---

## 3. 網頁視覺風格：Warm Academic（暖調學術書房風）

為了讓研究生在長時間閱讀論文時兼顧專業感與視覺溫度，全站 UI 必須遵守以下設計系統（Design System）：

* **色彩配置 (Color Palette)：**
* **主背景色：** 暖米白 / 羊皮紙色 (`#FAF8F5`)，降低長時間閱讀的視覺疲勞。
* **卡片與內容容器：** 溫潤象牙白 (`#FFFFFF`) 搭配極細暖灰邊框 (`#E6E2D8`) 與柔和陰影。
* **主強調色 (Primary Accent)：** 陶土橘 (`#D97757`)，用於重點標籤、進度條與互動按鈕。
* **次強調色 (Secondary Accent)：** 鼠尾草綠 (`#4A6B5D`)，用於次要狀態標示與本地 PDF 按鈕。
* **主要文字色：** 深炭灰 (`#2D2A26`) 取代純黑，輔助說明文字使用暖灰 (`#6E6A63`)。
* **字體階層 (Typography)：**
* **論文大標題與章節標題：** 使用襯線體（`Merriweather`, `Noto Serif TC`, serif），營造學術雜誌的沉澱感。
* **內文、標籤與導覽列：** 使用清晰易讀的無襯線體（`Inter`, `Noto Sans TC`, sans-serif）。
* **響應式設計 (RWD)：** 必須支援桌面端與行動裝置瀏覽，文章內文最大寬度限制在 `760px`～`820px` 以維持最佳閱讀行長。
* **首頁卡片排版與對齊規範 (Card Alignment)：**
  * 首頁論文卡片網格（`.paper-grid`）內的每張卡片（`.paper-card`）必須採用**垂直 Flex 佈局**（`display: flex; flex-direction: column; justify-content: space-between; height: 100%;`）。
  * 卡片底部的作者與「閱讀筆記 ↗」連結列必須使用 `margin-top: auto;` 固定貼齊卡片最下方，確保無論標題或摘要行數多寡，同一列卡片的底部動作按鈕皆保持在同一水平線上。
* **論文內圖片與圖說樣式 (Image Styling)：**
  * 內文圖片（`.paper-content img`）必須置中、最大寬度 `90%`、帶有圓角 (`8px`)、溫潤暖灰邊框 (`#E6E2D8`) 與柔和陰影。
  * 圖片下方圖說（`figcaption` / `blockquote`）需置中、字體縮小（`0.9rem`）且使用暖灰色（`#6E6A63`）。

---

## 4. 網頁互動機制規範 (Modular Interactive Features)

所有互動功能皆為純前端（Vanilla JS + `localStorage`）實作，無需後端伺服器即可在 GitHub Pages 運作，且嚴格對應 `assets/js/` 下的模組：

1. **首頁 Tag 即時互動篩選 (`assets/js/filter.js` -> 僅 `index.html` 引入)：**
* 首頁頂部需列出所有論文標籤（如 `#Representation Learning`、`#Contrastive Learning`、`#Variational Inference`）。
* 點擊標籤時，下方的論文卡片列表需平滑過濾出符合該標籤的文章，並提供「全部顯示 (All)」按鈕。

2. **頂部閱讀進度條 (`assets/js/progress.js` -> 僅 `papers/*.html` 引入)：**
* 單篇論文頁面視窗最上方需固定一條 `4px` 高的陶土橘 (`#D97757`) 進度條，隨捲動軸即時顯示閱讀百分比。

3. **研究生「閱讀狀態 / 心情印章」切換器 (`assets/js/mood-badge.js` -> 僅 `papers/*.html` 引入)：**
* 在每篇論文頂部的 MetaData 資訊卡右上角，提供一個可點擊切換狀態的互動按鈕，並將狀態儲存於瀏覽器 `localStorage`（以該篇論文檔名為 key）：
* `🌱 初讀萌芽`（預設狀態）
* `☕ 深度消化中`
* `💡 靈感爆發`
* `🤯 看到懷疑人生`


4. **章節折疊與專注模式 (`assets/js/accordion.js` -> 僅 `papers/*.html` 引入)：**
* 論文內文的各個主要章節（H2）需支援點擊標題展開或收合內容，方便讀者快速對照特定段落。

### 4.5 首頁頂部 Navigation / Tab（整合 LLM Wiki 與教學簡報）
- 在 `index.html` 最上方提供輕量頂部切換列（`.site-nav`），讓使用者可在同一個站點切換：
  - **LLM Wiki**（保留原本 PaperWiki 首頁與論文卡片列表）
  - **教學簡報**（連結至教學型 HTML 簡報，`build/slides.html`，並確保相對路徑在 GitHub Pages 可正常開啟）
- 視覺沿用 Warm Academic 色系（`#FAF8F5`、`#FFFFFF`、`#2D2A26`、`#6E6A63`、`#E6E2D8`、`#D97757`、`#4A6B5D`），不破壞既有 `.paper-grid`、`.paper-card` 與 `assets/js/filter.js` 的篩選行為。

---

## 5. 單篇論文筆記內容格式規範 (Content Schema)

將 `notes/` 中的原始筆記轉換為 `papers/` 網頁時，**不需羅列繁瑣的數學推導**，應著重於觀念、架構、實驗、限制與脈絡，並嚴格包含以下 **MetaData 資訊卡**與 **7 大核心區塊**：

### 頂部 MetaData 資訊卡

* 論文完整英文標題與中文譯名
* 作者群與所屬機構 (Authors & Affiliation)
* 發表會議/期刊與年份 (Venue & Year)
* 主題標籤陣列 (Tags)
* **時間戳記雙欄位（供版本追蹤）：**
* 收錄日期 (`Date Added: YYYY-MM-DD`)
* 最後修改日期 (`Last Modified: YYYY-MM-DD`，初次建立時與收錄日期相同)


* **資源連結按鈕區：**
* `📄 閱讀本地 PDF`（連結至 `../pdfs/[filename].pdf`，使用鼠尾草綠 `#4A6B5D` 強調按鈕樣式）
* `🔗 原始論文 (arXiv/OpenReview)` 與 `💻 開源程式碼 (GitHub)`

### 7 大固定內容區塊

1. **核心重點摘要 (TL;DR)：** 一句話總結論文核心價值，並條列 3 項主要貢獻。
2. **研究動機與背景 (Motivation & Background)：** 點出現有方法的痛點，以及本篇論文的核心洞察（Key Insight）。
3. **核心方法與架構 (Methodology)：** 用直觀、好懂的語言解釋模型運作機制與關鍵設計巧思（避免純公式堆砌）。
4. **實驗與評估 (Experiments)：** 說明評估資料集、對比基準（Baselines）以及關鍵實驗發現。
5. **侷限性與未來展望 (Limitations & Future Work)：** 客觀分析該方法目前的限制（如算力開銷、資料依賴）與未來延伸方向。
6. **相關工作 (Related Work)：** 梳理前人研究脈絡，並明確指出本篇論文與同期方法的本質差異。
7. **個人省思與啟發 (Personal Takeaways) — 特殊視覺樣式：**
* 忠實保留使用者在原始筆記中寫下的個人思考、疑惑或研究啟發。
* **UI 渲染規定：** 此區塊在 HTML 中必須套用專屬的 `.sticky-note` 樣式，呈現為一張**帶有淡淡暖黃/米黃底色 (`#FFF9DB`)、細微陰影、微幅傾斜 (`rotate(-0.8deg)`) 的手寫便利貼卡片**，為嚴肅的學術筆記保留溫度。

---

## 6. AI 新增與同步內容的標準作業流程 (Incremental Update & Sync SOP)

當使用者要求「上架新筆記」或「同步更新網站」時，AI 必須執行**基於修改日期的增量同步機制**，**嚴禁進行無差別的全站重建**：

1. **變更偵測與比對 (Change Detection)：**
* 掃描 `notes/` 目錄下的所有 `.md` 檔案，比對其檔案最後修改日期（或內容差異）與 `papers/` 中對應 `.html` 頁面的 `Last Modified` 欄位。
* **未變更之舊檔絕對唯讀：** 凡是 `notes/` 內容未更動的歷史論文，**嚴禁修改或覆寫**其對應的 `papers/*.html` 檔案。
2. **三種執行情境處置：**
* **情境 A（全新筆記）：** 若 `notes/` 中有對應不到 `.html` 的新檔案，則依據第 5 節規範生成全新的 `papers/[filename].html`（`Date Added` 與 `Last Modified` 皆設為當日日期），並在 `index.html` 的 `.paper-grid` 最上方**附加 (Prepend)** 該論文卡片。
* **情境 B（已存在但有修改的筆記）：** 若某篇 `notes/[filename].md` 的修改時間晚於對應網頁的 `Last Modified` 日期（或使用者明確指出修改了該篇筆記），則**僅針對該單一 HTML 檔案進行重新渲染**，保留原本的 `Date Added`，並將 `Last Modified` 更新為最新修改日期（若首頁卡片有顯示更新日期或摘要變動，亦同步局部更新該張卡片）。
* **情境 C（無任何變更）：** 若所有檔案皆為最新狀態，回報「所有筆記皆已同步，無需更新」並結束任務。
* **情境 D（刪除筆記）：**
  * 若 AI 在掃描時發現 `pdfs/` 中某個 `.pdf` 檔案已被移除，不須做任何事情。
  * 若 AI 在掃描時發現 `notes/` 中某個 `.md` 檔案已被移除（對應不到來源筆記）：
  * 1. **清理網頁：** 自動刪除 `papers/` 中對應的 `.html` 檔案。
  * 2. **更新首頁：** 自動從 `index.html` 的 `.paper-grid` 容器中移除該篇論文的摘要卡片。
  * 3. **保留原始 PDF：** 為了安全起見，預設**不主動刪除** `pdfs/` 中的原始 PDF（除非使用者明確要求連同 PDF 一起刪除）。
3. **忠實轉換原則：** 轉換內容時必須保留使用者在 `notes/` 中撰寫的原意與個人省思，嚴禁擅自捏造實驗數據或竄改個人心得；並確保 CSS (`../assets/css/style.css`) 與對應的模組化 JS (`../assets/js/*.js`) 路徑引入正確。