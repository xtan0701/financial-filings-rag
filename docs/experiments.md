# Implemented experiments

All paths below are maintained as reviewable technical alternatives. Exact duplicates and credential-only differences have a single public implementation. All distinct model, prompt, retrieval, and chunking variants found in the source files and ZIP members are represented. Historical originals remain local, outside the public file set.

Chunk sizes and overlaps are **characters**, not tokens. `MMR` below means `k=4`, `fetch_k=20`, `lambda_mult=0.7`. Defaults mean the application leaves that setting to its dependency version.

## Document applications

| Implementation | Generation / embeddings | Chunk / overlap | Retrieval | Conversation and evidence |
| --- | --- | --- | --- | --- |
| [Primary OpenAI](../apps/openai_pdf.py) | GPT-4o / OpenAI default | 5,000 / 500 | Similarity defaults | Display history only; no source panel |
| [OpenAI baseline](../experiments/baselines/chat_with_pdf_openai.py) | GPT-4o / OpenAI default | 500 / 50 | Similarity defaults | Display history only; no source panel |
| [Gemini baseline](../experiments/baselines/chat_with_pdf_gemini.py) | Gemini 2.0 Flash / Google embedding-001 | 500 / 50 | MMR | Generic instructions in query; source panel |
| [Local Ollama baseline](../experiments/baselines/chat_with_pdf_ollama.py) | Mistral / nomic-embed-text | 500 / 50 | MMR | Generic instructions in query; source panel |
| [Gemini generic history](../experiments/baselines/chat_with_pdf_gemini_generic_history.py) | Gemini 2.0 Flash / Google embedding-001 | 500 / 50 | MMR | History in query; generic persona; source panel |
| [Ollama generic history](../experiments/baselines/chat_with_pdf_ollama_generic_history.py) | Mistral / nomic-embed-text | 500 / 50 | MMR | History in query; generic persona; source panel |
| [Gemini 4,000](../experiments/retrieval/chat_with_pdf_gemini_4000.py) | Gemini 2.0 Flash / Google embedding-001 | 4,000 / 200 | MMR | Financial persona and history in query; source panel |
| [DeepSeek 4,000](../experiments/retrieval/chat_with_pdf_ds_4000.py) | DeepSeek Reasoner / Google embedding-001 | 4,000 / 200 | MMR | Financial persona and history in query; source panel |
| [Gemini financial](../experiments/financial/chat_with_pdf_gemini_with_history.py) | Gemini 2.0 Flash / Google embedding-001 | 5,000 / 500 | MMR | **Generic persona actually used**; financial persona defined but unused; history and source panel |
| [DeepSeek financial](../experiments/financial/chat_with_pdf_ds_with_history.py) | DeepSeek Reasoner / Google embedding-001 | 5,000 / 500 | MMR | Financial persona and history in query; source panel |
| [Ollama financial](../experiments/financial/chat_with_pdf_ollama_with_history.py) | Mistral / Google embedding-001 | 5,000 / 500 | MMR | Financial persona and history in query; source panel; cloud embeddings |

The primary and baseline OpenAI configurations use temperature 0.5. The basic Gemini, basic Ollama, and generic-history configurations also use 0.5. Financial and 4,000-character variants use 0.0. This is another reason their outputs would not constitute a one-factor comparison.

## Plain chat and connection probes

| Implementation | Purpose |
| --- | --- |
| [Gemini plain chat](../experiments/baselines/chat_with_gemini.py) | Streamlit chat without document retrieval |
| [Ollama plain chat](../experiments/baselines/chat_with_local_ollama.py) | Streamlit chat using `deepseek-r1:14b`, despite the generic filename |
| [DeepSeek Chat probe](../experiments/connectivity/deepseek_chat.py) | Direct `ChatOpenAI` connection to DeepSeek |
| [DeepSeek base probe](../experiments/connectivity/deepseek_base_chat.py) | Direct `BaseChatOpenAI` connection to DeepSeek |
| [Ollama probe](../experiments/connectivity/ollama_chat.py) | Minimal Mistral invocation |

These three probes call providers when run. They are not unit tests and do not run as part of offline verification.

## Reading comparisons correctly

Use the 500/50 generic-history variants to inspect the distinction between fully local and cloud pipelines. Use the 4,000-character variants to inspect the same domain persona with a smaller chunk configuration. Use the 5,000-character variants to inspect the final set of provider integrations.

The source panel displays the loader's page index, which is generally zero-based, without converting it to a printed filing page. Some source panels omit the document filename. Match the passage manually to the correct report before treating it as a citation. Provider behavior, cost, latency, and factuality have not been ranked.
