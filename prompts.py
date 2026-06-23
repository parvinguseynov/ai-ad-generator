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


def build_facebook_prompt(business: str, product: str) -> str:
    return f"""You are an expert social media copywriter specializing in Facebook marketing.

Create a Facebook ad for the following business:
Business: {business}
Product/Service: {product}

Requirements:
- Write detailed, informative ad copy (5-6 sentences) that explains the product's benefits
- The tone should be friendly, mature and trustworthy, building confidence in the product
- End with a strong, explicit call to action (e.g. "Order today", "Learn more")

Return ONLY a valid JSON object in exactly this format, with no extra text:
{{
"text": "your ad text here",
"cta": "your call to action here"
}}"""
