from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
   name: str = Field(..., min_length=1)
   description: str = Field(..., min_length=1)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    description: str | None = Field(None, min_length=1)
    
class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
