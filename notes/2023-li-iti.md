# 論文基本資訊 (MetaData)
- **Title:** Inference-Time Intervention: Eliciting Truthful Answers from a Language Model
- **Authors:** Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, Martin Wattenberg
- **Venue & Year:** NeurIPS 2023
- **Tags:** #Representation Learning, #AI Safety, #Truthfulness, #Activation Editing
- **Date Added:** 2026-11-20
- **Last Modified:** 2026-11-20
- **Paper Link:** https://arxiv.org/abs/2306.03341
- **Code Link:** https://github.com/likenneth/honest_llama

---

## 1. 核心重點摘要 (TL;DR)
* **核心價值：** 提出 Inference-Time Intervention（ITI），透過在少數 attention heads 的 activation 空間中加入與 truthfulness 相關的方向，提升語言模型在 TruthfulQA 上產生真實回答的能力。
* **主要貢獻：**
  1. 使用線性 probe 找出與 truthfulness 相關的 attention heads 與方向。
  2. 在 inference 過程中只對部分高 probe accuracy 的 heads 做 activation shift，並對每個 next-token prediction 重複干預。
  3. 展示 ITI 可少量資料、低計算成本地提升 TruthfulQA 真實度，但也會與 helpfulness 出現取捨。

## 2. 研究動機與背景 (Motivation & Background)
* **現有痛點：** LLM 有時會產生看似正確但實際錯誤或 hallucinated 的回答；前人研究也指出，模型的輸出可能錯誤，但中間 activation 中可能已包含正確資訊。
* **核心洞察 (Key Insight)：** 模型內部可能存在可分辨真實與錯誤陳述的 activation 方向；若能把這些方向定位並於 inference 時沿方向移動 activation，便可能縮小「知道」與「說出」之間的差距。

## 3. 核心方法與架構 (Methodology)
* 對 TruthfulQA 的 true／false QA pairs，在每個 attention head 的 activation 上訓練線性 probe；以驗證準確率排序 heads。
* 選取 top-K heads，避免干預所有 heads；每個 head 的 probe weight 或 truthfulness mean difference 可作為 truthful direction。
* 在 autoregressive generation 時，將 activation 沿 truthful direction shift：
  * 依 selected head 的 activation standard deviation scaling 方向；
  * 以 intervention strength `alpha` 控制干預強度；
  * 每個 next-token prediction 都重複此程序。
* ITI 干預可低計算成本實作，也可透過修改 attention output projection 的 bias offline bake into the model。

## 4. 實驗與評估 (Experiments)
* **評估基準與資料集：**
  * TruthfulQA，包含 multiple-choice 與 generation tracks；
  * LLaMA-7B、Alpaca 與 Vicuna；
  * 另以 Natural Questions、TriviaQA 與 MMLU 測試 out-of-distribution generalization。
* **關鍵實驗發現：**
  * LLaMA-7B 的 probe 與 generation accuracy 存在差距，最突出 attention head 在分離 truth／false activation 上有較高驗證準確率。
  * Alpaca baseline 在筆記中的 TruthfulQA true*informative 為 32.5%，加入 ITI 後為 65.1%；Vicuna baseline 為 51.5%，加入 ITI 後為 74.0%。
  * top-K 與 `alpha` 的超參數掃描呈現 truthfulness 與 helpfulness 之 trade-off；過強干預可能使大量問題回答「I have no comment」。
  * 相較 intervention all heads 或 point-wise selection，head-wise selection 在維持資訊性與限制 perturbation 大小上較適合。
  * 在未重新調整參數的分布外測試中，ITI 在 LLaMA-7B 的 Natural Questions、TriviaQA 與 MMLU 多選準確率上都有提升。

## 5. 侷限性與未來展望 (Limitations & Future Work)
* **侷限性：**
  * TruthfulQA 無法涵蓋「truth」的完整意義，結果主要針對特定真實性與 common misconceptions。
  * ITI 會有 truthfulness 與 helpfulness trade-off；overly strong intervention 可能犧牲資訊性。
  * 論文未宣稱已機制性理解 ITI 如何改變模型內部表示，也未宣稱 ITI 足以確保所有 truthful answers。
  * out-of-distribution 評估是初步探索；未來需在真實聊天情境與更廣泛資料上驗證。
* **未來展望：**
  * 探索 unsupervised 或更少人工標註的 truthful direction discovery；
  * 研究 truthfulness 在 activation subspace 中的 multidimensional geometry；
  * 評估更廣泛的資料、真實聊天情境，以及 truthfulness 與 helpfulness 的 hyperparameter trade-off。

## 6. 相關工作 (Related Work)
* 屬於 activation editing 與 steering vectors 路線，可調整 inference 表示且比 weight editing 更 minimally invasive。
* 與 Contrast-Consistent Search（CCS）一同利用 latent representations 找真實方向，但 ITI 用 TruthfulQA labels 找方向並以 benchmark 因果效果驗證干預。
* 與 RLHF／RLAIF 不同，ITI 不需要對模型做 reinforcement-learning fine-tuning；而是以少量 annotated QA pairs 找出 attention-head directions。

## 7. 個人省思與啟發 (Personal Takeaways)
* **🤖 AI 初步觀察與研究切入點：** ITI 可作為「內部 probing 找方向、對特定 components 注入方向、再以 output behavior 驗證」的實作案例。
* **🤖 AI 初步觀察與研究切入點：** 後續值得比較 ITI 的 sparse head selection、SAE learned features 與 refusal direction，釐清分解粒度、干預位置與行為目標如何影響控制效果。
* **✍️ 研究生手寫筆記區：** *（待補充：閱讀完 PDF 後，可在此寫下對自己論文的具體啟發）*
