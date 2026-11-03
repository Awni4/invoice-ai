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

## Tag 2 – 02.11.2026
**Erledigt:**
Ollama installiert und das Sprachmodell qwen2.5:3b eingerichtet; Handtest im Terminal mit zwei Rechnungen -> Modell liest Rechnungsnummer, Datum und Betrag korrekt aus

Neue Datei `ki.py` mit der Funktion `frage_stellen`: Python sendet eine Frage an das lokale Sprachmodell und erhält die Antwort zurück -> Testfrage nach der Rechnungsnummer der ersten Rechnung wird korrekt beantwortet (PN-2026-0417)

**Gelernt:**
Lokale Sprachmodelle mit Ollama verwalten (`pull`, `run`, `list`, `rm`); Zusammenhang zwischen Modellgröße, Speicherbedarf und Antwortzeit; Anbindung an Python über die Bibliothek `ollama` mit Nachrichten im Format Rolle/Inhalt.

Gültigkeitsbereich von Variablen: Eine innerhalb einer Funktion erstellte Variable existiert nur dort und ist außerhalb nicht verfügbar.

**Problem & Lösung:**
- Problem: Das zunächst gewählte Modell mit 7 Milliarden Parametern (ca. 4–5 GB) ist für einen Laptop ohne eigene Grafikkarte zu groß und zu langsam
- Lösung: Wechsel auf die kleinere Variante qwen2.5:3b (ca. 2 GB) mit einer Antwortzeit von rund 5 Sekunden.


-> Handtest mit einer Rechnung ohne Rechnungsnummer: Das Modell erkennt, dass die Nummer fehlt, statt eine zu erfinden – wichtig, da erfundene Werte bei Rechnungsdaten zu Fehlbuchungen führen würden.

-> Die Antworten kommen als Fließtext („Die Rechnungsnummer dieser Rechnung lautet …“). Für eine automatische Prüfung ist das ungeeignet, da ein Programm die Werte nicht zuverlässig daraus entnehmen kann.


**Nächster Schritt:**
Die Rechnungsdaten in einem festen, strukturierten Format (JSON) von der KI zurückgeben lassen, damit sie automatisch weiterverarbeitet und geprüft werden können.

## Tag 3 – 03.11.2026
**Erledigt:**
Neue Funktion `rechnungsdaten_auslesen`: Das Sprachmodell gibt die Rechnungsdaten (Lieferant, Rechnungsnummer, Datum, IBAN, Netto, USt-Satz, USt-Betrag, Brutto) in einem festen JSON-Format zurück -> Daten liegen als Python-Dictionary vor und können automatisch weiterverarbeitet werden

Anweisung an das Modell um feste Regeln ergänzt (Beträge exakt übernehmen, nichts erfinden, fehlende Angaben als null).

**Gelernt:**
JSON-Schema als Vorgabe für die Ausgabe des Sprachmodells (`format`); Datentypen im Schema (`string`, `number`) und `null` für fehlende Angaben; `temperature: 0` für möglichst gleichbleibende Antworten; JSON mit `json.loads` in ein Dictionary umwandeln.

Prompt Engineering: Die Formulierung der Anweisung beeinflusst das Ergebnis stark – eine Änderung kann ein Problem beheben und gleichzeitig ein neues erzeugen.

**Problem & Lösung:**
- Problem: Bei Rechnung 03 gibt das Modell als Bruttobetrag 892,50 € zurück, obwohl auf der Rechnung 942,50 € steht – es rechnet Netto + USt selbst aus, statt den gedruckten Wert zu übernehmen, auch mit ausdrücklicher Anweisung
- Lösung: Noch offen. Statt weiterer Anweisungen werden die Ergebnisse im nächsten Schritt im Code gegen den Originaltext der Rechnung geprüft.

- Problem: Fehlende Angaben wurden zunächst als leerer Text statt als null zurückgegeben; Lieferant und Datum wurden bei einem Layout nicht erkannt
- Lösung: Anweisung um Regeln zu Lieferant, Datumsformat und fehlenden Angaben ergänzt.


-> Die KI hat einen Rechnungsfehler stillschweigend „korrigiert“. Eine Prüfung von Netto + USt = Brutto auf Basis dieser Werte würde den Fehler nie finden – die falsche Rechnung würde unbemerkt bezahlt.

-> Die verbesserte Anweisung hat die Probleme bei Rechnung 04 behoben, dafür bei Rechnung 05 einen neuen Fehler erzeugt (erfundener Lieferantenname „Dr. Printhaus Rheinblick“ statt „Druckhaus Rheinblick“). Datum und IBAN kommen in wechselnden Formaten zurück.

-> Schlussfolgerung: KI-Ergebnisse dürfen bei Finanzdaten nicht ungeprüft übernommen werden – das kleine Modell ist hilfreich, aber nicht zuverlässig.


**Nächster Schritt:**
Ergebnisse im Code absichern: Datums- und IBAN-Format vereinheitlichen und jeden ausgelesenen Wert mit dem Originaltext der Rechnung abgleichen, damit erfundene oder veränderte Werte automatisch erkannt werden.