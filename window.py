
class window():

    def decision(self, tin, tout, humin, humout, lightin, lightout, optimal1=21, optimal2=28):
        # optymalna temperatura 21C - 28C
        # optymalna wilgotnoÅÄ od 40% do 70%
        # Å¹rÃ³dÅo: https://www.weather.gov/media/epz/wxcalc/heatIndex.pdf
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
        s = 'Odczuwalna temperatura w pomieszczeniu wynosi: ' + str(round(heatin, 2)) + "Â°C" + '\n'
        if optimal2 > heatin > optimal1:
            if heatin > heatout and lightout > 35000:
                s += 'Odczuwalna temperatura znajduje siÄ w podanym optymalnym przedziale. JeÅli chcesz, aby byÅo chÅodniej uchyl okno.'
            elif heatin > heatout:
                s += 'Odczuwalna temperatura znajduje siÄ w podanym optymalnym przedziale. JeÅli chcesz, aby byÅo chÅodniej otwÃ³rz okno.'
            else:
                s += 'Odczuwalna temperatura znajduje siÄ w podanym optymalnym przedziale. JeÅli chcesz, aby byÅo cieplej owÃ³rz okno.'
        else:
            if heatin > optimal2:
                if heatin > heatout and lightout > 35000:
                    s += 'Zalecamy uchylic okno w celu osiÄgniÄcia temperatury bliÅ¼szej optymalnej.'
                elif heatin > heatout:
                    s += 'Zalecamy otworzyÄ okno w celu osiÄgniÄcia temperatury bliÅ¼szej optymalnej.'
                else:
                    s += 'Nie zalecamy otwieraÄ okien. BÄdzie jeszcze cieplej.'
            else:
                if heatin < heatout:
                    s += 'Zalecamy otworzyÄ okno w celu osiÄgniÄcia temperatury bliÅ¼szej optymalnej.'
                else:
                    s += 'Nie zalecamy otwieraÄ okien. BÄdzie jeszcze zimniej.'
        return s

