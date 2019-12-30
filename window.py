
class window():

    def decision(self, tin, tout, humin, humout, lightin, lightout, optimal1=21, optimal2=28):
        # optymalna temperatura 21C - 28C
        # optymalna wilgotnosc od 40% do 70%
        # Zrodlo: https://www.weather.gov/media/epz/wxcalc/heatIndex.pdf
        tin = 9 / 5 * tin + 32  # konwersja na Fahrenheita
        tout = 9 / 5 * tout + 32
        heatin = -42.379 + 2.04901523 * tin + 10.14333127 * humin - .122475541 * tin * humin - .00683783 * tin * tin\
                 - .05481717 * humin * humin + .00122874 * tin * tin * humin + .00085282 * tin * humin * humin \
                 - .00000199 * tin * tin * humin * humin

        heatout = -42.379 + 2.04901523 * tout + 10.14333127 * humout - .122475541 * tout * humout - .00683783 * tout * tout \
             - .05481717 * humout * humout + .00122874 * tout * tout * humout + .00085282 * tout * humout * humout \
                  - .00000199 * tout * tout * humout * humout

        heatin = (heatin-32)*5/9    # konwersja na Celsjusza
        heatout = (heatout-32)*5/9
        s = 'Odczuwalna temperatura w pomieszczeniu wynosi: ' + str(round(heatin, 2)) + "°C" + '\n'
        if optimal2 > heatin > optimal1:
            if heatin > heatout and lightout > 35000:
                s += 'Odczuwalna temperatura znajduje sie w podanym optymalnym przedziale. Jesli chcesz, aby było chlodniej uchyl okno.'
            elif heatin > heatout:
                s += 'Odczuwalna temperatura znajduje sie w podanym optymalnym przedziale. Jesli chcesz, aby bylo chłodniej otworz okno.'
            else:
                s += 'Odczuwalna temperatura znajduje sie w podanym optymalnym przedziale. Jesli chcesz, aby bylo cieplej otworz okno.'
        else:
            if heatin > optimal2:
                if heatin > heatout and lightout > 35000:
                    s += 'Zalecamy uchylic okno w celu osiagniecia temperatury blizszej optymalnej.'
                elif heatin > heatout:
                    s += 'Zalecamy otworzyc okno w celu osiagniecia temperatury blizszej optymalnej.'
                else:
                    s += 'Nie zalecamy otwierac okien. Będzie jeszcze cieplej.'
            else:
                if heatin < heatout:
                    s += 'Zalecamy otworzyc okno w celu osiągniecia temperatury blizszej optymalnej.'
                else:
                    s += 'Nie zalecamy otwierac okien. Bedzie jeszcze zimniej.'
        return s

