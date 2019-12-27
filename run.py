from web_app import app
import hardware_manager.step as step
import hardware_manager.dht as dht
import RPi.GPIO as GPIO
import threading

def run():
	step.Stepper.get_instance()
	dht.DHSensor.get_instance()
	t2 = threading.Thread(target=app.run, args=('0.0.0.0', 8081,))
	t2.start()

if __name__ == '__main__':
	run()
