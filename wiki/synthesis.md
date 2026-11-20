# 主線演進脈絡

## 整體故事線：從「把句子表達成向量」到「把模型內部概念變成可讀取與可控制的方向」

### 第一段：先解決句向量的效率問題

- **Sentence-BERT 建立出發點**：研究不再只追問預訓練語言模型能否分類句對，而是追問能否先把句子各自編碼成可重複使用的向量，再用 cosine similarity 快速比較。它以共享權重的 Siamese / Triplet 編碼、Pooling 與分類／回歸／Triplet 目標，把交互式句對推論改成獨立句向量推論。[2019-reimers-sbert.md]
- **承接問題**：這條路解決了檢索效率，但句向量仍可能遺失細粒度關係，且監督效果依賴訓練資料與目標任務。下一個問題因此不是「如何更快編碼」，而是「能否以更簡單且更通用的方式校正句向量空間」。[2019-reimers-sbert.md]

### 第二段：簡化對比學習，讓句向量空間自己學會對齊與分散

- **SimCSE 收斂方法**：不再依賴複雜的語義替換或增強架構，SimCSE 以同一句子經過兩次 Dropout 後得到的兩個表示作正樣本，以其他句子的表示作負樣本；監督設定再加入 NLI Entailment／Contradiction。這把表示學習轉為「拉近語義等價表示、推遠其他表示」的直接問題。[2021-gao-simcse.md]
- **承接轉折**：此時方法重心已從「設計句向量處理流程」移到「設計對比目標與表示分布」。對比學習可校正 Alignment 與 Uniformity；自然下一步是把這套方式用到更強大的 Decoder-only LLM 上。[2021-gao-simcse.md]

### 第三段：把大型 Causal LLM 轉成雙向編碼器

- **LLM2Vec 彌合雙向與因果兩條路**：Causal Decoder-only LLM 已有強大的語言能力，但 Causal Mask 限制了每個 token 的雙向語境；Encoder-only 模型雖適合表示任務卻缺乏相同規模的生成與世界知識。LLM2Vec 透過移除 Causal Mask 啟用雙向注意力、以 MNTP 適應雙向資訊、再以無監督對比學習微調向量，試圖把兩者優勢接起來。[2024-behnamghader-llm2vec.md]
- **承接轉折**：到這裡，「能否學到好向量」已升級為「能否重用大型模型的內部知識來建立表示」。這使研究從只看最終文字嵌入，轉向觀察 activation、層與 token 位置中的內部表示。[2024-behnamghader-llm2vec.md][2023-zou-repe.md]

### 第四段：從文字輸出端轉向內部表徵

- **RepE 提出 top-down 觀察方法**：Representation Engineering 不再只檢查最終嵌入是否適合檢索，而是把 activation、層與 token 位置視為高階概念的載體。透過 LAT 設計 stimulus／task、收集 neural activity，再以 PCA、線性 probing 或 cluster difference 建構方向，即可嘗試讀取 truthfulness、honesty 等概念。[2023-zou-repe.md]
- **承接轉折**：RepE 區分讀取與控制：方向能否預測概念，與方向能否因果改變模型行為並不相同。因此研究從「表示長得像什麼」推進到「表示是否能被操控，以及操控後會發生什麼」。[2023-zou-repe.md]

### 第五段：把內部方向拆成稀疏、可解讀的 feature dictionary

- **Sparse Autoencoder 處理 superposition 與 polysemanticity**：個別神經元可能混合多種語義，且 residual stream 特徵未必對齊 neuron basis。Cunningham 等人以 Sparse Autoencoder 從模型 activation 學習 overcomplete、稀疏啟動的 feature dictionary，嘗試以少數方向重建每個 activation。[2023-cunningham-sae.md]
- **承接轉折**：SAE 補上 RepE 讀取方向後的下一個問題：不只要找出一個任意的線性方向，還要找到可自然解讀、能以 activation patching 定位並能串接跨層 circuit 的單元。[2023-zou-repe.md][2023-cunningham-sae.md]

### 第六段：聚焦拒絕行為，驗證單一方向的因果控制

- **Refusal Direction 作為安全行為的收束案例**：Arditi 等人以 HARMFUL／HARMLESS contrast pairs 抽取單一差值方向，再用 activation addition 與 directional ablation 驗證該方向對拒絕行為的因果中介；weight orthogonalization 則進一步將干預合併進模型權重。[2024-arditi-refusal.md]
- **最終學習主軸**：前四篇建立「句向量可重用、對比學習可校正空間、大型 Causal 模型可改成雙向編碼、內部表示可被讀取」的基礎；最後一篇收束成可驗證的案例：安全相關行為是否由特定內部方向中介，以及如何以方向干預驗證與操控它。[2019-reimers-sbert.md][2021-gao-simcse.md][2024-behnamghader-llm2vec.md][2023-zou-repe.md][2024-arditi-refusal.md]

# 跨篇方法與目標差異

| 論文 | 主要目的 | 核心方法／干預方式 | 與前後篇的差異 |
|---|---|---|---|
| Sentence-BERT | 建立可重用且適合相似度比較的句向量，降低大量句對推論成本 | 共享權重 Siamese / Triplet 編碼；Pooling；分類、回歸或 triplet 目標 | 目標仍是文本輸出端的句向量，且依監督任務微調；主要解決檢索效率而非內部表示控制。[2019-reimers-sbert.md] |
| SimCSE | 校正預訓練語言模型句向量分佈，簡化對比句向量學習 | 同一句子的兩次 Dropout 視角視為正樣本；NLI Entailment 正樣本與 Contradiction Hard Negative | 不需複雜增強架構，以對比目標優化 Alignment / Uniformity；也不是直接操作模型內部方向。[2021-gao-simcse.md] |
| LLM2Vec | 將 Causal LLM 重新轉成雙向文字編碼器 | 移除 Causal Mask；MNTP；無監督對比學習 | 比前兩篇更往模型架構轉換；保留大型 LLM 能力並重新使其適合通用文字嵌入。[2024-behnamghader-llm2vec.md] |
| Representation Engineering | 建立讀取與控制高階內部表徵的 top-down 方法 | LAT 收集刺激下的 neural activity；以線性方向讀取；用 Reading / Contrast Vector 或 representation tuning 控制 | 關注點從產生文字嵌入轉為理解、監控與操控內部表示；用途涵蓋 honesty、harmlessness 等。[2023-zou-repe.md] |
| Sparse Autoencoders | 解決 superposition 與 polysemanticity，建立可解讀的內部 feature dictionary | 從 activation 訓練 SAE；重建 loss 搭配 sparsity loss；以 autointerpretability、case study 與 activation patching 驗證 | 比單一 linear direction 更往 overcomplete feature decomposition 前進，並可為 circuit 與行為定位提供更多單元。[2023-cunningham-sae.md] |
| Refusal Direction | 找出拒絕行為的內部中介方向並驗證因果效果 | Difference-in-means 抽取 direction；directional ablation；activation addition；weight orthogonalization | 比 RepE 更聚焦於單一安全行為；又可直接將干預合併進權重，而不只在推論時加入控制向量。[2024-arditi-refusal.md][2023-zou-repe.md] |

# 新手教學講解順序

1. **先理解「為何需要句向量」**：以 Sentence-BERT 的 cross-encoder 成本問題為例，說明獨立句向量如何支援 cosine similarity、語義搜尋與聚類。再介紹共享編碼器、pooling 與三種訓練目標。[2019-reimers-sbert.md]
2. **再理解對比學習的直覺**：用 SimCSE 的正負樣本拉近與推遠機制說明句向量空間；先講無監督的兩次 Dropout，再講監督 NLI 正負樣本。強調它是在校正表示分佈，不是單純替換架構。[2021-gao-simcse.md]
3. **連到大型模型的編碼能力**：用 LLM2Vec 的三步驟說明如何把 Causal LLM 改成雙向編碼器：移除 Causal Mask、MNTP、無監督對比學習；此階段應區分「產生文字向量」與「改變模型注意力方向」。[2024-behnamghader-llm2vec.md]
4. **進一步區分「讀取表示」與「控制表示」**：以 RepE 的 LAT 流程介紹刺激設計、activation 收集、線性方向建構，以及 reading、contrast vector 與 representation tuning 的差異。再說明應以 correlation、manipulation、necessity / sufficiency 驗證。[2023-zou-repe.md]
5. **理解超完備特徵分解**：先以 polysemantic neuron 與 superposition 介紹單神經元基礎的侷限，再講 SAE 如何以 reconstruction loss 加 sparsity loss 學習 overcomplete feature dictionary；最後用 IOI activation patching 與跨層消融連到 circuit。[2023-cunningham-sae.md]
6. **以單一安全行為收束主線**：以 refusal direction 為案例，依序講解 contrast activation → difference-in-means → unit direction → activation addition / directional ablation → weight orthogonalization。最後區分「方向存在」與「方向可精確語義解釋」兩件事。[2024-arditi-refusal.md][2023-zou-repe.md]

# 侷限性與防過度宣稱提醒

- **Sentence-BERT 的細粒度與領域泛化有限**：跨主題論證相似度仍低於對應 cross-encoder；單句向量可能不足以保留逐詞對照或未見主題推理。BERT 編碼在 CPU 上也可能比簡單雙向架構慢，因此檢索優勢不能脫離 GPU / batching 等條件。監督效果也受訓練資料與任務影響。[2019-reimers-sbert.md]
- **SimCSE 仍受基底與訓練設定限制**：效果依賴強大的 BERT／RoBERTa 基底模型；對 Batch Size 有依賴；資料增強雖簡單，仍不代表普遍適用所有模型與領域。簡報不應宣稱 Dropout 對所有表示學習問題都是最優增強。[2021-gao-simcse.md]
- **LLM2Vec 有算力與上下文長度成本**：移除 Causal Mask 並進行微調需要 GPU 記憶體與算力；極長文本仍受原模型上下文視窗限制。不能只描述為「無代價改造現成 LLM」。[2024-behnamghader-llm2vec.md]
- **RepE 的讀取不等於穩健控制**：有效讀取不一定能有效控制；linear assumption、token／layer 選擇與 stimulus 設計會影響方向品質；跨層干預可能產生級聯效應；抽出的方向未必具有單一清楚語義。簡報應避免把 LAT 或 linear direction 描述成完整模型因果解剖。[2023-zou-repe.md]
- **SAE 分解仍不是完整且穩健的 feature 真值**：重建仍有 loss，替換部分 activation 會喪失資訊並影響模型預測。較高 sparsity 可能降低 reconstruction accuracy；目前管線對 residual stream 最穩定，對 intermediate MLP 與 attention head 的學習仍有限；後層特徵與自動解讀也較困難。[2023-cunningham-sae.md]
- **IOI 與 feature 定位的泛化仍待確認**：Sparse dictionary 是 task-agnostic 訓練，但論文在 IOI 行為上的精細定位證據需更多工作確認是否能泛化到相似或不同任務；不能據此宣稱已取得完整網路電路。[2023-cunningham-sae.md]
- **拒絕方向方法只得到有限且模型相依的證據**：方向抽取仍是啟發式方法，不保證是最佳抽取；主要證據來自特定開源 Chat 模型集合，未必外推到更大規模或未測試的專有模型；方向語義也可能是 harm／danger 等概念而非單純「拒絕」。Coherence 指標、以及 adversarial suffix 機制分析的範圍仍有限。[2024-arditi-refusal.md]
- **內部方法證明的是特定干預結果，不是所有安全問題都已解決**：應把這些方法表述為一種讀取、監控或控制工具，而非證明對齊永久可靠、模型已無 jailbreak 風險，或所有能力都能不受影響地保持。[2023-zou-repe.md][2024-arditi-refusal.md]