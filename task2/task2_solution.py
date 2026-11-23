import numpy as np
from sentence_transformers import SentenceTransformer

faqs = [
    "What is the company policy on remote work and hybrid schedules?",
    "How many days of paid annual leave do employees receive?",
    "How do I apply for maternity or paternity leave?",
    "What is the dress code for office visits and client meetings?",
    "How do I reset my forgotten active directory password or unlock my account?",
    "How can I request access to company VPN from home?",
    "Who do I contact if my company laptop crashes or won't boot?",
    "How do I set up two-factor authentication on my new phone?",
    "On what date of the month are employee paychecks deposited?",
    "Where can I download my monthly payslips and tax forms?",
    "How do I update my bank account details for direct deposit?",
    "When are annual performance bonuses disbursed?"
]

model = SentenceTransformer("all-MiniLM-L6-v2")
faq_embeddings = model.encode(faqs)

def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def semantic_search(query, top_k=3):
    query_embedding = model.encode(query)
    scores = []
    for idx, emb in enumerate(faq_embeddings):
        sim = cosine_similarity(query_embedding, emb)
        scores.append((sim, faqs[idx]))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]

def keyword_search(query, top_k=3):
    stop_words = {"is", "the", "a", "an", "for", "to", "in", "on", "of", "i", "my", "when", "how", "do"}
    query_words = set(query.lower().split()) - stop_words
    scores = []
    for faq in faqs:
        faq_words = set(faq.lower().replace("?", "").split())
        overlap = len(query_words.intersection(faq_words))
        scores.append((overlap, faq))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top_k]

test_queries = [
    "I cannot log in",
    "when is salary credited",
    "work from home rules",
    "my computer screen is frozen",
    "change where my paycheck goes"
]

print("=== SEARCH RESULTS COMPARISON ===\n")
for q in test_queries:
    kw_top = keyword_search(q, top_k=1)[0]
    sem_top = semantic_search(q, top_k=3)
    kw_result = kw_top[1] if kw_top[0] > 0 else "No exact keyword match found"
    print(f"Query: '{q}'")
    print(f"  -> Keyword Top-1 (matches={kw_top[0]}): {kw_result}")
    print(f"  -> Semantic Top-1 (score={sem_top[0][0]:.3f}): {sem_top[0][1]}")
    print(f"  -> Semantic Top-3: {[(round(s[0], 3), s[1]) for s in sem_top]}\n")

