"""
Invoice AI – Rechnungen einlesen und auswerten

Funktionsumfang:
1. Liest alle PDF-Rechnungen aus dem Ordner data/rechnungen ein
2. Extrahiert den Text jeder Rechnung
3. Lässt das lokale Sprachmodell die Rechnungsdaten strukturiert auslesen
4. Vereinheitlicht Datum (TT.MM.JJJJ) und IBAN (ohne Leerzeichen)
5. Gleicht jeden ausgelesenen Wert mit dem Originaltext ab und markiert Werte, die nicht im Dokument stehen

Ausführen (im Projektordner):
    python src/main.py
"""

from pathlib import Path

from pypdf import PdfReader

from ki import rechnungsdaten_auslesen
from pruefungen import iban_normalisieren, datum_normalisieren, werte_abgleichen

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
        text = text_aus_pdf(pfad)
        daten = rechnungsdaten_auslesen(text)
        daten["iban"] = iban_normalisieren(daten["iban"])
        daten["rechnungsdatum"] = datum_normalisieren(daten["rechnungsdatum"])
        for feld, wert in daten.items():
            print(f"{feld}: {wert}")
        nicht_gefunden = werte_abgleichen(daten, text)
        if nicht_gefunden:
            print(f"⚠ Nicht im Dokument gefunden: {', '.join(nicht_gefunden)}")
        print()


if __name__ == "__main__":
    main()

