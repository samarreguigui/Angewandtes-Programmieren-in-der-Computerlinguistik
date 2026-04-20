import sys
from collections import defaultdict


def read_frequencies(filename: str) -> dict[str, int]:
    """
    Liest die erste Spalte der Datei ein und zählt Häufigkeiten.
    Nur rein alphabetische Wörter werden berücksichtigt.
    """
    freq: dict[str, int] = defaultdict(int)
    with open(filename, encoding="utf-8") as fh:
        for line in fh:
            parts = line.strip().split()
            if not parts:
                continue
            word = parts[0]
            if word.isalpha():
                freq[word] += 1
    return freq


def best_casing(freq: dict[str, int]) -> dict[str, int]:
    """
    Falls ein Wort in zwei Schreibungen vorkommt,
    behalten wir nur die häufigere Variante.
    Rückgabe:  Häufigkeits-Dictionary.
    """
    grouped = defaultdict(lambda: defaultdict(int))

    for word, count in freq.items():
        grouped[word.lower()][word] += count

    result = {}
    for low, forms in grouped.items():
        best = max(forms.items(), key=lambda x: x[1])[0]
        total = sum(forms.values())
        result[best] = total

    return result


def build_anagram_dict(freq: dict[str, int]) -> defaultdict:
    """
    Baut das Anagramm-Dictionary auf.
    Key   : alphabetisch sortierte Kleinbuchstaben des Wortes
    Value : Liste der Wörter mit dieser Buchstabenmenge
    """
    anagramme: defaultdict[str, list[str]] = defaultdict(list)
    for word in freq:
        key = "".join(sorted(word.lower()))
        anagramme[key].append(word)
    return anagramme


def main() -> None:
    if len(sys.argv) < 2:
        print("Aufruf: python anagramme.py <korpus>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    # 1. Häufigkeiten einlesen
    freq = read_frequencies(filename)

    # 2. Doppelschreibungen bereinigen
    freq = best_casing(freq)

    # 3. Wörter mit Häufigkeit < 10 entfernen
    freq = {w: c for w, c in freq.items() if c >= 10}

    # 4. Anagramm-Gruppen aufbauen
    anagramme = build_anagram_dict(freq)

    # 5. Gruppen mit mehr als einem Element sammeln und sortieren
    results: list[list[str]] = []
    for words in anagramme.values():
        if len(words) > 1:
            # Innerhalb der Gruppe: absteigend nach Korpushäufigkeit
            words_sorted = sorted(words, key=lambda w: freq[w], reverse=True)
            results.append(words_sorted)

    # 6. Ausgabe
    for words in results:
        print(" ".join(words))


if __name__ == "__main__":
    main()