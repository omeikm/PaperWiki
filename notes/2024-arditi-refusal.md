# 論文基本資訊 (MetaData)
- **Title:** Refusal in Language Models Is Mediated by a Single Direction
- **Authors:** Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, Neel Nanda
- **Venue & Year:** NeurIPS 2024
- **Tags:** #AI Safety, #Mechanistic Interpretability, #Representation Engineering, #LLM Jailbreak
- **Date Added:** 2026-11-20
- **Last Modified:** 2026-11-20
- **Paper Link:** https://arxiv.org/abs/2406.11717
- **Code Link:** https://github.com/andyrdt/refusal_direction

---

## 1. 核心重點摘要 (TL;DR)
* **核心價值：** 證明對 13 個開源 Chat LLM 而言，拒絕回答惡意指令的行為主要由殘差流中的單一一維方向所中介；移除或加入這個方向可大幅控制拒絕行為。
* **主要貢獻：**
  1. 使用 HARMFUL 與 HARMLESS 指令的 difference-in-means 方法，從模型內部表示中抽取單一「拒絕方向」。
  2. 證明 directional ablation 可在保留模型其他能力的情況下大幅停用拒絕，也可透過 activation addition 在無害指令上誘發拒絕。
  3. 提出 weight orthogonalization，直接修改模型權重，使模型不再寫入拒絕方向，並展示其比多種既有 jailbreak 方法更簡潔且具競爭力。

## 2. 研究動機與背景 (Motivation & Background)
* **現有痛點：** 聊天型 LLM 在 instruction-following 與 safety fine-tuning 後，會拒絕惡意指令，但這個拒絕機制在內部是如何表達與傳播的仍不清楚。既有 jailbreak 大多從輸入提示或模型微調出發，缺乏對模型內部機制的精確理解。
* **核心洞察 (Key Insight)：** Refusal 是可由一個線性方向作因果中介的高階行為；只要針對這個方向進行消除或注入，就能有效控制拒絕，而不必大規模改動整個模型。

## 3. 核心方法與架構 (Methodology)
* 對 HARMFUL 與 HARMLESS 指令分別取得 post-instruction residual stream activation，並計算兩者的均值差，形成 `r`；再在單一代表層與關鍵 token 位置找出最具因果效果的單位方向 `r_hat`。
* **Directional ablation：** 在推論時從所有殘差流 activation 中移除 `r_hat` 的成分，讓模型失去產生拒絕訊號的能力。
* **Activation addition：** 將 `r` 加入殘差流 activation，讓模型即使面對無害指令也傾向拒絕。
* **Weight orthogonalization：** 將所有會寫入 residual stream 的權重矩陣針對 `r_hat` 正交化，使模型永久不再將這個方向寫入中間表示；這相當於把 directional ablation 合併進權重，不需梯度優化或惡意完成範例。

## 4. 實驗與評估 (Experiments)
* **評估基準與資料集：** JAILBREAKBENCH 上的 100 筆惡意指令、ALPACA 隨機無害指令，以及 HARMBench 159 筆 standard behaviors；實驗涵蓋 13 個開源 Chat 模型，規模由 1.8B 至 72B。
* **關鍵實驗發現：**
  * 移除 refusal direction 後，多數模型對惡意指令的 refusal 明顯下降並產生 unsafe completion。
  * 在無害指令上加入 refusal direction，可讓原本會正常回答的模型開始拒絕。
  * Weight orthogonalization 在 HARMBench 的 attack success rate 與多種通用 jailbreak 具競爭力，且比 GCG 等需針對提示個別優化的方法更簡潔。
  * 模型在大多數能力評估上的退化有限，顯示干預具有相當的外科手術式效果；論文也分析 adversarial suffix 會如何將 attention 從惡意指令轉向 suffix，抑制拒絕方向的傳播。

## 5. 侷限性與未來展望 (Limitations & Future Work)
* **侷限性：** 抽取 refusal direction 的方法仍是啟發式，可能不是最優方法；結果主要來自開源模型，未必能完全外推到更大規模或未測試的專有模型。
* **侷限性：** 單一方向是否精確對應拒絕、危險或其他語義概念尚不完全清楚；coherence 評估方式也有缺陷，adversarial suffix 的機制分析僅涵蓋單一模型與單一案例。
* **未來展望：** 可尋找更穩健的方向抽取與干預位置、建立更完整的 coherence 指標，以及研究如何將拒絕機制與功能相近但更精確的安全表徵分離。

## 6. 相關工作 (Related Work)
* 與使用 neuron、rank 或 sparse autoencoder 的安全機制研究相關；這些方法通常直接移除 safety-critical components 或尋找可由資料驅動的 feature direction。
* 與 Activation Steering、Activation Addition 和 concept erasure 共用對「模型表示可線性操控」的假設。
* 相較於只透過提示最佳化或惡意資料微調的 jailbreak，本文直接利用 contrastive activation 找出因果方向，再將干預合併到權重；作者因此展現了一條計算成本較低且不需 harmful completions 的白盒路徑。

## 7. 個人省思與啟發 (Personal Takeaways)
* **🤖 AI 初步觀察與研究切入點：** 單一線性方向能中介高階安全行為，意味著安全對齊仍可能高度集中且脆弱；後續值得研究「拒絕、harmfulness、policy compliance」是否能從向量空間中被區分，而不是只移除單一方向。
* **🤖 AI 初步觀察與研究切入點：** 這篇論文對研究工具的啟示是，white-box 表徵研究可以直接產生對模型行為的因果驗證，應與黑盒 jailbreak、能力評估和安全 red teaming 結合。
* **✍️ 研究生手寫筆記區：** *（待補充：閱讀完 PDF 後，可在此寫下對自己論文的具體啟發）*
