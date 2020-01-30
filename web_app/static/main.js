"use strict";
const API_BASE_URL = "http://192.168.1.20:8081/api";



(async function () {

    $().alert();
    $('.alert').on('close.bs.alert', function (event) {
        event.preventDefault();
        document.getElementById("alert_calib_success").style.display = "none";
    });
    let slider = new Slider("#ex6");
    slider.setValue(50);
    slider.on("slide", function (sliderValue) {
        document.getElementById("ex6SliderVal").textContent = sliderValue;
    });
    slider.on("change", function (value) {
        document.getElementById("ex6SliderVal").textContent = value.newValue;
    });

    let calib_buton = document.getElementById("btn_calibration");
    calib_buton.onclick = calibration_button_clicked;

    document.getElementById("btn_open").onclick = update_sensors;

})();


function calibration_button_clicked() {
    let content = document.getElementById("div_calibration");
    if (content.style.display === "") {
        window.scrollTo({top: 0, behavior: 'smooth'});
        $("#div_calibration").fadeOut(400);
    } else {
        $("#div_calibration").fadeIn(400);
        $("html, body").animate({scrollTop: document.body.scrollHeight}, "slow");
    }
}

async function update_sensors() {
    let result = await makeRequest("GET", API_BASE_URL+"/sensors");
    console.log(result);
}

function makeRequest(method, url) {
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send();
    });
}