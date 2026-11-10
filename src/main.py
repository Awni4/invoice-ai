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

import json
from pathlib import Path

from pypdf import PdfReader

from ki import rechnungsdaten_auslesen
from pruefungen import iban_normalisieren, datum_normalisieren, werte_abgleichen, rechenlogik_pruefen


# Ordner mit den Rechnungen – relativ zum Projektordner, damit es auf jedem Rechner funktioniert
RECHNUNGS_ORDNER = Path(__file__).parent.parent / "data" / "rechnungen"

CACHE_ORDNER = Path(__file__).parent.parent / "output" / "cache"


def text_aus_pdf(pfad: Path) -> str:
    """Liest den Text aller Seiten einer PDF-Datei aus und gibt ihn zurück."""
    reader = PdfReader(pfad)
    return "\n".join(seite.extract_text() for seite in reader.pages)


def daten_auslesen_mit_cache(pfad: Path, text: str) -> dict:
    """Gibt das KI-Ergebnis aus dem Cache zurück oder fragt die KI und speichert das Ergebnis."""
    cache_datei = CACHE_ORDNER / f"{pfad.stem}.json"      # Dateiname ohne Endung .pdf

    if cache_datei.exists():
        return json.loads(cache_datei.read_text(encoding="utf-8"))

    daten = rechnungsdaten_auslesen(text)
    CACHE_ORDNER.mkdir(parents=True, exist_ok=True)
    cache_datei.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    return daten


def main() -> None:
    rechnungen = sorted(RECHNUNGS_ORDNER.glob("*.pdf"))
    print(f"{len(rechnungen)} Rechnungen gefunden\n")
    
    print(rechenlogik_pruefen({"netto": 750, "ust_satz": 19, "ust_betrag": 142.5, "brutto": 942.5}))


    for pfad in rechnungen:
        print(f"=== {pfad.name} ===")
        text = text_aus_pdf(pfad)
        daten = daten_auslesen_mit_cache(pfad, text)
        daten["iban"] = iban_normalisieren(daten["iban"])
        daten["rechnungsdatum"] = datum_normalisieren(daten["rechnungsdatum"])
        for feld, wert in daten.items():
            print(f"{feld}: {wert}")
        nicht_gefunden = werte_abgleichen(daten, text)
        if nicht_gefunden:
            print(f"⚠ Nicht im Dokument gefunden: {', '.join(nicht_gefunden)}")
        print(rechenlogik_pruefen(daten))
        print()


if __name__ == "__main__":
    main()

