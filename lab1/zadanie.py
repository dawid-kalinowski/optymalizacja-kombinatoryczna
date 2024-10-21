import matplotlib.pyplot as plt
import networkx as nx

skierowany = input("Czy chcesz graf skierowany? (tak/nie): ").lower() == "tak"

file = open("lista.txt", "r")

# pobranie danych z pliku i stworzenie tablicy krawedzi oraz tablicy wierzcholkow
krawedzie = []
wierzcholki = []

# sortowanie krawedzi (przy nieskierowanych grafach sortujemy, a przy skierowanych nie)
def sort(krawedz):
    return ''.join(sorted(krawedz)) if not skierowany else krawedz

# wczytanie danych z pliku
for x in file:
    x = x.replace("\n", "")
    krawedzie.append(sort(x))

# wypelnienie tablicy wierzcholkami
for krawedz in krawedzie:
    for wierzcholek in krawedz:
        if wierzcholek not in wierzcholki:
            wierzcholki.append(wierzcholek)

wierzcholki.sort()
print("Wierzchołki: ", wierzcholki)

macierz_sasiedztwa = []

def wypelnij_macierz():

    # stworzenie macierzy wypelnionej zerami
    global macierz_sasiedztwa
    macierz_sasiedztwa = [[0 for _ in wierzcholki] for _ in wierzcholki]

    # wypelnienie macierzy jedynkami tam, gdzie wierzcholki sąsiadują (dla nieskierowanego robimy macierz symetryczną względem przekątnej)
    for krawedz in krawedzie:
        u, v = sort(krawedz)
        macierz_sasiedztwa[wierzcholki.index(u)][wierzcholki.index(v)] = 1
        if not skierowany:
            macierz_sasiedztwa[wierzcholki.index(v)][wierzcholki.index(u)] = 1

    print("  ", " ".join(wierzcholki))
    for i in range(len(wierzcholki)):
        print(wierzcholki[i], macierz_sasiedztwa[i])

# rysowanie grafu
def rysuj_graf():
    G = nx.DiGraph() if skierowany else nx.Graph()
    G.add_edges_from(krawedzie)
    pos = nx.spring_layout(G)
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=500)
    plt.savefig("plot.png")

# funkcja liczaca stopnie w grafie skierowanym i nieskierowanym
def stopien_wierzcholka(wierzcholek):
    index = wierzcholki.index(wierzcholek)
    if skierowany:
        # stopień wychodzący to 1 w wierszu danego wierzchołka
        stopien_wychodzacy = sum(macierz_sasiedztwa[index])
        # a wchodzący to 1 w kolumnie
        stopien_wchodzacy = sum(row[index] for row in macierz_sasiedztwa)
        return stopien_wychodzacy, stopien_wchodzacy
    else:
        # a dla nieskierowanego po prostu sumujemy wszystkie krawędzie
        return sum(macierz_sasiedztwa[index]), None

# funkcja sumujaca wierzchołki parzyste  i nieparzyste
def parzyste_nieparzyste():
    parzyste = nieparzyste = 0
    for wierzcholek in wierzcholki:
        stopien, _ = stopien_wierzcholka(wierzcholek)
        if stopien % 2 == 0:
            parzyste += 1
        else:
            nieparzyste += 1
    return parzyste, nieparzyste


def main():
    global skierowany

    wypelnij_macierz()
    rysuj_graf()

    while True:
        print("\nOpcje:")
        print("1 - Dodaj wierzchołek")
        print("2 - Usuń wierzchołek")
        print("3 - Dodaj krawędź")
        print("4 - Usuń krawędź")
        print("5 - Stopień wierzchołka")
        print("6 - Minimalny i maksymalny stopień grafu")
        print("7 - Liczba wierzchołków o stopniu parzystym i nieparzystym")
        print("8 - Posortowany ciąg stopni wierzchołków")
        print("exit - Wyjście")

        option = input("Wybierz opcję: ")

        if option == "1":
            my_wierzcholek = input("Podaj literę wierzchołka, który chcesz dodać: ")
            if my_wierzcholek.isalpha() and len(my_wierzcholek) == 1:
                if my_wierzcholek not in wierzcholki:
                    wierzcholki.append(my_wierzcholek)
                    wierzcholki.sort()
                    print("Wierzchołki: ", wierzcholki)
                    wypelnij_macierz()
                    rysuj_graf()
                else:
                    print("Wierzchołek już istnieje.")
            else:
                print("Wierzchołek musi być pojedynczą literą.")

        elif option == "2":
            my_wierzcholek = input("Podaj literę wierzchołka, który chcesz usunąć: ")
            if my_wierzcholek in wierzcholki:
                krawedzie[:] = [krawedz for krawedz in krawedzie if my_wierzcholek not in krawedz]
                wierzcholki.remove(my_wierzcholek)
                wierzcholki.sort()
                print("Wierzchołki: ", wierzcholki)
                wypelnij_macierz()
                rysuj_graf()
            else:
                print("Taki wierzchołek nie istnieje.")

        elif option == "3":
            my_krawedz = input("Podaj krawędź (w formacie AB): ").lower()
            if len(my_krawedz) == 2 and my_krawedz[0].isalpha() and my_krawedz[1].isalpha():
                sorted_krawedz = sort(my_krawedz)
                if sorted_krawedz not in krawedzie:
                    krawedzie.append(sorted_krawedz)
                    print("Krawędzie: ", krawedzie)
                    wypelnij_macierz()
                    rysuj_graf()
                else:
                    print("Taka krawędź już istnieje.")
            else:
                print("Krawędź musi być w formacie dwóch liter.")

        elif option == "4":
            my_krawedz = input("Podaj krawędź do usunięcia (w formacie AB): ").lower()
            sorted_krawedz = sort(my_krawedz)
            if sorted_krawedz in krawedzie:
                krawedzie.remove(sorted_krawedz)
                print("Krawędzie: ", krawedzie)
                wypelnij_macierz()
                rysuj_graf()
            else:
                print("Taka krawędź nie istnieje.")

        elif option == "5":
            my_wierzcholek = input("Podaj wierzchołek, aby sprawdzić jego stopnie: ").lower()
            if my_wierzcholek in wierzcholki:
                stopien_wychodzacy, stopien_wchodzacy = stopien_wierzcholka(my_wierzcholek)
                if skierowany:
                    print(f"Wierzchołek {my_wierzcholek.upper()}:")
                    print(f"Stopień wychodzący: {stopien_wychodzacy}")
                    print(f"Stopień wchodzący: {stopien_wchodzacy}")
                else:
                    print(f"Stopień wierzchołka {my_wierzcholek.upper()}: {stopien_wychodzacy}")
            else:
                print("Taki wierzchołek nie istnieje.")

        elif option == "6":
            stopnie = [sum(macierz_sasiedztwa[i]) for i in range(len(wierzcholki))]
            min_stopien = min(stopnie)
            max_stopien = max(stopnie)
            wierzcholki_min = [wierzcholki[i] for i, stopien in enumerate(stopnie) if stopien == min_stopien]
            wierzcholki_max = [wierzcholki[i] for i, stopien in enumerate(stopnie) if stopien == max_stopien]
            
            print(f"Minimalny stopień: {min_stopien}, wierzchołki: {', '.join(wierzcholki_min).upper()}")
            print(f"Maksymalny stopień: {max_stopien}, wierzchołki: {', '.join(wierzcholki_max).upper()}")


        elif option == "7":
            parzyste, nieparzyste = [], []
            for i in range(len(wierzcholki)):
                stopien = sum(macierz_sasiedztwa[i])
                if stopien % 2 == 0:
                    parzyste.append(wierzcholki[i])
                else:
                    nieparzyste.append(wierzcholki[i])

            print(f"Wierzchołki parzyste: {len(parzyste)}: {', '.join(parzyste).upper()}")
            print(f"Wierzchołki nieparzyste: {len(nieparzyste)}: {', '.join(nieparzyste).upper()}")


        elif option == "8":
            stopnie = [(wierzcholki[i], sum(macierz_sasiedztwa[i])) for i in range(len(wierzcholki))]
            stopnie.sort(key=lambda x: x[1], reverse=True)
            for wierzcholek, stopien in stopnie:
                print(f"Wierzchołek {wierzcholek.upper()}: stopień {stopien}")


        elif option == "exit":
            break

if __name__ == "__main__":
    main()
