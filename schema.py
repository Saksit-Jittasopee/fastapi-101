from pydantic import BaseModel

# 1 - Base (Pydantic Model) ทำให้เวลา POST จะต้องใช้โครง Model นี้ แทนการใช้ Request
class WordBase(BaseModel):
    title: str
    description: str
    price: float

# 2 - Request
class WordCreated(WordBase):
    pass

# 3 - Response
class WordResponse(WordBase):
    id: int
    class Config:
        from_attributes = True