# 論文基本資訊 (MetaData)
- **Title:** Sparse Autoencoders Find Highly Interpretable Features in Language Models
- **Authors:** Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert Huben, Lee Sharkey
- **Venue & Year:** arXiv 2023
- **Tags:** #Sparse Autoencoders, #Mechanistic Interpretability, #Superposition, #Feature Dictionaries
- **Date Added:** 2026-11-20
- **Last Modified:** 2026-11-20
- **Paper Link:** https://arxiv.org/abs/2309.08600
- **Code Link:** https://github.com/HoagyC/sparse_coding

---

## 1. 核心重點摘要 (TL;DR)
* **核心價值：** 使用 Sparse Autoencoder（SAE）從語言模型的內部 activation 中學習 overcomplete、稀疏啟動的 feature dictionary，嘗試把 superposition 中混雜的特徵拆解成更可理解的方向。
* **主要貢獻：**
  1. 將模型 activation 視為未知特徵的稀疏線性組合，以單層 autoencoder 搭配 sparsity penalty reconstruction loss學習 dictionary features。
  2. 透過 autointerpretability、monosemantic case study 與 activation patching，驗證學到的方向比 neuron、PCA、ICA 等基線更具可解讀性與因果定位能力。
  3. 展示 dictionary features 可用於更精細的 IOI 行為定位與自動 circuit detection，作為未來 mechanistic interpretability 的可擴展基礎。

## 2. 研究動機與背景 (Motivation & Background)
* **現有痛點：** 神經元常具有 polysemanticity，同一神經元可能在語義不同的情境中啟動；在 residual stream 等空間中，特徵不一定對齊 neuron basis。
* **核心洞察 (Key Insight)：** Polysemanticity 可能源於 superposition：模型以 overcomplete、非正交的方向表示數量多於層維度的特徵。若特徵足夠稀疏啟動，就可能透過 sparse dictionary learning 從 activation 重建中找到這些方向。

## 3. 核心方法與架構 (Methodology)
* 從語言模型 residual stream、MLP sublayer 或 attention head sublayer 抽取內部 activation。
* 訓練單層 Sparse Autoencoder：encoder 與 decoder 使用 tied weights、hidden size 為模型維度乘上 dictionary size ratio，並以 ReLU 產生稀疏係數。
* 最佳化 reconstruction loss 與 `L1` sparsity loss：
  * reconstruction loss 確保 decoded activation 接近原始 activation。
  * sparsity loss 鼓勵每個 activation 只由少數 dictionary features 線性組合。
* 用 OpenAI autointerpretability 讓模型為 feature 產生自然語言描述，再預測其在新文本上的啟動程度並計算可解讀性分數。
* 用 activation patching 修改 residual stream 中指定 feature 的方向，並量化對輸出 logits 與任務的因果效果。

## 4. 實驗與評估 (Experiments)
* **評估基準與資料集：**
  * 主要研究 Pythia-70M 與 Pythia-410M 的 residual stream；也比較 MLP 與 attention head sublayer。
  * 與 default basis、random directions、PCA 與 ICA 的 feature dictionaries 比較。
  * 在 Indirect Object Identification（IOI）反事實句子上進行 activation patching。
* **關鍵實驗發現：**
  * Sparse dictionary features 在 autointerpretability 分數上整體優於多種 baseline；效果在較後層下降，也可能受後層特徵更複雜或自動解讀能力限制。
  * 個別 feature 會呈現 highly monosemantic 特徵，例如只針對 apostrophe、period、`the` 或 newline 等輸入模式。
  * Ablating apostrophe dictionary feature 的主要效果是降低緊接其後的 `s` token logit，與其對 contraction 或 possessive 結構的可理解作用一致。
  * 在 IOI activation patching 中，sparse feature dictionary 能以較少 patches 達成相同 KL divergence，且在較小 edit magnitude 下改善 PCA 與 non-sparse dictionary 的編輯權衡。
  * 可透過 feature 跨層的因果消融建立 causal tree，用於自動 circuit detection。

## 5. 侷限性與未來展望 (Limitations & Future Work)
* **侷限性：**
  * Dictionary reconstruction 無法達到 zero reconstruction loss；替換部分 residual stream activation 後仍會喪失資訊並影響模型預測。
  * 較高 sparsity coefficient 可提升稀疏性，但可能降低 reconstruction accuracy。
  * 目前 SAE 訓練管線最適合 residual stream；對 intermediate MLP layer 尚不穩定，在 attention head 與 MLP 上理解運算仍有額外挑戰。
  * IOI 結果雖具前景，但 feature dictionary 是 task-agnostic，是否能推廣到相似任務之外仍需更多驗證。
  * 自動解讀主要依賴文字模式，並未直接把 causal output 變化送回 hypothesis generation；後層特徵較複雜，因此 autointerpretability 不一定能完整描述。
* **未來展望：**
  * 探索其他 SAE 架構、加入 feature 或相鄰層資訊，並直接優化 activation replacement 對模型輸出造成的變化。
  * 發展更穩健的 MLP 與 attention head dictionary training。
  * 繼續追蹤跨層 feature 的 causal dependencies，朝向以稀疏且端到端可理解的 lens 描述模型運算。

## 6. 相關工作 (Related Work)
* 延續 Yun et al. 與 Sharkey et al. 等 sparse dictionary learning 工作，並將方法應用於 language model activation。
* 相較於 neuron basis、PCA、ICA 與 random/default directions，SAE 透過 learned overcomplete dictionary 與 sparsity penalty 尋找可能對應單一語義的 activation directions。
* 與視覺皮質 sparse dictionary learning 及模型稀疏化方法相關，但本文是在訓練完成後再從 activation 中施加稀疏分解，而非從頭調整 foundation model 架構或訓練目標。

## 7. 個人省思與啟發 (Personal Takeaways)
* **🤖 AI 初步觀察與研究切入點：** SAE 提供了從「任意 internal direction」進到「可能更 monosemantic 的 feature dictionary」的方法，可與 RepE 的 representation reading 和 direction control 串接。
* **🤖 AI 初步觀察與研究切入點：** 下一步值得思考的是，如何區分 SAE feature 是否真實對應可泛化的網路概念，而不只是特定資料與 token 分布下產生的稀疏分解。
* **✍️ 研究生手寫筆記區：** *（待補充：閱讀完 PDF 後，可在此寫下對自己論文的具體啟發）*
