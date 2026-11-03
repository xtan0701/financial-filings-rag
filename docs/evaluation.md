# Limitations and evaluation protocol

## Current evidence

The retained materials contain source code and filing inputs. They contain no scored answer set, model response transcripts, human rankings, token usage, end-to-end timing, or production outcomes. Offline integrity and UI startup checks cannot establish retrieval quality or factual answer quality.

## Known limitations in the implemented pipelines

1. **Corpus state:** the first FAISS index persists in `st.session_state`. Changing uploads does not invalidate it. Start a fresh session when changing the corpus; do not interpret answers from a stale index as answers about the new upload.
2. **Conversation:** the primary OpenAI app shows chat history but does not pass it to the model. In history-enabled variants, history and persona become part of the retrieval query and can displace relevant passages.
3. **Evidence:** requesting citations does not validate them. Source panels show page indices and may omit filenames. The primary app has no evidence panel. Manual source checking remains necessary.
4. **Financial reasoning:** text splitting is not table parsing. The code does not enforce units, periods, company alignment, or arithmetic accuracy.
5. **Confounding:** providers, embeddings, chunk sizes, temperatures, and prompts differ across variants. An observed answer difference would not isolate one factor.
6. **Data flow:** the financial Ollama variant still sends text to Google for embeddings. DeepSeek variants also use Google embeddings. Cloud variants require authorization to send uploaded content to their providers.
7. **Operational behavior:** no robust handling for empty/scanned/encrypted PDFs, provider failures, context limits, or malicious document instructions is implemented. Upload filenames are used as temporary paths. Treat this as a local prototype for trusted documents.
8. **Compatibility:** model IDs and SDK APIs reflect the original implementation. Installation and startup do not confirm that a historical cloud model is still available to a given account.
9. **UI latency:** word-by-word display uses `time.sleep`; this is simulated streaming after a complete response, not provider token streaming or a latency measurement.

The public preparation changes credential configuration and organization, while preserving the original analytical behavior. The limitations above are documented rather than silently replaced with a different experiment.

## Proposed study — not executed

Build a manually checked question set from the included snapshots before comparing answers. Preserve the exact question, company, period, expected unit, answer evidence, and physical PDF page alongside each reference answer. Use a separate development set and a held-back question set. If questions or outputs have already been inspected during tuning, report subsequent evaluation as retrospective.

| Question type | Example task | What to check |
| --- | --- | --- |
| Single disclosure | Locate a company's disclosed segment revenue | Exact amount, scale, period, and supporting passage |
| Cross-company comparison | Compare disclosed cloud segment measures | Whether definitions and fiscal periods are comparable |
| Multi-step calculation | Calculate a year-over-year change from a filing table | Correct operands, denominator, unit, and arithmetic |
| Narrative synthesis | Summarize a specified risk factor | Coverage without invented facts; traceable source |
| Follow-up | Ask “How did that change?” after a company-specific question | Correct reference to earlier company and metric |
| Missing evidence | Ask about a period absent from the PDFs | Explicit abstention, without fabricated figures |

Run a no-retrieval model and manual document lookup as baselines. Hold corpus, model, embedding, prompt, and retrieval configuration fixed while changing chunk size; then test other factors separately. Log model IDs, dependency versions, question IDs, retrieved passages, raw answers, and any failures.

Score factual correctness and citation support separately. Also record unsupported-claim rate, correct abstention, period/unit errors, and retrieval evidence coverage. Report denominators and per-question outcomes, not only an average. Compare runs on the same questions; with a small set, describe uncertainty rather than asserting a stable winner. Collect provider-reported usage and measured wall-clock time before making cost or speed claims.
