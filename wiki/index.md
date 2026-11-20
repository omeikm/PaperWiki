# LLM Wiki Index: Representation Learning to Representation Control

> 本索引彙整 `notes/` 中核心論文條目，作為後續教學簡報生成與溯源檢查的基準清單。

| concept_id | year | paper_title | note_path | core_role_in_wiki |
| :--- | :--- | :--- | :--- | :--- |
| `sbert` | 2019 | Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks | `notes/2019-reimers-sbert.md` | 用 siamese/triplet 結構產生可做 cosine similarity 的句向量，解決 cross-encoder 推論瓶頸。 |
| `simcse` | 2021 | SimCSE: Simple Contrastive Learning of Sentence Embeddings | `notes/2021-gao-simcse.md` | 利用 Dropout 做無監督對比學習、NLI 做有監督對比學習，改善表徵空間 Alignment 與 Uniformity。 |
| `llm2vec` | 2024 | LLM2Vec: Large Language Models Are Secretly Powerful Text Encoders | `notes/2024-behnamghader-llm2vec.md` | 透過啟用雙向注意力、MNTP 與無監督對比學習，將 causal LLM 轉化為強大文字編碼器。 |
| `repe` | 2023 | Representation Engineering: A Top-Down Approach to AI Transparency | `notes/2023-zou-repe.md` | 以 top-down 視角透過 LAT 讀取高階概念方向，並進行 representation control 與 tuning。 |
| `refusal-dir` | 2024 | Refusal in Language Models Is Mediated by a Single Direction | `notes/2024-arditi-refusal.md` | 指出拒絕行為可由殘差流單一方向中介，並提出 directional ablation、activation addition 與 weight orthogonalization。 |
| `sae-superposition` | 2023 | Sparse Autoencoders Find Highly Interpretable Features in Language Models | `notes/2023-cunningham-sae.md` | 用 Sparse Autoencoder 從模型 activation 學習稀疏、可解讀且可因果定位的 feature dictionary，以處理 superposition 與 polysemanticity。 |