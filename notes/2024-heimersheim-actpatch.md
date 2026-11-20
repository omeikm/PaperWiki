# 論文基本資訊 (MetaData)
- **Title:** How to use and interpret activation patching
- **Authors:** Stefan Heimersheim, Neel Nanda
- **Venue & Year:** arXiv 2024
- **Tags:** #Mechanistic Interpretability, #Activation Patching, #Causal Interventions, #Circuit Analysis
- **Date Added:** 2026-11-20
- **Last Modified:** 2026-11-20
- **Paper Link:** https://arxiv.org/abs/2404.15255
- **Code Link:** N/A

---

## 1. 核心重點摘要 (TL;DR)
* **核心價值：** 總結 Activation Patching 的實務做法與解讀陷阱，說明如何在 mechanistic interpretability 中從因果干預結果推論模型電路，而不把 patching 效果誤當成完整模型因果證明。
* **主要貢獻：**
  1. 系統比較 exploratory／confirmatory patching、residual stream／MLP／attention／neuron／SAE feature 等不同粒度，以及 path patching。
  2. 分析 denoising 與 noising 的不同因果含義，並說明 prompt corruption、AND／OR circuit 與 backup behavior 如何影響解讀。
  3. 結構化比較 logit difference、logprob、probability、accuracy 與 KL divergence 等 metric 的優缺點。

## 2. 研究動機與背景 (Motivation & Background)
* **現有痛點：** Activation patching 名稱與實作方式多，容易與 ablation 或 causal tracing 混淆；單看 patching heatmap 也可能把必要性、充分性、直接路徑與線路備份行為混在一起。
* **核心洞察 (Key Insight)：** Patching 是在兩個相近 prompt run 之間替換特定 activation，以控制哪些資訊變化；但其結果只說明特定 prompt distribution 下的 sufficiency 或 necessity，不能直接外推成所有模型行為。

## 3. 核心方法與架構 (Methodology)
* 執行前選取 source／clean prompt 與 destination／corrupt prompt；保存 source run 的 activation，再於 destination run overwrite 指定 residual stream、MLP、attention head、neuron 或 SAE feature。
* **Denoising（clean → corrupt）：** 用 clean activation 修復 corrupt run，測試 patched component 是否 sufficient to restore behavior。
* **Noising（corrupt → clean）：** 用 corrupt activation破壞 clean run，測試 patched component 是否 necessary to maintain behavior。
* **Granularity：** 可先從 residual stream patching 起步，再增加到 MLP／attention head／neuron／SAE feature，最後用 path patching 分辨 direct connection 與 mediation。
* **Zero／mean／Gaussian noise patching：** 單 prompt 或 single-run ablation 類方法可以定位必要性，但相比 clean-corrupt pair 的 precision 與 in-distribution 控制通常較弱。

## 4. 實驗與評估 (Experiments)
* **評估基準與資料集：** 本文以 factual recall、IOI、AND／OR circuit 與 toy circuit 作方法說明，並對比多種 patching 技術與 metrics。
* **關鍵實驗發現：**
  * Exploratory patching 通常逐一 patch component 做 sweep；confirmatory patching 則一次 patch 多個 hypothesized circuit components，確認是否足以支撐行為。
  * Denoising 與 noising 不互為對稱：前者關心 sufficient restoration，後者關心 necessary disruption。
  * Narrow prompt variations 適合 exploratory patching；confirmatory patching 需用 wider prompt distribution 控制 hypothesized circuit 的所有變數。
  * Continuous linear-ish metrics（如 logit difference／logprob difference）較適合 exploratory patching；probability 與 accuracy 可能受 saturation 或 threshold 效應影響。

## 5. 侷限性與未來展望 (Limitations & Future Work)
* **侷限性：**
  * Patching 結果高度依賴 clean／corrupt prompt 的選擇與 prompt distribution。
  * Positive result 不代表找到最小 circuit；可有 sufficient cross-section、necessary full-circuit 或 backup components 等不同解讀。
  * AND／OR circuit、negative components 與 backup heads 可使單純 patch heatmap 看起來矛盾或低估原始 circuit。
  * Discrete metric 易在 threshold 附近失敏；probability 是 logits 的 exponential transform；logprob 可能 saturation 或 unspecific。
* **未來展望：** 使用多組 prompt distribution、cross-section 與 path patching 合併驗證 circuit；建立包含多種 continuous／discrete metrics 的 patching dataframe；持續研究 backup behavior、negative components 與 causal scrubbing 的 rigor。

## 6. 相關工作 (Related Work)
* 涵蓋 Causal Tracing、Interchange Intervention、Resample Ablation、Causal Mediation Analysis、Causal Scrubbing、attribution patching 與 SAE feature patching。
* 與 Ablation 相比，activation patching 以另一個 run 的 activation 替換 target activation，可控制不同 prompt fact 而不只把 activation 歸零。
* 與功能 steering、SAE 或線性 probe 不同，本文不是提出一個新控制方法，而是提供因果 patching 實驗的 best practices 與 interpretive guardrails。

## 7. 個人省思與啟發 (Personal Takeaways)
* **🤖 AI 初步觀察與研究切入點：** 從這篇可建立「先控制 prompt difference，再選 patch target，再選 metric，最後才解讀 circuit」的標準流程。
* **🤖 AI 初步觀察與研究切入點：** 未來讀任何 patching 結果都應同步確認 denoising／noising方向、prompt distribution、metric 與 backup behavior。
* **✍️ 研究生手寫筆記區：** *（待補充：閱讀完 PDF 後，可在此寫下對自己論文的具體啟發）*
