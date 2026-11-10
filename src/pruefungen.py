"""Prüft und vereinheitlicht die vom Sprachmodell ausgelesenen Rechnungsdaten."""

TOLERANZ = 0.01  # maximal erlaubte Rundungsdifferenz in Euro

import re


def iban_normalisieren(iban: str | None) -> str | None:
    """Entfernt Leerzeichen aus der IBAN und schreibt sie in Großbuchstaben."""
    if iban is None:
        return None
    return iban.replace(" ", "").upper()


def datum_normalisieren(datum: str | None) -> str | None:
    """Sucht ein Datum im Text und gibt es im Format TT.MM.JJJJ zurück."""
    if datum is None:
        return None
    treffer = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", datum)
    if treffer:
        return treffer.group(0)
    treffer = re.search(r"(\d{4})-(\d{2})-(\d{2})", datum)
    if treffer:
        jahr, monat, tag = treffer.groups()
        return f"{tag}.{monat}.{jahr}"
    return None


def betrag_als_text(betrag: float) -> str:
    """Wandelt einen Betrag in das deutsche Format um, z. B. 1150.5 → '1.150,50'."""
    return f"{betrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def im_text_gefunden(feld: str, wert, text: str) -> bool:
    """Prüft, ob ein ausgelesener Wert tatsächlich im Text der Rechnung vorkommt."""
    if wert is None:
        return True
    if feld == "iban":
        return wert in text.replace(" ", "")
    if feld == "ust_satz":
        return f"{wert:g} %" in text
    if isinstance(wert, (int, float)):
        return betrag_als_text(wert) in text
    return wert in text


def werte_abgleichen(daten: dict, text: str) -> list[str]:
    """Gibt die Namen aller Felder zurück, deren Wert nicht im Text der Rechnung steht."""
    return [feld for feld, wert in daten.items() if not im_text_gefunden(feld, wert, text)]


def rechenlogik_pruefen(daten: dict) -> list[str]:
    """Prüft, ob Netto, USt-Satz, USt-Betrag und Brutto rechnerisch zusammenpassen."""
    fehler = []
    netto, ust_satz = daten["netto"], daten["ust_satz"]
    ust_betrag, brutto = daten["ust_betrag"], daten["brutto"]

    if None in (netto, ust_betrag, brutto):
        return fehler  # fehlende Werte meldet die Pflichtangaben-Prüfung

    if abs(netto + ust_betrag - brutto) > TOLERANZ:
        fehler.append("Netto + USt ergibt nicht den Bruttobetrag")

    if ust_satz is not None and abs(netto * ust_satz / 100 - ust_betrag) > TOLERANZ:
        fehler.append("USt-Betrag passt nicht zum USt-Satz")

    return fehler