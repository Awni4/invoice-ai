"""Kommunikation mit dem lokal ausgeführten Sprachmodell (Ollama)."""

import json

import ollama

MODELL = "qwen2.5:3b"

SCHEMA = {
    "type": "object",
    "properties": {
        "lieferant": {"type": "string"},
        "rechnungsnummer": {"type": ["string", "null"]},
        "rechnungsdatum": {"type": ["string", "null"]},
        "iban": {"type": ["string", "null"]},
        "netto": {"type": ["number", "null"]},
        "ust_satz": {"type": ["number", "null"]},
        "ust_betrag": {"type": ["number", "null"]},
        "brutto": {"type": ["number", "null"]},
    },
    "required": ["lieferant", "rechnungsnummer", "rechnungsdatum",
                 "iban", "netto", "ust_satz", "ust_betrag", "brutto"],
}

def frage_stellen(frage: str) -> str:
    """Schickt eine Frage an das Sprachmodell und gibt die Antwort als Text zurück."""
    antwort = ollama.chat(
        model=MODELL,
        messages=[{"role": "user", "content": frage}],
    )
    return antwort["message"]["content"]

def rechnungsdaten_auslesen(text: str) -> dict:
    """Lässt das Sprachmodell die Rechnungsdaten auslesen und gibt sie als Dictionary zurück."""
    anweisung = (
        "Lies aus der folgenden Rechnung die Rechnungsdaten aus.\n"
        "Regeln:\n"
        "- Übernimm alle Beträge exakt so, wie sie auf der Rechnung stehen. "
        "Rechne nichts nach und korrigiere keine Beträge, auch wenn sie nicht zusammenpassen.\n"
        "- Beträge als Zahl mit Punkt als Dezimaltrennzeichen, ohne Eurozeichen.\n"
        "- Der Lieferant ist das Unternehmen, das die Rechnung ausstellt, nicht der Empfänger.\n"
        "- Das Rechnungsdatum kann auch in der Form 'Ort, den TT.MM.JJJJ' angegeben sein.\n"
        "- Wenn eine Angabe nicht vorhanden ist, gib null zurück, keinen leeren Text, und erfinde nichts.\n\n"
    )
    antwort = ollama.chat(
        model=MODELL,
        messages=[{"role": "user", "content": anweisung + text}],
        format=SCHEMA,
        options={"temperature": 0},
    )
    return json.loads(antwort["message"]["content"])
