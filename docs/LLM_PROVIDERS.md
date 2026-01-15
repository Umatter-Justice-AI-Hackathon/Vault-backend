# LLM Provider Comparison

## Free Options (Recommended for MVP)

### 🥇 Groq (BEST FREE OPTION)
**Why:** Ultra-fast inference on custom LPU hardware
- **Cost:** FREE (generous limits)
- **Limits:** 30 requests/min, 14,400/day
- **Speed:** ⚡ Fastest (2-10x faster than others)
- **Models:** Llama 3.1 70B, Mixtral 8x7B, Gemma 2
- **Quality:** Excellent for mental health conversations
- **Get API Key:** https://console.groq.com/keys

**Recommended model:** `llama-3.1-70b-versatile`

### Hugging Face Inference API
**Why:** Access to many open models
- **Cost:** FREE (with rate limits)
- **Limits:** Varies by usage
- **Speed:** Moderate to slow
- **Models:** Llama, Mistral, many others
- **Quality:** Good, depends on model
- **Get API Key:** https://huggingface.co/settings/tokens

**Recommended model:** `meta-llama/Llama-3.1-70B-Instruct`

## Paid Options (For Scale)

### OpenAI
- **Cost:** ~$0.60/1000 conversations (GPT-4o-mini)
- **Speed:** Fast
- **Quality:** Excellent, very reliable
- **Best for:** Production at scale

### Anthropic Claude
- **Cost:** Similar to OpenAI
- **Speed:** Fast
- **Quality:** Excellent, especially for nuanced conversations
- **Best for:** High-quality empathetic responses

## Local Development

### Ollama
- **Cost:** FREE (uses your hardware)
- **Speed:** Depends on your machine
- **Quality:** Good with llama3.1:8b
- **Best for:** Local development without internet

## Recommendation for Umatter

**Development:** Ollama (local, free, private)
**Production (MVP):** Groq (free, fast, excellent quality)
**Production (Scale):** OpenAI GPT-4o-mini (paid but reliable)

## Why Groq is Perfect for Umatter

1. **FREE** - No cost for MVP and early users
2. **FAST** - Near-instant responses improve UX
3. **QUALITY** - Llama 3.1 70B is excellent for empathetic conversations
4. **LIMITS** - 14,400 requests/day = 480 users having 30 messages each
5. **EASY** - Simple API, similar to OpenAI

## Setup Instructions

### For Groq (Recommended)

1. Go to https://console.groq.com/
2. Sign up (free, no credit card required)
3. Navigate to API Keys
4. Create a new API key
5. Add to `.env`:
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your_key_here
   ```

### For Hugging Face

1. Go to https://huggingface.co/
2. Sign up (free)
3. Go to Settings → Access Tokens
4. Create a new token
5. Add to `.env`:
   ```
   LLM_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=hf_your_key_here
   ```

## Render Deployment

Set environment variables in Render dashboard:
- `LLM_PROVIDER=groq`
- `GROQ_API_KEY=gsk_...`

That's it! No infrastructure, no model management, just works.
