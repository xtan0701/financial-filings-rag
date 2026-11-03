# Verification record

Validation was performed on November 3, 2026, on Windows with Python 3.12.4. This record distinguishes mechanical reproducibility checks from model evaluation.

| Check | Executed result | What it establishes |
| --- | --- | --- |
| Isolated environment installation | Passed; exact installed packages in `requirements-lock.txt` | Dependency installation for this Windows environment |
| `python -m pip check` | No broken requirements | Declared dependency compatibility |
| Streamlit `AppTest` initial execution | All 13 application pages passed with non-secret placeholder keys | Initial UI execution and imports, before uploads or inference |
| Filing extraction through `PyPDFLoader` | 99 / 89 / 221 pages, matching each PDF | Page extraction and sequential metadata indices |
| Character splitting | All three PDFs passed at 500/50, 4,000/200, and 5,000/500 | Nonempty chunks retaining source and page metadata |
| Deterministic local FAISS exercise | Similarity and MMR retrieval passed on a tiny synthetic corpus | Local indexing and retriever wiring, not semantic model quality |
| Filing integrity | All three SHA-256 hashes and byte sizes matched the input snapshots | Input bytes preserved |
| Source coverage | 27 Python file/ZIP members represented by 16 distinct sanitized implementations | No distinct technical variant discarded during deduplication |
| Credential removal | Common-pattern scan and exact comparison against original credential values found no public matches | Checked public files do not contain those original keys |
| Syntax and relative documentation links | Passed using the offline integrity script | Public Python parses; linked local paths exist |

Re-run the standard-library checks with:

```powershell
python scripts/verify_repository.py
```

Re-run the dependency-based checks after installing `requirements-lock.txt`:

```powershell
python -m pip check
python scripts/smoke_check.py
```

The [smoke script](../scripts/smoke_check.py) replaces credentials with placeholders inside its own process. It starts pages without uploading documents to the applications. PDF extraction, chunking, and FAISS checks run separately and locally. It never calls provider inference.

## Warnings and unverified scope

The Google integration emits a warning that `google.generativeai` is no longer maintained. The locked legacy stack preserves the existing implementation; migrating to the replacement SDK would require separate compatibility work. Streamlit's test harness also emits missing-context warnings from its main thread; there were no application exceptions in the startup checks.

Cloud answer generation, actual provider embeddings, model availability, Ollama downloads/inference, user-upload error handling, browser rendering, and Linux/macOS installation were not verified. No model accuracy, latency, cost, or business-impact result follows from these checks. Existing prototype limitations remain listed in the [evaluation document](evaluation.md).
