"""Kommunikation mit dem lokal ausgeführten Sprachmodell (Ollama)."""

import ollama

MODELL = "qwen2.5:3b"


def frage_stellen(frage: str) -> str:
    """Schickt eine Frage an das Sprachmodell und gibt die Antwort als Text zurück."""
    antwort = ollama.chat(
        model=MODELL,
        messages=[{"role": "user", "content": frage}],
    )
    return antwort["message"]["content"]