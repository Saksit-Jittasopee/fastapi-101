from fastapi import FastAPI, HTTPException, Request, Depends
from typing import Union, List

from sqlalchemy.orm import Session

from database import engine, get_db, Base
from schema import WordCreated, WordResponse
from models import Word

app = FastAPI()

# Create Database
Base.metadata.create_all(bind=engine)

@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

# @app.get("/hello/{hello_id}")
# def hello_id(hello_id : int):
#     return {"message": hello_id}

@app.get("/word/{word_id}", response_model=WordResponse)
def word_id(word_id : int, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first() # ดึงข้อมูลจากฐานข้อมูลมาแสดง
    return db_word

@app.get("/word", response_model=List[WordResponse])
def word_readall(db: Session = Depends(get_db)):
    db_word = db.query(Word).all()
    return db_word

@app.post("/word", response_model=WordResponse) # JSON Input
def create_word(word: WordCreated, db: Session = Depends(get_db)):
    # db_word = Word(title=word.title, description=word.description, price=word.price)
    db_word = Word(**word.model_dump())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    # body = await request.json()
    # print(body["name"]) # Request
    # print(word.name) # Pydantic
    return db_word

@app.put("/word/{word_id}", response_model=WordResponse) # JSON Input
async def update_word(word_id : int, word: WordCreated, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    for key, value in word.model_dump().items():
        setattr(db_word, key, value)
    db.commit()
    db.refresh(db_word)
    # body = await request.json()
    # print(body["name"]) # Request
    # print(word.name) # Pydantic
    return db_word

@app.delete("/word/{word_id}") # JSON Input
async def delete_word(word_id : int, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(db_word)
    db.commit()
    # body = await request.json()
    # print(body["name"]) # Request
    # print(word.name) # Pydantic
    return db_word

# Running
# python -m fastapi dev main.py

# Run Production
# fastapi run main.py