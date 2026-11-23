# Task 4: Decision Framework and Technical Proposal

## Part 1: Solution Decision Framework

| Problem | Input Type | Output Type | Constraints (Latency, Cost, Explainability) | Tool Choice | Human-in-the-Loop / AI Usage Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. GST calculation on invoices** | Structured numerical & tax slab fields | Exact currency amount (100% deterministic) | **Latency:** <10ms<br>**Cost:** ~$0<br>**Explainability:** 100% auditable tax rules | **Rule-Based Code (Python / SQL)** | **DO NOT USE AI.** LLMs make arithmetic errors and hallucinate tax rates. Standard code is exact, instant, and legally compliant. |
| **2. Current leave balance of an employee** | Structured Employee ID & date range | Exact integer/float from HR database | **Latency:** <50ms<br>**Cost:** ~$0<br>**Explainability:** Exact database record | **Direct Database / REST API Query** | **DO NOT USE AI** for the lookup itself (optional LLM only as a conversational wrapper over the API). Source of truth must be the HR DB. |
| **3. Ranking resumes for a role** | Unstructured PDFs/DOCX + Job Description | Ranked shortlist & match scores | **Latency:** Seconds to minutes (batch)<br>**Cost:** Low–Moderate<br>**Explainability:** High (must justify rankings & avoid bias) | **Semantic Embeddings + Structured Rubric Scoring** | **MANDATORY HUMAN REVIEW.** AI can shortlist top candidates, but HR/hiring managers must review all decisions to prevent bias and legal/compliance risks. |
| **4. Answering questions from a 60-page contract** | Unstructured 60-page PDF + natural language query | Grounded answer with exact section/page citations | **Latency:** 2–5 seconds<br>**Cost:** Moderate per query<br>**Explainability:** High (must cite exact clauses) | **RAG (Retrieval-Augmented Generation)** | **MANDATORY HUMAN REVIEW.** Legal/operations staff must verify cited clauses before signing or acting on contract terms. |
| **5. Forecasting next month's sales** | Historical tabular time-series data (sales, seasonality, promos) | Numerical forecast + confidence interval | **Latency:** Batch (minutes/hours)<br>**Cost:** Low<br>**Explainability:** Feature importance & trend breakdown | **Classical ML / Time-Series Models (XGBoost, Prophet, ARIMA)** | **HUMAN REVIEW RECOMMENDED.** Finance/sales leadership reviews anomalies and adjusts for upcoming business events not in historical data. |

---

## Part 2: 1-Page Technical Proposal — Contract Q&A System

### 1. Recommended Approach
Build a **Retrieval-Augmented Generation (RAG)** pipeline tailored for legal/commercial contracts:
- **Ingestion & Chunking:** Parse the 60-page PDF using layout-aware extraction (preserving section headers and page numbers) and split into semantic chunks (`500–800 tokens` with `100-token` overlap).
- **Embedding & Vector Store:** Embed chunks using `text-embedding-3-small` (or `all-MiniLM-L6-v2` for local deployment) and store them with metadata (`page_number`, `section_title`) in a vector database (FAISS / Chroma / pgvector).
- **Grounded Generation:** Retrieve the top-5 most relevant clauses via hybrid search (semantic + keyword) and pass them to an LLM (`temperature=0.0`) instructed to **only answer from provided context**, cite exact page/section numbers, and respond *"Information not found in contract"* if the answer is missing.

### 2. Data Requirements
- **Primary Corpus:** Clean, machine-readable PDF/DOCX versions of the 60-page contract (plus OCR preprocessing if scanned).
- **Metadata:** Document version, effective date, page numbers, and clause/section headings.
- **Evaluation Set:** 30–50 realistic Q&A pairs curated by legal/business stakeholders (including 5–10 unanswerable questions to test hallucination refusal).

### 3. Evaluation Metrics & Targets
- **Retrieval Recall@5:** `>= 92%` (the correct contract clause appears in the top 5 retrieved chunks).
- **Citation & Faithfulness Accuracy:** `>= 95%` (every claim in the generated answer is directly supported by the cited clause, verified via LLM-as-a-judge + human spot checks).
- **Hallucination / False-Answer Rate on Unanswerable Queries:** `< 2%`.
- **End-to-End Latency:** `< 4 seconds` per query.

### 4. Estimated Build Time (2 Weeks Total)
- **Days 1–2:** Document parsing, section-aware chunking, and metadata tagging.
- **Days 3–5:** Vector index setup, hybrid retrieval tuning, and grounded prompt engineering.
- **Days 6–8:** Evaluation benchmark creation (40 test questions) and accuracy/latency optimization.
- **Days 9–10:** Simple UI with clickable source citations, security/access controls, and stakeholder handoff.

### 5. Key Trade-Offs
- **RAG vs. Long-Context Stuffing (passing all 60 pages every time):** 60 pages is ~30,000–45,000 tokens. Stuffing the full document into every prompt increases API cost by ~15x, adds latency, and suffers from *"lost-in-the-middle"* accuracy drops. RAG retrieves only ~3,000 tokens of relevant clauses, keeping cost low and citations pinpointed.
- **Strict Grounding vs. Conversational Flexibility:** Setting `temperature=0` and strict refusal prompts prevents dangerous legal hallucinations, at the trade-off of the bot refusing to speculate on ambiguous clauses (which is desirable for legal safety).

---

## Part 3: 3-Minute Presentation & "Why Not Just Ask ChatGPT?"

### 3-Minute Pitch Outline
1. **The Problem (30s):** Teams waste hours manually searching 60-page contracts for payment terms, SLAs, and termination clauses—missing a single detail carries financial risk.
2. **The Solution (60s):** Instead of manual Ctrl+F or risky guesswork, our RAG system indexes the contract by section, retrieves only the relevant clauses, and generates a `temperature=0` answer with exact page citations.
3. **Validation & Timeline (60s):** We validate against 40 stakeholder-written questions targeting `>=95%` citation faithfulness and `<4s` latency, delivered in 10 working days with mandatory human review for final sign-off.
4. **Closing / Why Not Just ChatGPT? (30s):** Address privacy, auditability, hallucination control, and scale (below).

### Answer to: "Why Not Just Ask ChatGPT?"
1. **Data Privacy & Confidentiality:** Uploading confidential 60-page client or vendor contracts into a public consumer ChatGPT interface risks exposing proprietary terms and violating NDAs. Our RAG pipeline runs inside our private cloud/VPC with zero data retention.
2. **Auditability & Exact Citations:** Consumer ChatGPT gives a single blended answer without verifiable page/clause links. Our system forces inline citations (`[Section 4.2, Page 19]`) so a human reviewer can verify the source in seconds.
3. **Hallucination Guardrails:** Standard ChatGPT tries to be helpful and may fill in standard legal assumptions when a clause is missing. Our system uses a strict system prompt (`temperature=0`) that refuses to guess if the clause isn't in the text.
4. **Cost & Scale Across Contracts:** Manually uploading a 60-page PDF in every chat session doesn't scale across a team or across 500 contracts—whereas a vector-indexed RAG system searches across all approved contracts instantaneously at a fraction of the token cost.
