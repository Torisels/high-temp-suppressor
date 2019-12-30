
class window():

    def decision(self, tin, tout, humin, humout, lightin, lightout, optimal1=21, optimal2=28):
        # Optimal temperature is usually claimed to be between 21°C - 28°C, but there is room for customization
        # Source: https://www.weather.gov/media/epz/wxcalc/heatIndex.pdf
        tin = 9 / 5 * tin + 32  # Fahrenheit conversion
        tout = 9 / 5 * tout + 32
        heatin = -42.379 + 2.04901523 * tin + 10.14333127 * humin - .122475541 * tin * humin - .00683783 * tin * tin\
                 - .05481717 * humin * humin + .00122874 * tin * tin * humin + .00085282 * tin * humin * humin \
                 - .00000199 * tin * tin * humin * humin # Equation for apparent temperature

        heatout = -42.379 + 2.04901523 * tout + 10.14333127 * humout - .122475541 * tout * humout - .00683783 * tout * tout \
             - .05481717 * humout * humout + .00122874 * tout * tout * humout + .00085282 * tout * humout * humout \
                  - .00000199 * tout * tout * humout * humout

        heatin = (heatin-32)*5/9    # Celsius conversion
        heatout = (heatout-32)*5/9
        s = 'Apparent temperature in a room equals to: ' + str(round(heatin, 2)) + "°C" + '\n'
        if optimal2 > heatin > optimal1:
            if heatin > heatout and lightout > 35000:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to decrease temperature in the room, tilt the window.'
            elif heatin > heatout:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to decrease temperature in the room, open the window.'
            else:
                s += 'Apparent temperature is located in given optimal temperature range. If you want to increase temperature in the room, open the window.'
        else:
            if heatin > optimal2:
                if heatin > heatout and lightout > 35000:
                    s += 'It is advised to tilt the window to achieve temperature closer to optimum range.'
                elif heatin > heatout:
                    s += 'It is advised to open the window achieve temperature closer to optimum range.'
                else:
                    s += 'It is not advised to open the window. It will only get hotter.'
            else:
                if heatin < heatout:
                    s += 'It is advised to open the window achieve temperature closer to optimum range.'
                else:
                    s += 'It is not advised to open the window. It will only get hotter.'
        return s

