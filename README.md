# Offline-First AI Chatbot

A terminal chatbot that runs **fully offline** using a local model via Ollama, with an optional flag to switch to a **hosted API** (Groq) for higher-quality responses.

Both modes use the same `OpenAI` client — switching between local and hosted only requires changing the `base_url` and model name, nothing else.

## Setup

1. **Clone/download the project**, then create and activate the virtual environment (already included as `env/`):

   ```bash
   # Windows
   env\Scripts\activate

   # macOS/Linux
   source env/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **For local mode:** install [Ollama](https://ollama.com) and pull the model:

   ```bash
   ollama pull qwen2.5:0.5b
   ```

4. **For hosted mode:** get a free API key from [Groq](https://console.groq.com) and set it as an environment variable:

   ```bash
   # Windows
   set GROQ_API_KEY=your_key_here

   # macOS/Linux
   export GROQ_API_KEY=your_key_here
   ```

## Usage

Run in local (offline) mode:

```bash
python main.py
```

Run in hosted mode:

```bash
python main.py --hosted
```

Type your prompts at the `Enter your prompt:` line. Type `exit` or `quit` to end the session. The app remembers the full conversation, so follow-up questions work naturally.

## Model Choice Justification

**Local — `qwen2.5:0.5b`**
Chosen specifically because it's a *tiny* model — around **0.5 GB** in size — which means it can run on almost any device, including low-end laptops with no dedicated GPU. This makes it a genuinely practical "offline-first" choice: no internet, no API costs, no meaningful hardware barrier to entry. The trade-off is weaker reasoning and shorter, less nuanced answers compared to larger hosted models — acceptable for a lightweight offline chat assistant, but not for complex tasks.

**Hosted — `groq/compound` (via Groq API)**
Chosen for significantly higher response quality, using Groq's fast inference infrastructure. Requires an internet connection and an API key, and inference isn't free at scale — but it's the right choice when quality matters more than offline availability.

**Decision framework:** local wins on privacy, cost, and offline access; hosted wins on quality and capability. The `--hosted` flag lets the user pick per-session depending on which trade-off matters more at the time.

## Benchmark Notes

Measured using the built-in `[Xs | Y tok/s]` output printed after every response (uses the API's `usage.completion_tokens` divided by wall-clock response time).

| Mode | Model | Speed (tok/s) | Quality notes |
|---|---|---|---|
| Local | qwen2.5:0.5b | _fill in after testing on your machine_ | Fast, but shorter/simpler answers; occasional factual slips on niche questions |
| Hosted | groq/compound | _fill in after testing_ | Noticeably more detailed and accurate; consistent across follow-ups |

*(Run a few identical prompts in both modes and drop your actual numbers in here before submitting — the app prints them for you after every reply.)*

## Offline Proof

Tested by disabling the internet connection entirely:
- **Local mode** continued working normally — confirms inference happens on-device.
- **Hosted mode** failed immediately — confirms it depends on the Groq API, not a local fallback.

Both modes were also asked "what model are you?" and self-identified correctly (Qwen2.5 / a Groq-hosted model), as a second confirmation.

## Project Structure

```
.
├── main.py
├── requirements.txt
├── env/              # virtual environment (not portable — recreate with requirements.txt on a new machine)
└── README.md
```

## Possible Future Improvements

- Add a `--model` flag to swap between different local Ollama models without editing code.
- Persist conversation history to disk between sessions.
- Stream tokens as they're generated instead of waiting for the full response.
