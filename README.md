# Invoice AI

KI-gestützte Verarbeitung von PDF-Rechnungen mit Python: Rechnungsdaten automatisch auslesen, auf Vollständigkeit und Richtigkeit prüfen und als Excel-Liste exportieren.

> **Status:** in Entwicklung – Fortschritt wird regelmäßig im [Entwicklungstagebuch](DEVLOG.md) dokumentiert.

## Problem

Im Rechnungseingang werden Daten wie Rechnungsnummer, Datum, Beträge und Bankverbindung häufig noch manuell aus PDF-Rechnungen abgetippt. Jeder Lieferant verwendet ein anderes Layout, Fehler wie falsche Summen oder fehlende Pflichtangaben fallen oft erst spät auf. Das kostet Zeit und ist fehleranfällig.

## Lösung

Dieses Projekt automatisiert den Ablauf von der PDF-Rechnung bis zur geprüften Excel-Liste:

1. **Einlesen** – Text aus PDF-Rechnungen extrahieren
2. **Auslesen** – ein lokal ausgeführtes KI-Sprachmodell erkennt die Rechnungsdaten unabhängig vom Layout
3. **Prüfen** – Rechenlogik (Netto + USt = Brutto), Pflichtangaben und IBAN automatisch kontrollieren
4. **Exportieren** – Excel-Liste mit Prüfstatus für jede Rechnung

Die KI läuft lokal auf dem eigenen Rechner: Die Rechnungsdaten verlassen das Gerät nicht.

## Funktionen

- [x] PDF-Rechnungen einlesen und Text extrahieren
- [ ] Rechnungsdaten mit KI auslesen
- [ ] Prüfung der Rechenlogik
- [ ] Prüfung der Pflichtangaben
- [ ] Prüfung der IBAN
- [ ] Export als Excel-Liste mit Prüfstatus
- [ ] Prozessmodell (BPMN) Vorher/Nachher

## Technologien

Python · pypdf · Ollama (qwen2.5:3b) · (geplant: pandas, openpyxl, BPMN)

## Installation & Nutzung

**Voraussetzungen:** Python 3 und [Ollama](https://ollama.com) mit dem Modell `qwen2.5:3b`:

```bash
ollama pull qwen2.5:3b
```

**Projekt starten:**

```bash
git clone https://github.com/Awni4/invoice-ai.git
cd invoice-ai
pip install -r requirements.txt
python src/main.py
```

Ollama muss beim Ausführen im Hintergrund laufen.

## Daten

Alle Rechnungen im Ordner `data/rechnungen/` sind **frei erfunden**. Firmen, Adressen, Steuer- und Kontonummern sind fiktiv. Einzelne Rechnungen enthalten bewusst Fehler, um die Prüfungen zu testen.

## Autor

Awni Badlah – Student der Wirtschaftsinformatik, Schwerpunkt KI, Finanzen und Prozessautomatisierung

Entwickelt mit KI-Unterstützung (Claude) als Lern- und Portfolioprojekt.
