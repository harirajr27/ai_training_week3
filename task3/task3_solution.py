import os
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

enc = tiktoken.get_encoding("cl100k_base")

texts = [
    "Hello, how can I reset my password today?",
    "Artificial intelligence models process text by breaking sentences down into smaller subword units called tokens.",
    "def calculate_monthly_cost(chats_per_day, input_tokens, output_tokens, in_price, out_price): return ((chats_per_day * 30 * input_tokens / 1_000_000) * in_price) + ((chats_per_day * 30 * output_tokens / 1_000_000) * out_price)",
    "Supercalifragilisticexpialidocious electroencephalographically antidisestablishmentarianism!"
]

print("=== 1. TOKEN COUNT & WORDS PER TOKEN ===")
for i, t in enumerate(texts, 1):
    tokens = enc.encode(t)
    word_count = len(t.split())
    token_count = len(tokens)
    wpt = round(word_count / token_count, 2)
    print(f"Text {i}: Words={word_count} | Tokens={token_count} | Words/Token={wpt}")

chats_per_day = 300
days = 30
total_chats = chats_per_day * days
total_input_tokens = total_chats * 1200
total_output_tokens = total_chats * 300

input_price_per_1m = 0.15
output_price_per_1m = 0.60

monthly_input_cost = (total_input_tokens / 1_000_000) * input_price_per_1m
monthly_output_cost = (total_output_tokens / 1_000_000) * output_price_per_1m
total_monthly_cost = monthly_input_cost + monthly_output_cost

print("\n=== 2. MONTHLY COST ESTIMATE ===")
print(f"Total Monthly Chats: {total_chats}")
print(f"Total Input Tokens: {total_input_tokens:,} | Cost: ${monthly_input_cost:.2f}")
print(f"Total Output Tokens: {total_output_tokens:,} | Cost: ${monthly_output_cost:.2f}")
print(f"Total Monthly Cost: ${total_monthly_cost:.2f}")

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
    model_name = "gpt-4o-mini"

    print("\n=== 3. TEMPERATURE COMPARISON (0.0 vs 1.0) ===")
    prompt_temp = "Give me a creative one-sentence tagline for a coffee shop."
    for temp in [0.0, 1.0]:
        print(f"\n--- Temperature = {temp} ---")
        for run in range(1, 6):
            res = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt_temp}],
                temperature=temp,
                max_tokens=40
            )
            print(f"Run {run}: {res.choices[0].message.content.strip()}")

    print("\n=== 4. HALLUCINATION TEST ===")
    fake_question = "Who won the 2025 Mars Orbital Chess Championship held on Olympus Mons?"
    res_no_guard = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": fake_question}],
        temperature=0.7,
        max_tokens=80
    )
    res_with_guard = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Answer accurately. Say 'I don't know' if unsure."},
            {"role": "user", "content": fake_question}
        ],
        temperature=0.7,
        max_tokens=80
    )
    print(f"Without guardrail: {res_no_guard.choices[0].message.content.strip()}")
    print(f"With guardrail: {res_with_guard.choices[0].message.content.strip()}")
else:
    print("\n[Note: Set OPENAI_API_KEY in a local .env file to run live API calls for Points 3 & 4]")
