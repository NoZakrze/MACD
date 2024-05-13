import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
def EMA(dane,N,i):
    alfa = 2/(N+1)
    licznik = dane[i]
    mianownik = 1
    i -= 1
    j = 1
    while i >= 0 and j <= N:
        licznik += ((1-alfa)**j) * dane[i]
        mianownik += (1-alfa)**j
        j += 1
        i -= 1
    return licznik/mianownik
def okres_kupna_sprzedazy(macd, signal, poczatek, koniec, daty, notowania, nazwa1, nazwa2 ):
    rozmiar = koniec - poczatek
    kapitaly = [0] * rozmiar
    kapitaly[0] = 0
    akcje = 1000
    ilosc_akcji = [0] * rozmiar
    ilosc_akcji[0] = 1000
    part_macd = macd[poczatek:koniec]
    part_signal = signal[poczatek:koniec ]
    part_daty = daty[poczatek:koniec]
    part_notowania = notowania[poczatek:koniec]
    kupno = []
    sprzedaz = []
    print("Stan poczatkowy:")
    print(1000 * part_notowania[0])
    for i in range(1,len(part_notowania)):
        if part_macd[i] > part_signal[i] and part_macd[i - 1] < part_signal[i - 1]:
            if akcje == 0:
                akcje = kapitaly[i-1] // part_notowania[i]
                kapitaly[i] = kapitaly[i-1] - akcje*part_notowania[i]
                kupno.append((part_daty[i], part_notowania[i]))
        elif part_macd[i] < part_signal[i] and part_macd[i - 1] > part_signal[i - 1]:
            if akcje > 0:
                kapitaly[i] = kapitaly[i-1] + akcje * part_notowania[i]
                akcje = 0
                sprzedaz.append((part_daty[i], part_notowania[i]))
        else:
            kapitaly[i] = kapitaly[i-1]
        ilosc_akcji[i] = akcje
    for i in range(len(kapitaly)):
        if ilosc_akcji[i] != 0 or kapitaly[i] == 0:
            kapitaly[i] += ilosc_akcji[i] * part_notowania[i]

    plt.subplots_adjust(bottom=0.2, left=0.2, right=0.9, top=0.9)
    plt.plot(part_daty,kapitaly,label ="kapital")
    plt.gca().xaxis.set_major_locator(MultipleLocator(rozmiar/10))
    plt.xticks(rotation=30)
    plt.xlabel("Daty")
    plt.ylabel("Stan portfela w PLN")
    plt.title("Zmiany kapitalu w okreslonym okresie")
    plt.legend()
    plt.savefig(nazwa2)
    plt.show()

    plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9, top=0.9)
    plt.scatter([], [], color='green', label="Kupno")
    plt.scatter([], [], color='red', label="Sprzedaz")
    plt.plot(part_daty, part_notowania, label="notowania", color="blue")
    for point in kupno:
        plt.scatter(point[0], point[1], s=25, color="green")
    for point in sprzedaz:
        plt.scatter(point[0], point[1], s=25, color="red")
    plt.gca().xaxis.set_major_locator(MultipleLocator(rozmiar/10))
    plt.xticks(rotation=30)
    plt.xlabel("Daty")
    plt.ylabel("Cena akcji w PLN")
    plt.title("Miejsca kupna i sprzedazy")
    plt.legend()
    plt.savefig(nazwa1)
    plt.show()

    print("Stan koncowy:")
    if akcje == 0:
        print(kapitaly[rozmiar-1])
    else:
        print(akcje*part_notowania[rozmiar-1])



notowania = []
data = []
macd = [0] * 1000
signal = [0] * 1000
kupno = []
sprzedaz = []
kupno_n = []
sprzedaz_n= []

with open("dane.csv", newline='') as plik:
    scanner = csv.reader(plik, delimiter=',')
    for line in scanner:
        notowania.append(float(line[4]))
        data.append(line[0])

for i in range(len(notowania)):
    EMA12 = EMA(notowania,12,i)
    EMA26 = EMA(notowania,26,i)
    macd[i] = EMA12 - EMA26
    signal[i] = EMA(macd,9,i)
    if macd[i] > signal[i] and macd[i-1] < signal[i-1]:
        kupno.append((data[i],macd[i]))
        kupno_n.append((data[i], notowania[i]))
    if macd[i] < signal[i] and macd[i-1] > signal[i-1]:
        sprzedaz.append((data[i],macd[i]))
        sprzedaz_n.append((data[i], notowania[i]))

plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9, top=0.9)
plt.scatter([], [], color='green', label="Kupno")
plt.scatter([], [], color='red', label="Sprzedaz")
plt.plot(data,macd, label="macd", color = "blue")
plt.plot(data,signal, label="signal", color = "orange")
for point in kupno:
    plt.scatter(point[0],point[1], s=15, color = "green")
for point in sprzedaz:
    plt.scatter(point[0],point[1], s=15, color = "red")
plt.gca().xaxis.set_major_locator(MultipleLocator(95))
plt.xticks(rotation=30)
plt.xlabel("Daty")
plt.ylabel("wartosc linii macd i signal")
plt.title("Wskaznik MACD wraz z miejscami kupna/sprzedazy")
plt.legend()
plt.savefig('MACD-SIGNAL.png')
plt.show()


plt.subplots_adjust(bottom=0.2, left=0.1, right=0.9, top=0.9)
plt.plot(data, notowania, label="notowania", color = "blue")
plt.gca().xaxis.set_major_locator(MultipleLocator(95))
plt.xticks(rotation=30)
plt.xlabel("Daty")
plt.ylabel("Cena akcji w PLN")
plt.title("Notowania firmy PKN Orlen")
plt.legend()
plt.savefig('Notowania.png')
plt.show()


okres_kupna_sprzedazy(macd,signal,0,1000,data,notowania,"Notowania_caly_okres.png","Fundusze_caly_okres.png")
okres_kupna_sprzedazy(macd,signal,30,200,data,notowania,"Notowania_czesc1.png","Fundusze_czesc1.png")
okres_kupna_sprzedazy(macd,signal,350,476,data,notowania,"Notowania_czesc2.png","Fundusze_czesc2.png")
okres_kupna_sprzedazy(macd,signal,561,666,data,notowania,"Notowania_czesc3.png","Fundusze_czesc3.png")
okres_kupna_sprzedazy(macd,signal,833,950,data,notowania,"Notowania_czesc4.png","Fundusze_czesc4.png")

