def build_instagram_prompt(business: str, product: str) -> str:
    return f"""You are an expert social media copywriter specializing in Instagram marketing.

Create an Instagram post for the following business:
Business: {business}
Product/Service: {product}

Requirements:
- Write an engaging, warm, lifestyle-oriented caption (2-3 sentences)
- The tone should be inspiring and visually evocative
- Include at least 5 relevant hashtags
- You may use emojis naturally

Return ONLY a valid JSON object in exactly this format, with no extra text:
{{
  "caption": "your caption here",
  "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"]
}}"""
