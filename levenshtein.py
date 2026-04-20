import sys


# levenshtein matrix
def levenshtein_matrix(a, b):
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialisierung
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j

    # Berechnung mit angegebener Formel
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + cost
            )

    return d


# Backtracking (alle optimalen Alignments)
def backtrack_alignments(d, a, b):

    def bt(i, j):
        if i == 0 and j == 0:
            return [("", "")]

        res = []

        # deletion
        if i > 0 and d[i][j] == d[i - 1][j] + 1:
            for x, y in bt(i - 1, j):
                res.append((x + a[i - 1], y + "-"))

        # insertion
        if j > 0 and d[i][j] == d[i][j - 1] + 1:
            for x, y in bt(i, j - 1):
                res.append((x + "-", y + b[j - 1]))

        # match / substitution
        if i > 0 and j > 0:
            cost = 0 if a[i - 1] == b[j - 1] else 1
            if d[i][j] == d[i - 1][j - 1] + cost:
                for x, y in bt(i - 1, j - 1):
                    res.append((x + a[i - 1], y + b[j - 1]))

        return res

    return bt(len(a), len(b))


def main():
    if len(sys.argv) < 2:
        print("Benutzung: python levenshtein.py wordpairs.txt")
        return

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            a, b = line.split("\t")

            d = levenshtein_matrix(a, b)
            dist = d[len(a)][len(b)]

            print(f"\n{a}-{b}: {dist}")

            alignments = backtrack_alignments(d, a, b)

            for x, y in alignments:
                print(f"{x}:{y}")


if __name__ == "__main__":
    main()