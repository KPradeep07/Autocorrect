import os

import ujson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from autocorrect import Autocorrect

data_path = os.path.join(os.getcwd(), "correct_words.json")
config_path = os.path.join(os.getcwd(), "config.json")
data = ujson.load(open(data_path))
CONFIG = ujson.load(open(config_path))
correcter = Autocorrect(data)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Word(BaseModel):
    word: str


class Sentence(BaseModel):
    sentence: str


@app.get("/")
def root():
    return {"message": "Autocorrect API"}


@app.get("/ping")
def ping():
    return "Pong"


@app.post("/suggest")
async def correct_word(params: Word):
    correct_word = correcter.correct_word(
        params.word, 
        CONFIG["match_score"]
        )

    return correct_word


@app.post("/suggest_with_key")
async def suggest_with_key(params: Sentence):
    correct_sentence = correcter.correct_sentence(
        params.sentence,
        CONFIG["match_score"],
    )

    return correct_sentence
