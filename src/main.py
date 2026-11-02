"""
Invoice AI – Rechnungen einlesen und auswerten

Funktionsumfang:
1. Liest alle PDF-Rechnungen aus dem Ordner data/rechnungen ein
2. Extrahiert den Rohtext jeder Rechnung und gibt ihn aus
3. Stellt testweise eine Frage zum Inhalt der ersten Rechnung an das lokale Sprachmodell

Ausführen (im Projektordner):
    python src/main.py
"""

from pathlib import Path

from pypdf import PdfReader

from ki import frage_stellen

# Ordner mit den Rechnungen – relativ zum Projektordner, damit es auf jedem Rechner funktioniert
RECHNUNGS_ORDNER = Path(__file__).parent.parent / "data" / "rechnungen"


def text_aus_pdf(pfad: Path) -> str:
    """Liest den Text aller Seiten einer PDF-Datei aus und gibt ihn zurück."""
    reader = PdfReader(pfad)
    return "\n".join(seite.extract_text() for seite in reader.pages)


def main() -> None:
    rechnungen = sorted(RECHNUNGS_ORDNER.glob("*.pdf"))
    print(f"{len(rechnungen)} Rechnungen gefunden\n")

    for pfad in rechnungen:
        print(f"=== {pfad.name} ===")
        print(text_aus_pdf(pfad))
        print()


    print("=== Test: Frage an die KI ===")
    text = text_aus_pdf(rechnungen[0])
    print(frage_stellen("Wie lautet die Rechnungsnummer dieser Rechnung?\n\n" + text))


if __name__ == "__main__":
    main()

