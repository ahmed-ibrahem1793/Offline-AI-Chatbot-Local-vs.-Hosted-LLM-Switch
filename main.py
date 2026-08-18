import argparse, os, time
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--hosted", action="store_true", help="Use Grok instead of local Ollama")
args = parser.parse_args()
groq_api_key=os.environ.get("GROQ_API_KEY")

if args.hosted:
    base_url="https://api.groq.com/openai/v1"
    model = "groq/compound"
    api_key = groq_api_key
    print(f"[Hosted mode | {model} | requires internet + API key | higher quality]")
else:
    base_url="http://localhost:11434/v1"
    model = "qwen2.5:0.5b"
    api_key = "dummy_key"
    print(f"[Local mode | {model} | offline, free, lower VRAM | weaker reasoning]")

client = OpenAI(
        base_url = base_url,
        api_key = api_key
    )
messages=[]
while True:
    prompt = input("Enter your prompt: ")
    if prompt.lower() in ("exit", "quit"): break

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        start = time.time()
        request = client.chat.completions.create(
            messages=messages,
            model= model,
        )
        elapsed = time.time() - start

    except Exception as e:
        print(f"Error: {e}. Check your connection/API key/Ollama server.")
        messages.pop()
        continue

    messages.append({
        "role": "assistant",
        "content": request.choices[0].message.content
    })

    usage = request.usage 
    tok_per_sec = usage.completion_tokens / elapsed if elapsed > 0 else 0
    print(f"[{elapsed:.2f}s | {tok_per_sec:.1f} tok/s]")
    print('------\n' + request.choices[0].message.content + '\n------')
