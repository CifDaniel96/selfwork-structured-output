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
# ESEMPIO 1 - BUG REPORT TRIAGE
# =========================================================

class BugReport(BaseModel):
    category: str
    priority: str
    summary: str
    possible_cause: str
    suggested_actions: list[str]


def analyze_bug_report(report: str) -> BugReport:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Sei un assistente tecnico specializzato nel triage "
                    "dei bug software. Analizza la segnalazione ricevuta "
                    "e restituisci le informazioni secondo lo schema fornito. "
                    "La possibile causa deve essere indicata come ipotesi "
                    "e non come certezza. Non inventare dettagli non presenti "
                    "o non deducibili dalla segnalazione."
                ),
            },
            {
                "role": "user",
                "content": report,
            },
        ],
        response_format=BugReport,
    )

    return completion.choices[0].message.parsed


bug_report = analyze_bug_report(
    """
    Dopo l'ultimo aggiornamento dell'applicazione,
    quando provo a caricare un'immagine profilo in formato PNG
    ricevo sempre un errore 500.

    Il problema impedisce di completare il profilo utente.
    """
)

print("\n=== ESEMPIO 1: BUG REPORT TRIAGE ===\n")

print(f"Categoria: {bug_report.category}")
print(f"Priorità: {bug_report.priority}")
print(f"Riassunto: {bug_report.summary}")
print(f"Possibile causa: {bug_report.possible_cause}")

print("\nAzioni suggerite:")

for action in bug_report.suggested_actions:
    print(f"- {action}")


# =========================================================
# ESEMPIO 2 - SECURITY CODE REVIEW
# =========================================================

class Vulnerability(BaseModel):
    name: str
    description: str
    mitigation: str


class SecurityReview(BaseModel):
    risk_level: str
    vulnerabilities: list[Vulnerability]
    overall_recommendation: str


def analyze_code_security(code: str) -> SecurityReview:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Sei un assistente specializzato in secure coding. "
                    "Analizza il codice fornito, individua eventuali "
                    "vulnerabilità e restituisci il risultato secondo "
                    "lo schema fornito. Concentrati su problemi realmente "
                    "deducibili dal codice e proponi mitigazioni difensive."
                ),
            },
            {
                "role": "user",
                "content": code,
            },
        ],
        response_format=SecurityReview,
    )

    return completion.choices[0].message.parsed


code_to_review = """
def find_user(email, cursor):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    return cursor.fetchone()
"""

security_review = analyze_code_security(code_to_review)

print("\n=== ESEMPIO 2: SECURITY CODE REVIEW ===\n")

print(f"Livello di rischio: {security_review.risk_level}")

print("\nVulnerabilità individuate:")

for vulnerability in security_review.vulnerabilities:
    print(f"\nNome: {vulnerability.name}")
    print(f"Descrizione: {vulnerability.description}")
    print(f"Mitigazione: {vulnerability.mitigation}")

print(
    f"\nRaccomandazione generale: "
    f"{security_review.overall_recommendation}"
)