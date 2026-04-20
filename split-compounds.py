import sys
import re
from collections import Counter


def get_geometric_mean(frequencies):
    if not frequencies:
        return 0
    # Produkt der Häufigkeiten berechnen
    product = 1
    for f in frequencies:
        product *= f
    # n-te Wurzel ziehen
    return pow(product, 1 / len(frequencies))


def split_compound(word, word_list):
    """
    Rekursive Funktion zur Zerlegung nach Koehn.
    """
    word_lower = word.lower()

    # Basisfall: Das Wort selbst ist in der Liste (als Ganzes)
    if word_lower in word_list and len(word) >= 3:
        yield [word]

    # Suche nach möglichen Split-Punkten (min. 3 Zeichen für das erste Element)
    for i in range(3, len(word) + 1):
        prefix = word[:i]
        suffix = word[i:]

        prefix_lower = prefix.lower()

        if prefix_lower not in word_list:
            continue

        if suffix:
            # 1. Fall: Direkter Split (z.B. Arbeit | amt)
            for rest in split_compound(suffix, word_list):
                yield [prefix] + rest

            # 2. Fall: Fugenelement 's' (z.B. Arbeit | s | amt)
            if suffix.startswith('s') and len(suffix) > 2:
                real_suffix = suffix[1:]
                for rest in split_compound(real_suffix, word_list):
                    yield [prefix] + rest


def main():
    if len(sys.argv) < 2:
        print("Benutzung: python split-compounds.py <korpus_datei>")
        return

    dateipfad = sys.argv[1]
    nomen_counts = Counter()

    # 1. Korpus einlesen und Wortliste (Nomen) erstellen
    # Muster: Großbuchstabe + mindestens 2 Kleinbuchstaben
    pattern = re.compile(r"^[A-Z][a-z]{2,}$")

    try:
        with open(dateipfad, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                word, tag = parts[0], parts[1]
                if tag == "NN" and pattern.match(word):
                    nomen_counts[word] += 1

    except FileNotFoundError:
        print(f"Fehler: Datei {dateipfad} nicht gefunden.")
        return

    # Dictionary für Case-Insensitive Lookup (Kleingeschrieben -> Originalhäufigkeit)
    # Da Koehn vorschlägt, Groß/Kleinschreibung zu ignorieren:
    word_lookup = {w.lower(): count for w, count in nomen_counts.items()}

    # 2. Jedes gefundene Nomen zerlegen
    for original_word in nomen_counts:
        all_splits = []

        for parts in split_compound(original_word, word_lookup):
            # Validierung
            valid = True
            freqs = []

            for p in parts:
                p_lower = p.lower()
                if p_lower not in word_lookup:
                    valid = False
                    break
                freqs.append(word_lookup[p_lower])

            if not valid:
                continue

            score = get_geometric_mean(freqs)
            all_splits.append((score, parts))

        # 3. Sortieren (nach Score absteigend) und Ausgabe
        all_splits.sort(key=lambda x: x[0], reverse=True)

        for score, parts in all_splits:
            print(f"{original_word} {score:.1f} {' '.join(parts)}")


if __name__ == "__main__":
    main()