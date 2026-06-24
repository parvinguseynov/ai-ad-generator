# AI Multi-Platform Ad Generator

An AI-powered web service that turns a single business description into ready-to-use
advertising content for three different social media platforms — each with its own
tone of voice. Built with FastAPI and the Anthropic Claude API.

The user provides only two inputs (business name and product/service), and the service
returns tailored content for **Instagram**, **Facebook**, and **TikTok** in one response.

---

## Features

- **Single input, three outputs** — one request generates platform-specific content for Instagram, Facebook, and TikTok.
- **Platform-aware tone** — each platform uses a dedicated prompt with its own voice (inspiring lifestyle for Instagram, detailed and trustworthy for Facebook, bold and punchy for TikTok).
- **Strict output validation** — every AI response is parsed and validated against a schema before it reaches the user, so malformed or incomplete output never gets through.
- **Automatic retry** — if the model returns invalid content, the request is retried before failing.
- **Honest error handling** — if generation cannot be validated, the API returns a clear error instead of crashing.
- **Secure configuration** — the API key is read from an environment variable and is never committed to the repository.

---

## Tech Stack

- **Python 3.13**
- **FastAPI** — web framework (request handling, automatic validation, auto-generated docs)
- **Pydantic** — input and output validation through typed schemas
- **Anthropic Claude API** — content generation (`claude-sonnet-4-6`)
- **python-dotenv** — loads the API key from a `.env` file

---

## Project Structure

```
ad_generation/
├── main.py            # FastAPI app and the /generate endpoint
├── schemas.py         # Pydantic schemas for input and platform outputs
├── prompts.py         # Prompt builder functions, one per platform
├── generator.py       # Claude client, validation, retry and orchestration
├── requirements.txt   # Direct dependencies with pinned versions
├── .env.example       # Template for required environment variables
└── README.md
```

Each file has one clear responsibility: schemas describe the shape of data, prompts
describe the instructions for the model, and the generator connects them to the API
and validates the result.

---

## Setup and Installation

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd ad_generation
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure the API key**

Copy the example file and add your Anthropic API key:

```bash
cp .env.example .env
```

Then open `.env` and set your key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**5. Run the server**

```bash
python -m uvicorn main:app --reload
```

The API is now available at `http://127.0.0.1:8000`, and the interactive
documentation at `http://127.0.0.1:8000/docs`.

---

## Usage

Send a `POST` request to `/generate` with a business name and a product/service description:

**Request**

```json
{
  "business": "Bean & Brew",
  "product": "specialty coffee and pastries"
}
```

The response contains content for all three platforms (see examples below).

You can test the endpoint directly from the interactive docs at `/docs` — no extra
tools required.

---

## Prompt Design

Prompt design is the core of this project. Instead of using one generic prompt for all
platforms, each platform has its own dedicated prompt builder. This is what produces
genuinely different tones rather than three near-identical texts.

Every prompt follows the same four-part structure:

1. **Role** — the model is told it is an expert copywriter for that specific platform.
2. **Task and data** — the business name and product are injected into the prompt.
3. **Constraints** — platform-specific tone, length, and format rules.
4. **Output format** — the model is required to return strict JSON matching the schema.

The tone constraints are deliberately different for each platform:

- **Instagram** — warm, lifestyle-oriented, visually evocative caption (2–3 sentences) with at least 5 hashtags. Goal: inspire.
- **Facebook** — detailed, informative copy (5–6 sentences) explaining the product's benefits, in a mature and trustworthy tone, ending with a strong call to action. Goal: convince and convert.
- **TikTok** — one short, bold, conversational hook designed to stop the scroll instantly. Goal: grab attention.

Because the model is asked to return JSON, but cannot be fully trusted to always comply,
every response is cleaned (to remove markdown wrappers), parsed, and validated against a
Pydantic schema. For example, Instagram output is rejected if it contains fewer than 5
hashtags. If validation fails, the request is retried once before returning an error.

---

## Examples

### Example 1 — Coffee Shop

**Input**

```json
{
  "business": "Bean & Brew",
  "product": "specialty coffee and pastries"
}
```

**Output**

```json
{
  "instagram": {
    "caption": "Some mornings deserve to be savored slowly ☕✨ At Bean & Brew, every cup is crafted with care and every pastry baked with love — because the perfect start to your day is always worth it. Pull up a chair, breathe it all in, and let the magic begin. 🥐",
    "hashtags": ["#BeanAndBrew", "#SpecialtyCoffee", "#CoffeeCommunity", "#MorningVibes", "#PastryLove", "#CafeLife", "#SlowMornings"]
  },
  "facebook": {
    "text": "At Bean & Brew, we believe every cup of coffee should be an experience worth savoring. Our specialty coffees are sourced from small, sustainable farms around the world, carefully roasted to bring out the richest and most complex flavors in every single sip. Paired with our freshly baked pastries — made from scratch each morning using real, wholesome ingredients — you have the perfect combination to start your day right. Whether you prefer a velvety latte, a bold espresso, or a flaky butter croissant, our skilled baristas and bakers pour their passion into everything they create. We are committed to quality, consistency, and giving you a warm, welcoming experience every time you walk through our doors or place an order. Treat yourself to something truly exceptional — because you deserve more than an ordinary coffee run.",
    "cta": "Visit us today or order online and taste the Bean & Brew difference for yourself!"
  },
  "tiktok": {
    "hook": "Your coffee shop is lying to you — and we're done letting it happen."
  }
}
```

### Example 2 — Fitness Studio

**Input**

```json
{
  "business": "PulseFit Studio",
  "product": "group fitness classes and personal training"
}
```

**Output**

```json
{
  "instagram": {
    "caption": "Every great transformation begins with a single step through our doors. 💪 At PulseFit Studio, our group classes and personal training sessions are designed to push your limits, lift your energy, and surround you with people who cheer you on. Your strongest self is waiting — let's go find it together. 🔥",
    "hashtags": ["#PulseFitStudio", "#FitnessMotivation", "#GroupFitness", "#PersonalTraining", "#FitLife", "#WorkoutCommunity", "#TransformYourself"]
  },
  "facebook": {
    "text": "At PulseFit Studio, we believe that fitness is more than just a workout — it's a lifestyle transformation backed by expert guidance and a supportive community. Our energizing group fitness classes are designed for all levels, from beginners to seasoned athletes, ensuring everyone feels challenged and motivated. With certified personal trainers dedicated to your individual goals, you'll receive customized programming that delivers real, measurable results. Our state-of-the-art studio creates the perfect environment to stay consistent, accountable, and genuinely excited about your health journey. Hundreds of members have already discovered what it feels like to look forward to every single workout — and now it's your turn. Whether you're looking to build strength, improve endurance, or simply feel better every day, PulseFit Studio has everything you need to succeed.",
    "cta": "Claim your free trial class today and take the first step toward a stronger, healthier you!"
  },
  "tiktok": {
    "hook": "You've been doing the same workout for months and wondering why nothing's changing — yeah, we need to talk."
  }
}
```

### Example 3 — Online Clothing Store

**Input**

```json
{
  "business": "Urban Thread",
  "product": "online clothing and accessories store"
}
```

**Output**

```json
{
  "instagram": {
    "caption": "Every outfit tells a story — make yours unforgettable. ✨ At Urban Thread, we curate pieces that move with your life, from sun-soaked mornings to city nights that never slow down. 🌆 Dress like the main character you've always been.",
    "hashtags": ["#UrbanThread", "#StyleYourStory", "#FashionForward", "#OOTDInspo", "#WearYourVibe", "#UrbanStyle", "#OnlineFashion"]
  },
  "facebook": {
    "text": "Discover your signature style with Urban Thread, your go-to online destination for premium clothing and accessories that blend modern trends with timeless elegance. Every piece in our carefully curated collection is crafted with quality materials designed to keep you looking polished and feeling confident, whether you're dressing for the office or a weekend out. We believe great fashion should be accessible, which is why we offer competitive pricing without ever compromising on craftsmanship or style. Shopping with us is effortless — enjoy a seamless browsing experience, secure checkout, and fast reliable shipping straight to your door. Our dedicated customer support team is always on hand to help you find the perfect fit, and with our hassle-free returns policy, you can shop with complete peace of mind. Join thousands of satisfied customers who have already made Urban Thread their trusted style destination.",
    "cta": "Shop the full collection at Urban Thread today and elevate your wardrobe — visit our store now!"
  },
  "tiktok": {
    "hook": "You're still wearing THAT when this exists?!"
  }
}
```

---

## API Reference

### `POST /generate`

Generates advertising content for all three platforms.

**Request body**

| Field      | Type   | Description                          |
|------------|--------|--------------------------------------|
| `business` | string | Business or brand name (required)    |
| `product`  | string | Product or service description (required) |

**Responses**

| Code  | Meaning                                                        |
|-------|---------------------------------------------------------------|
| `200` | Success — returns content for all three platforms             |
| `422` | Invalid input (e.g. empty business or product)               |
| `502` | The model could not produce valid content after retry        |
