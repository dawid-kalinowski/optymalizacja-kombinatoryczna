file = open("lista.txt", "r")

# pobranie danych z pliku i stworzenie tablicy krawedzi oraz tablicy wierzcholkow
krawedzie = []
wierzcholki = []

for x in file:
    x = x.replace("\n", "")
    krawedzie.append(x)

for x in file:
    print()

print(krawedzie)

for krawedz in krawedzie:
    for wierzcholek in krawedz:
        if wierzcholek not in wierzcholki:
            wierzcholki.append(wierzcholek)

wierzcholki.sort()
print(wierzcholki)

# stworzenie macierzy sasiedztwa
macierz_sasiedztwa = []
for i in wierzcholki:
    wiersz = []
    for j in wierzcholki:
        wiersz.append(0)
    macierz_sasiedztwa.append(wiersz)

print(macierz_sasiedztwa)
