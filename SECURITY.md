# Credential handling

The public code reads `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and `DEEPSEEK_API_KEY` from environment variables. The repository distributes no usable provider key. Users supply their own credentials; deployed services should inject secrets through their hosting platform. GitHub Actions should use repository or environment Secrets if provider calls are added later.

`.env`, `.env.*` other than `.env.example`, and `.streamlit/secrets.toml` are ignored. Ignoring a file does not remove it from existing Git history. Scan staged content before committing, including any newly added binary or archive. The offline verification script detects selected common credential patterns; it is not an exhaustive secret detector.

If a real credential has been shared or committed, revoke or rotate it at the provider first. Removing the text is not revocation. Follow [GitHub's sensitive-data guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) for any repository history that contains secrets. Never post keys in issues, screenshots, or error reports.
