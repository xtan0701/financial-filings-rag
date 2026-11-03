# Reproduction guide

## Environment

Run from the repository root with Python 3.12. `requirements.txt` constrains the legacy LangChain 0.3 API used by the source. `requirements-lock.txt` records the environment actually installed for validation. This is a Windows verification record, not a claim of cross-platform validation.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python -m pip check
python scripts/verify_repository.py
```

If intentionally re-resolving dependencies, install `requirements.txt` instead. A newer major LangChain version changes import paths and is outside this reproduction protocol.

## Credentials

Use fresh keys belonging to your own provider accounts. In PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-own-key"
$env:GOOGLE_API_KEY = "your-own-key"
$env:DEEPSEEK_API_KEY = "your-own-key"
```

Set only the keys needed for the chosen pipeline. `.env.example` documents names, but the scripts do not load `.env`. Do not put real keys into source code or commit them. The DeepSeek scripts retain their original OpenAI-compatible client configuration within their own process.

| Pipeline | Credentials / service |
| --- | --- |
| Primary or baseline OpenAI | `OPENAI_API_KEY` |
| Gemini PDF or Gemini chat | `GOOGLE_API_KEY` |
| DeepSeek PDF | `DEEPSEEK_API_KEY` and `GOOGLE_API_KEY` for embeddings |
| Financial Ollama | Running Ollama with Mistral; `GOOGLE_API_KEY` for embeddings |
| Basic or generic-history Ollama PDF | Running Ollama with Mistral and nomic-embed-text; no cloud key |
| Plain Ollama chat | Running Ollama with deepseek-r1:14b |
| Connection probes | Service corresponding to the probe |

For the fully local PDF baseline, prepare `mistral` and `nomic-embed-text` in Ollama. This model download and local inference were not executed during public-repository validation.

## Launch and review

```powershell
python -m streamlit run apps/openai_pdf.py
```

For another application, substitute a path from the [experiment catalogue](experiments.md), for example:

```powershell
python -m streamlit run experiments/financial/chat_with_pdf_ds_with_history.py
python -m streamlit run experiments/baselines/chat_with_pdf_ollama.py
```

Upload the desired PDFs from `data/filings/`. Begin with a single-company disclosure question and manually verify its answer. For multi-company comparisons, upload all required reports and explicitly name fiscal periods. Start a fresh session when changing uploads; the scripts do not rebuild an existing index automatically.

Some variants initialize cloud clients at script startup, so they require credentials even before an upload. Cloud model availability, account access, quotas, and Ollama model installation are external requirements. No supplied historical credential is used by this protocol.

## Verification scope

`scripts/verify_repository.py` uses only Python's standard library to verify syntax, public-file secret patterns, local documentation links, filing hashes, and manifest sizes. It does not execute model calls. See the [verification record](verification.md) for checks actually performed and the [evaluation protocol](evaluation.md) for work that remains unrun.

After dependency installation, `python scripts/smoke_check.py` repeats initial UI execution, PDF extraction and splitting, and a deterministic local FAISS check. It uses placeholder credentials and makes no inference calls.

The retained Google SDK emits an end-of-support warning. The pinned environment reproduces this legacy implementation; it is not a claim of support for current Google models or a production deployment recommendation.
