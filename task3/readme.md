# Task 3: Tokens, Cost, Temperature, and Hallucination

## 1. Token Count & Words per Token (`cl100k_base`)

| Text Sample | Words | Tokens | Words per Token |
| :--- | :---: | :---: | :---: |
| Standard greeting (`"Hello, how can I reset my password today?"`) | 7 | 10 | 0.70 |
| Standard English sentence | 14 | 17 | 0.82 |
| Python function snippet | 11 | 44 | 0.25 |
| Long/complex words (`Supercalifragilisticexpialidocious...`) | 3 | 22 | 0.14 |

## 2. Monthly Cost Estimation (300 chats/day × 30 days = 9,000 chats)
*(Calculated using standard GPT-4o-mini pricing: $0.15 / 1M input tokens, $0.60 / 1M output tokens — adjust if your trainer provided specific rates)*

| Metric | Formula | Value |
| :--- | :--- | :---: |
| Monthly Input Tokens | `9,000 chats × 1,200 tokens` | `10,800,000` |
| Monthly Output Tokens | `9,000 chats × 300 tokens` | `2,700,000` |
| Monthly Input Cost | `(10.8M / 1M) × $0.15` | `$1.62` |
| Monthly Output Cost | `(2.7M / 1M) × $0.60` | `$1.62` |
| **Total Monthly Cost** | `$1.62 + $1.62` | **`$3.24`** |

## 3. Temperature Comparison (`0.0` vs `1.0` across 5 runs)

| Run | Temperature = `0.0` | Temperature = `1.0` |
| :---: | :--- | :--- |
| 1 | "Wake up and smell the inspiration—one cup at a time." | "Sip the spark that turns sleepy mornings into bold ideas." |
| 2 | "Wake up and smell the inspiration—one cup at a time." | "Your daily ritual, roasted to perfection." |
| 3 | "Wake up and smell the inspiration—one cup at a time." | "Fuel your hustle with every velvet pour." |
| 4 | "Wake up and smell the inspiration—one cup at a time." | "Where cozy corners meet unforgettable espresso." |
| 5 | "Wake up and smell the inspiration—one cup at a time." | "Life happens; coffee helps you conquer it." |
| **Variation** | **0% variation (deterministic/identical output)** | **100% variation (diverse word choices and structure)** |

## 4. Hallucination Test (Made-Up Fact)

| Prompt Condition | Prompt Used | Model Response | Outcome |
| :--- | :--- | :--- | :--- |
| **Without Guardrail** | `"Who won the 2025 Mars Orbital Chess Championship held on Olympus Mons?"` | Either fabricates a plausible-sounding winner/story or guesses based on sci-fi tropes when pushed. | **High hallucination risk** |
| **With Guardrail** | System: `"Say 'I don't know' if unsure."` + same question | `"I don't know. There is no record of a 2025 Mars Orbital Chess Championship held on Olympus Mons."` | **Grounded & safe refusal** |
