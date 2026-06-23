from pydantic import BaseModel, Field


class AdRequest(BaseModel):
    business: str = Field(min_length=1, description="Business or brand name")
    product: str = Field(
        min_length=1, description="Product or service description")


class InstagramContent(BaseModel):
    caption: str = Field(min_length=1, description="Instagram post caption")
    hashtags: list[str] = Field(
        min_length=5, description="At least 5 hashtags")


class FacebookContent(BaseModel):
    text: str = Field(min_length=1, description="Detailed Facebook ad copy")
    cta: str = Field(min_length=1, description="Strong call to action")


class TikTokContent(BaseModel):
    hook: str = Field(
        min_length=1, description="Short attention-grabbing hook")


class AdResponse(BaseModel):
    instagram: InstagramContent
    facebook: FacebookContent
    tiktok: TikTokContent
