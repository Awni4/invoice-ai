# Entwicklungstagebuch

## Tag 1 – 30.10.2026
**Erledigt:**
Projekt aufgesetzt (Repository, Ordnerstruktur, README, `.gitignore`) und fünf fiktive PDF-Rechnungen mit unterschiedlichen Layouts als Testdaten angelegt -> Grundlage für die Verarbeitung steht

Erste Funktion `text_aus_pdf`: Der Text aller Rechnungen wird mit pypdf ausgelesen und im Terminal ausgegeben.

**Gelernt:**
Text aus PDF-Dateien mit pypdf extrahieren; alle Dateien eines Ordners mit `glob("*.pdf")` finden und verarbeiten.

**Problem & Lösung:**
- Problem: Jede Rechnung ist anders aufgebaut – Rechnungsnummer, Datum und Beträge stehen je nach Lieferant an unterschiedlichen Stellen und sind unterschiedlich beschriftet
- Lösung: Feste Regeln wie bei der Kategorisierung im ersten Projekt reichen hier nicht aus. Für das Auslesen wird deshalb ein KI-Sprachmodell eingesetzt, das die Daten unabhängig vom Layout erkennt.


-> Entscheidung für ein lokal ausgeführtes Sprachmodell (Ollama) statt eines Cloud-Dienstes: keine laufenden Kosten, und die Rechnungsdaten verlassen den eigenen Rechner nicht – ein wichtiger Punkt beim Umgang mit Finanz- und Geschäftsdaten.

-> Beispiel aus den Testdaten: Die Rechnungsnummer steht bei einer Rechnung als „Rechnungsnummer: PN-2026-0417“ in zwei Zeilen, bei einer anderen als „Rechnung Nr. 2026/1183“ in einer Zeile; das Rechnungsdatum einmal als „Rechnungsdatum: 02.09.2026“, einmal als „Landau, den 09.09.2026“.


**Nächster Schritt:**
Ollama installieren und ein passendes Sprachmodell einrichten, damit die Rechnungsdaten im nächsten Schritt automatisch ausgelesen werden können.
