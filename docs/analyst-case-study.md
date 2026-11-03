# Analyst case study

## Research problem

Annual reports contain narrative disclosures, financial statements, segment tables, and risk discussions across many pages. The practical question is whether a document-grounded assistant can help an analyst locate relevant information while keeping the original filing available for verification.

The corpus covers Amazon, Alphabet, and Microsoft. Useful research tasks include locating revenue components, comparing segment disclosures with their fiscal periods intact, and finding management's discussion of operating risks. The implemented financial persona requests structured answers, source references, and an explicit response when the provided documents do not support an answer.

## Source inspection before model selection

The snapshots have 99 pages for Alphabet, 89 for Amazon, and 221 for Microsoft. Microsoft's PDF is a printed filing with browser headers and footers. Page extraction can therefore introduce repeated nonfinancial text, and PDF page positions can differ from printed report page numbers.

Microsoft FY2024 ends six months before the calendar year-end used by the other two companies. A cross-company answer must state those periods, rather than silently treating the reports as an aligned twelve-month panel. The snapshots preserve the available reports; they do not establish a point-in-time investment information set.

The [data manifest](../data/manifest.csv) makes these inputs auditable through byte counts and SHA-256 hashes. The snapshot bytes have not been rewritten during preparation.

## Implemented work and its analytical purpose

| Work visible in the code | What a reviewer can assess | Evidence boundary |
| --- | --- | --- |
| Standalone provider connection probes | Whether model access was separated from PDF retrieval | Connectivity code does not measure answer quality |
| Plain chat and basic PDF variants | How document grounding changes the architecture | No paired answer outputs were retained |
| OpenAI, Gemini, DeepSeek, and Ollama integrations | Ability to implement different provider interfaces and data flows | Provider availability today is not guaranteed by historical model names |
| 500/50, 4,000/200, and 5,000/500 chunk settings | Tradeoff between context breadth, overlap, and retrieval granularity | Configuration choices are not a controlled experiment |
| Similarity and MMR retrieval | Implementation of relevance and diversity alternatives | Changing the LLM, embeddings, and chunking together prevents attribution |
| Financial analyst persona | Translation of research requirements into answer instructions | Instructions do not enforce factuality or verified citations |
| Retrieved-passage display in selected variants | Ability to expose evidence for manual checking | Retrieved passages do not prove the answer used them correctly |
| History handling | Understanding of stateful analyst questions | Some variants display history only; others mix it into retrieval |

This table describes implemented work and the questions it enables. It does not claim that the original development followed a documented chronological experimental plan: no such log was supplied.

## Design implications

Larger chunks may keep a financial table and its explanatory context together, but can also dilute retrieval and consume more tokens. MMR may reduce repeated passages, but a fixed four-passage answer context may omit evidence needed for a multi-company comparison. Those implications motivate evaluation; they are not measured improvements in this project.

The financial persona asks for disclosure-based analysis, explicit uncertainty, no stock-price predictions, and source references. In the history-enabled implementation, that text is formatted into the query passed to `RetrievalQA`. It is not installed as an independently enforced system-level policy. The query used for retrieval includes persona text and prior messages, so a successful-looking response alone cannot isolate the value of the persona.

The final OpenAI entry point is simpler: 5,000-character chunks, 500-character overlap, OpenAI embeddings, FAISS, and GPT-4o generation at temperature 0.5. It has a chat interface but does not pass previous messages to the model or expose retrieved passages. It should not be described as the empirically best configuration.

## Review judgment

The strongest evidence here is the breadth of implemented alternatives, explicit domain constraints, traceable corpus, and the ability to explain implementation weaknesses. The available materials do not support a claim about accuracy uplift, hours saved, production readiness, or which provider wins.

A defensible next study would hold corpus, questions, embeddings, and retrieval settings fixed while varying one factor at a time. It would score factual correctness, citation support, abstention, and period/unit handling against manually checked filing evidence. The [evaluation protocol](evaluation.md) defines that study without presenting unrun experiments as results.
