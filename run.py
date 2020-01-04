from web_app import app
from hardware_manager.step import Stepper
from hardware_manager.dht import DHTSensor
from hardware_manager.bh1750 import BH1750
import threading


def run():
    Stepper.get_instance()
    DHTSensor.get_instance("indoor")
#    BH1750.get_instance("indoor")
#    BH1750.get_instance("outdoor")
    # dht.DHSensor.get_instance_2()
    app.run("0.0.0.0", port=8081, threaded=True)


if __name__ == '__main__':
    run()
