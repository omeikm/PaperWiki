# 論文基本資訊 (MetaData)
- **Title:** Steering Language Models With Activation Engineering
- **Authors:** Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, Monte MacDiarmid
- **Venue & Year:** arXiv 2023
- **Tags:** #Activation Engineering, #Representation Engineering, #Activation Addition, #AI Safety
- **Date Added:** 2026-11-20
- **Last Modified:** 2026-11-20
- **Paper Link:** https://arxiv.org/abs/2308.10248
- **Code Link:** https://zenodo.org/records/13879423

---

## 1. 核心重點摘要 (TL;DR)
* **核心價值：** 提出 Activation Addition（ActAdd），透過比較一對相反自然語言 prompt 的內部 activation 差，計算 steering vector，並在 inference 時直接加入 residual stream，以輕量方式控制情感、主題與毒性等輸出性質。
* **主要貢獻：**
  1. 建立不需機器學習優化或 backward passes 的 activation engineering 方法。
  2. 展示單一 prompt pair 可產生可注入的 steering vector，並以 intervention strength、intervention layer 與 sequence alignment 控制效果。
  3. 在 sentiment、toxicity 與 topic steering 上測試效果與 general capability preservation。

## 2. 研究動機與背景 (Motivation & Background)
* **現有痛點：** Prompt engineering 與 finetuning 有 reliability、side-effect 或訓練成本限制，且未必能充分 eliciting 模型已存在的能力。
* **核心洞察 (Key Insight)：** 模型 activation 空間可能包含可 causal steering high-level features 的方向；只要比較正反 prompt pair，就能直接取得「Love−Hate」等方向並於 forward pass 注入。

## 3. 核心方法與架構 (Methodology)
* 選取一組互相對立的 natural-language prompts `(p+, p−)`，例如 `Love` 與 `Hate`。
* 分別取得指定層的 activation `h_l+` 與 `h_l−`，計算差值 `h_l+ − h_l−` 作為 steering vector。
* 推論時將 steering vector 乘上 injection coefficient `c`，在指定 residual stream layer `l` 與部分 sequence positions 加入。
* 主要參數包括：
  * `c`：干預強度。
  * `l`：注入層。
  * `a`：sequence alignment。
* ActAdd 不需要 gradient descent、fine-tuning 或 backward passes，只需少量 contrast prompt pair。

## 4. 實驗與評估 (Experiments)
* **評估基準與資料集：**
  * GPT-2-XL、LLaMA-1、GPT-J、OPT 與 LLaMA-3。
  * OpenWebText、wedding topic、toxicity 與 Stanford IMDb sentiment。
  * ConceptNet／LAMA 作 general knowledge 與 off-target capability 檢查。
* **關鍵實驗發現：**
  * ActAdd 可降低 wedding 相關文本的 perplexity ratio，並對 unrelated text 保留表現。
  * 在 toxicity 與 negative-to-positive sentiment steering 中呈現有效控制；論文也指出 sentiment steering 仍會影響 fluency。
  * Steering vectors 可在 benchmark 與 qualitative completion 上改變生成方向，而不需更新權重。
  * ActAdd 的 steering direction 被視為 feature linearity 的因果證據之一，至少在論文測試的有限 prompts 與 context 中成立。

## 5. 侷限性與未來展望 (Limitations & Future Work)
* **侷限性：**
  * 使用者需調整 injection coefficient `c`、intervention layer `l` 與 sequence alignment；因此不如簡單 prompt engineering 直接。
  * 部分 steering vector 失敗，且論文未完整評估所有 reasoning effects。
  * API 需能 cache／expose intermediate activations；一般 API 未必提供此能力。
  * Finetuning 更成熟且更 flexible；ActAdd 不太可能教模型一項全新 skill。
  * Fluency 在 steering 下可能下降，sentiment 與 off-target behavior 仍需驗證。
* **未來展望：**
  * 發展更通用的 steering 方法與更穩定的 hyperparameter discovery。
  * 建立可持續控制模型 goal／priority 的 activation engineering，而不損害整體能力。
  * 將 activation editing 作為安全研究的一部分，並持續驗證其在線上與未見情境中的效果。

## 6. 相關工作 (Related Work)
* 與 prompt engineering、decoding control、fine-tuning／RLHF、steerable layers、weight editing 和 soft prompting 同屬模型控制方法。
* 與 Subramani、Dathathri、Hernandez 等 activation/embedding steering 工作相關，但 ActAdd 不使用 gradient-based 或其他 optimization，而直接用 contrast prompt pair 求差。
* 與 ITI 都在 activation space 中建立 steering direction；ITI 是選定 attention heads 並以 probes 找 truthful directions，ActAdd 則直接對 residual stream 加入 prompt-pair difference。

## 7. 個人省思與啟發 (Personal Takeaways)
* **🤖 AI 初步觀察與研究切入點：** ActAdd 最直觀的價值，是把「高階屬性」當成 activation 空間中的可加減方向，而不是只改 prompt 或權重。
* **🤖 AI 初步觀察與研究切入點：** 後續可比較 ActAdd 的單一 prompt-pair vector、ITI 的 probe-selected heads、SAE 的 feature dictionary 與 refusal direction 的 weight intervention。
* **✍️ 研究生手寫筆記區：** *（待補充：閱讀完 PDF 後，可在此寫下對自己論文的具體啟發）*
