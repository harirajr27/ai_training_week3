# Task 2: Embeddings and Semantic Search

## Comparison Table

| Query | Keyword Result (Top-1) | Semantic Result (Top-1) |
| :--- | :--- | :--- |
| `I cannot log in` | No exact keyword match found | How do I reset my forgotten active directory password or unlock my account? |
| `when is salary credited` | No exact keyword match found | On what date of the month are employee paychecks deposited? |
| `work from home rules` | How can I request access to company VPN from home? | What is the company policy on remote work and hybrid schedules? |
| `my computer screen is frozen` | No exact keyword match found | Who do I contact if my company laptop crashes or won't boot? |
| `change where my paycheck goes` | Where can I download my monthly payslips and tax forms? | How do I update my bank account details for direct deposit? |

## 2 Queries Where Semantic Search Wins (and Why)

1. **`when is salary credited`**
   - **Why it wins:** Keyword search fails completely because the FAQ uses *"date"*, *"paychecks"*, and *"deposited"* instead of *"salary"* or *"credited"*. Semantic embeddings understand that "salary credited" and "paychecks deposited" share the exact same payroll meaning.
2. **`my computer screen is frozen`**
   - **Why it wins:** Keyword search finds zero matching words with *"Who do I contact if my company laptop crashes or won't boot?"*. Semantic search maps *"computer screen is frozen"* close to *"laptop crashes or won't boot"* in vector space because both describe hardware failure symptoms.
