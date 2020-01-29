from flask import Flask
from flask import render_template, send_from_directory
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.xhtml', temp_1=123, hum_1=88)


@app.route("/calibration")
def calib():
    return render_template("calibration.html")



if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
