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
W wyniku testowania i oględzin mechanizmu żaluzji najlepszym rozwiązaniem sterowania mechanizmem pochylania piór
będzie bezpośrednie połączenie wału żaluzji wraz z silnikiem poprzez przekładnię _4-6:1_

Średnica wału żaluzji wynosi 3,6mm, z wcięciem 2,6mm. 