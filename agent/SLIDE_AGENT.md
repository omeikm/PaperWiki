# Agent Specification: Teaching Slide Deck Generator (Slide Agent)

## 1. 職責範圍
依據 `wiki/synthesis.md`、`wiki/manifest.json`（或 `wiki/index.md`）與 `notes/*.md` 的內容，規劃並生成給「原本不熟悉該主題的新手」閱讀的教學型簡報內容（先產出 `build/outline.json` 與 `build/slides_content.json`，再由 `scripts/assemble_slides.py` 組裝成 `build/slides.html`，並由 `scripts/` 下的驗證腳本進行最終檢查）。

## 2. 輸入來源與分工邊界
- **主要脈絡與順序**：參考 `wiki/synthesis.md` 中的「主線演進脈絡」、「新手教學講解順序」與「侷限性與防過度宣稱提醒」。
- **細節與證據**：只針對每頁綁定的 `source_files` 查閱對應的 `notes/*.md`（例如 `2019-reimers-sbert.md`、`2021-gao-simcse.md`、`2023-zou-repe.md`、`2023-cunningham-sae.md`、`2024-arditi-refusal.md`、`2024-behnamghader-llm2vec.md` 等）。
- **確定性交接**：來源清單、條列數量、字數上限、來源合法性、HTML 渲染輸出與最終 HTML 結構檢查，皆以 `scripts/` 下的 deterministic 腳本輸出為準，Agent 不自行宣告檢查通過。

## 3. 生成流程
1. **階段 A：規劃教學大綱（輸出 `build/outline.json`）**
   - 為零基礎新手安排循序漸進的頁數與學習目標（建議 6～12 頁）。
   - 每頁明確指定 `slide_id`、`title`、`goal`、`key_points` 與 `source_files`。
   - 執行 `python scripts/check_outline.py` 驗證大綱欄位、來源檔名合法性、知識庫覆蓋率與頁數節奏；若 `FAIL`（或有需修正的 `WARN`），依錯誤訊息修改 `build/outline.json` 後重跑。
2. **階段 B：生成逐頁教學內容（輸出 `build/slides_content.json`）**
   - 依通過檢查的 `build/outline.json` 逐頁撰寫新手友善的教學內容，建議包含 `slide_id`、`title`、`analogy`（直覺比喻）、`bullets`（核心要點）、`limitation_note`（限制或邊界提醒）與 `source_files`。
   - 嚴格控制每頁條列數量與文字精簡度，避免單頁塞入過多文字導致後續 HTML 排版溢出。
   - 執行 `python scripts/verify_content.py` 驗證每頁來源合法性、條列數與字數上限；若 `FAIL`（或有需修正的 `WARN`），只針對違規頁面修正並重跑檢查。
3. **階段 C：HTML 組裝與最終驗收（輸出 `build/slides.html`）**
   - 執行 `python scripts/assemble_slides.py`，將通過驗證的 `build/slides_content.json` 確定性渲染為 `build/slides.html`。
   - 執行 `python scripts/verify_html.py` 檢查渲染後的 HTML 結構、來源標記、殘留佔位符與導覽控制；若 `FAIL`（或有需修正的 `WARN`），回到對應的內容或組裝步驟修正後重跑。

## 4. 教學與溯源規則
- **新手友善、先直覺後細節**：避免一上來就堆砌過多專有名詞或公式；先講「為什麼需要／解決什麼問題」，再講做法與機制。
- **嚴格可溯源**：簡報中的概念、方法與實驗結論必須能對應到 `source_files` 所指定的 `notes/*.md`，不得自行編造論文未提及的數據或結論。
- **防過度宣稱**：在講解方法效果或應用潛力時，同步帶出各篇筆記中提到的限制與邊界條件（如算力與上下文長度成本、線性假設與干預副作用、啟發式抽取、開源模型範圍或安全干預的侷限），不把單一方法描述成萬能解法。
- **精簡可讀**：每頁聚焦 1 個核心教學重點，條列精簡、語句清楚，方便在 HTML 簡報中閱讀。

## 5. 執行與失敗重試指引
- **執行檢查**：
  - 完成 `build/outline.json` 後執行 `python scripts/check_outline.py`。
  - 完成 `build/slides_content.json` 後執行 `python scripts/verify_content.py`。
  - 產出 `build/slides.html` 後執行 `python scripts/assemble_slides.py` 與 `python scripts/verify_html.py`。
- **判定標準**：
  - `PASS`：所有確定性規則通過，可進入下一步。
  - `WARN`：存在節奏、字數上限或版面提醒，建議視情況調整並重跑。
  - `FAIL`：存在缺欄位、非法來源引用、漏涵蓋核心筆記、條列數超標或 HTML 結構／佔位符違規，必須修正後重新執行對應腳本。
- **失敗處理**：先看腳本輸出的具體錯誤原因（哪一頁、哪個欄位、哪個來源或哪項 HTML 檢查出錯），精準修改對應內容後重跑，不要整份盲目重寫。