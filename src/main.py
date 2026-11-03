"""
Invoice AI – Rechnungen einlesen und auswerten

Funktionsumfang:
1. Liest alle PDF-Rechnungen aus dem Ordner data/rechnungen ein
2. Extrahiert den Text jeder Rechnung
3. Lässt das lokale Sprachmodell die Rechnungsdaten strukturiert auslesen und gibt sie aus


Ausführen (im Projektordner):
    python src/main.py
"""

from pathlib import Path

from pypdf import PdfReader

from ki import rechnungsdaten_auslesen

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
        daten = rechnungsdaten_auslesen(text_aus_pdf(pfad))
        for feld, wert in daten.items():
            print(f"{feld}: {wert}")
        print()


if __name__ == "__main__":
    main()

