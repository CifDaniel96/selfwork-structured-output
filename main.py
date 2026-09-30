import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY mancante. Controlla il file .env"
    )

client = OpenAI(api_key=api_key)


# =========================================================
# ESEMPIO 1 - MATH TUTOR
# =========================================================

class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str


def get_math_solution(question: str) -> MathReasoning:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Sei un tutor di matematica. "
                    "Guida lo studente passo dopo passo "
                    "nella risoluzione del problema."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        response_format=MathReasoning,
    )

    return completion.choices[0].message.parsed


math_solution = get_math_solution(
    "Risolvi l'equazione 8x + 7 = -23"
)

print("\n=== ESEMPIO 1: MATH TUTOR ===\n")

for index, step in enumerate(
    math_solution.steps,
    start=1,
):
    print(f"Passaggio {index}")
    print(f"Spiegazione: {step.explanation}")
    print(f"Risultato: {step.output}")
    print()

print(
    f"Risposta finale: "
    f"{math_solution.final_answer}"
)


# =========================================================
# ESEMPIO 2 - TEXT SUMMARIZATION
# =========================================================

class Concept(BaseModel):
    title: str
    description: str


class ArticleSummary(BaseModel):
    invented_year: int
    summary: str
    inventors: list[str]
    concepts: list[Concept]
    description: str


def get_article_summary(article: str) -> ArticleSummary:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ti verrà fornito il contenuto di un articolo "
                    "su un'invenzione. Riassumi l'articolo seguendo "
                    "lo schema fornito."
                ),
            },
            {
                "role": "user",
                "content": article,
            },
        ],
        response_format=ArticleSummary,
    )

    return completion.choices[0].message.parsed


article = """
Il Transformer è un'architettura di rete neurale introdotta nel 2017
nel paper 'Attention Is All You Need'.

Il lavoro è stato sviluppato da un gruppo di ricercatori tra cui
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit,
Llion Jones, Aidan Gomez, Lukasz Kaiser e Illia Polosukhin.

L'architettura Transformer utilizza il meccanismo di attention per
elaborare le relazioni tra le parole di una sequenza senza dipendere
necessariamente da reti ricorrenti.

Uno dei concetti fondamentali è la self-attention, che permette al
modello di assegnare pesi differenti alle varie parti dell'input.
Un altro elemento importante è la multi-head attention, che consente
di analizzare contemporaneamente differenti rappresentazioni delle
informazioni.

I Transformer hanno avuto un forte impatto nel Natural Language
Processing e costituiscono la base di molti moderni Large Language
Models.
"""

article_summary = get_article_summary(article)

print("\n=== ESEMPIO 2: TEXT SUMMARIZATION ===\n")

print(
    f"Anno di introduzione: "
    f"{article_summary.invented_year}"
)

print(
    f"Riassunto: "
    f"{article_summary.summary}"
)

print("\nInventori:")

for inventor in article_summary.inventors:
    print(f"- {inventor}")

print("\nConcetti:")

for concept in article_summary.concepts:
    print(
        f"- {concept.title}: "
        f"{concept.description}"
    )

print(
    f"\nDescrizione: "
    f"{article_summary.description}"
)