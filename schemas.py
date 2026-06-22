from pydantic import BaseModel, Field


class AdRequest(BaseModel):
    business: str = Field(min_length=1, description="Business or brand name")
    product: str = Field(min_length=1, description="Product or service description")
