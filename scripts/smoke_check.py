"""Validate startup, PDF extraction, chunking, and local FAISS without inference.

Run from the repository root after installing the locked dependencies. Provider
keys are replaced with non-secret placeholders within this process only.
"""
import os
from pathlib import Path


def main():
    # Explicit non-secret test values; never read supplied historical credentials.
    os.environ['OPENAI_API_KEY'] = 'offline-validation-placeholder'
    os.environ['GOOGLE_API_KEY'] = 'offline-validation-placeholder'
    os.environ['DEEPSEEK_API_KEY'] = 'offline-validation-placeholder'
    os.environ['LANGCHAIN_TRACING_V2'] = 'false'
    os.environ['LANGSMITH_TRACING'] = 'false'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

    from streamlit.testing.v1 import AppTest
    from pypdf import PdfReader
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_core.embeddings import Embeddings
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    from langchain_ollama import OllamaLLM, OllamaEmbeddings
    from langchain.chains import RetrievalQA

    applications = sorted(Path('apps').rglob('*.py')) + sorted(Path('experiments').glob('*/*.py'))
    applications = [p for p in applications if 'connectivity' not in p.parts]
    results = []
    for path in applications:
        app = AppTest.from_file(str(path), default_timeout=45).run()
        errors = [str(e.message) for e in app.exception]
        results.append({'file':path.as_posix(),'startup_pass':not errors,'error_types':errors})
        print(path.as_posix(), 'PASS' if not errors else 'FAIL', flush=True)

    pages = {}
    for path in sorted(Path('data/filings').glob('*.pdf')):
        documents = PyPDFLoader(str(path)).load()
        assert len(documents) == len(PdfReader(path).pages)
        assert all(d.metadata['page'] == i for i,d in enumerate(documents))
        pages[path.name] = len(documents)
        for size, overlap in [(500,50),(4000,200),(5000,500)]:
            chunks = RecursiveCharacterTextSplitter(chunk_size=size,chunk_overlap=overlap).split_documents(documents)
            assert chunks and all(d.page_content.strip() for d in chunks)
            assert all('page' in d.metadata and 'source' in d.metadata for d in chunks)
        print(path.name, len(documents),'pages extracted; three chunk settings passed',flush=True)

    # Verify FAISS indexing/retrieval wiring with deterministic local vectors only.
    class LocalVectors(Embeddings):
        def embed_documents(self,texts):
            return [self.embed_query(t) for t in texts]
        def embed_query(self,text):
            return [float('revenue' in text),float('risk' in text),float('cloud' in text)]

    store = FAISS.from_texts(['revenue cloud','risk regulation','revenue sales'],LocalVectors())
    assert store.similarity_search('revenue cloud',k=1)[0].page_content == 'revenue cloud'
    assert len(store.max_marginal_relevance_search('revenue',k=2,fetch_k=3)) == 2
    assert all(r['startup_pass'] for r in results)
    print('All startup, PDF extraction, chunking, and deterministic local FAISS checks passed.')


if __name__ == "__main__":
    main()
