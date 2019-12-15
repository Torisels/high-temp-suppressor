### PyCharm
[Korzystanie z pycharm wraz z micropythonem](https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/)


#### Obserwacje wynikające z pracy silnika krokowego:
[Źródło mówiące o ilości kroków w silniku](http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html)

W wyniku serii przeprowadzonych testów nad silnikiem krokowym 28BYJ-48
sterowanym przez sterownik ULN2003 w trybie FULL STEP silnik ma następujące parametry:
 * pobór prądu wynosi od 200 do 250 mA
 * czas pełnego obrotu wynosi 4.2s
 * silnik na pełen obrót potrzebuje niecałe 2038 kroków (2037.886), co daje dokładność 0.1766 stopnia.
 * optymalne opóźnienie pomiędzy krokami wynosi 2ms
 
 

#### Żaluzje:
Głównym założeniem przy doborze żaluzji było posiadanie wału odpowiedniego do takiej modyfikacji, która pozwoliłaby
użyć silnika krokowego do regulacji nachylenia piór żaluzji. 

Zakupiona żaluzja ma _x_ mm długości.

Rozważyliśmy kilka opcji montażu silnika, początkowo planowany był montaż wewnątrz ramy, 
łącząc oś silnika bezpośrednio z elementem do ręcznej regulacji położonego pod kątem 90 stopni do wału 
umożliwiłoby sterowanie.

Cały natywny mechanizm do regulacji nachylenia żaluzji wraz z przekłądnią został jednak zdemontowany,
ponieważ w wyniku testowania i oględzin mechanizmu najlepszym rozwiązaniem okazało się 
bezpośrednie połączenie wału żaluzji wraz z silnikiem poprzez przekładnię _4:1_

Różne testy wykazały, iż najlepiej skorzystać z przekładni planetarnej
o wspomnianym wyżej przełożeniu _4:1_.

Przekładnia użyta w projekcie pochodzi z [Thingiverse](https://www.thingiverse.com/thing:3642542).
Element o nazwie _planet-carrier.stl_ został zmodyfikowany. 
W jego osi dodano tuleję, która swoim kształtem odpowiada kształtowi wału żaluzji, przez co może swobodnie się z nim połączyć.

Przy zastosowaniu powyższej przekładni na jeden obrót wału żaluzji przypadają *8152* kroki silnika krokowego (8151.5).

Do precyzyjnej kalibracji silnika krokowego użytkownik będzie mógł użyć rotary encodera.
Domyślnie jeden obrót encoderem będzie oznaczał _1/4_ obrotu głownego wału. 

Daje to przelicznik 1 puls = 2038/4 kroków => 1 puls = 509 kroków




Średnica wału żaluzji wynosi 3,6mm, z wcięciem 2,6mm. 




#### Rama:
Wszystkie elementy wykorzystane do produkcji ramy pochodzą ze sklepu Leroy Merlin.

Materiał użyty do wytworzenia ramy to płyta wiórowa o szerokości _x_ mm, 
została wybrana ponieważ jest lekka, tania, dość trwała i sztywna.

Wymiary ramy dopasowane zostały do długości uprzednio kupionej żaluzji.
Cała rama ma wymiary _x_ mm (wysokość) na _y_ mm (szerokość) na _z_ mm (długość).

Poglądowy projekt ramy z wymiarami został przekazany pracownikowi sklepu, 
który przy użyciu odpowiednich narzędzi dociął płytę wiórową do pożądanych rozmiarów,
a do połączenia płyt użył konfirmatów do mebli o długości _63_ mm.

Elementy podtrzymujące żaluzję zostały zamontowane po złożeniu ramy, za pomocą zwykłych wkrętów do drewna.