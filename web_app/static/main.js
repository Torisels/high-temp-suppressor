"use strict";
// const API_BASE_URL = "http://192.168.1.20:8081/api";
const API_BASE_URL = "/api";

let stepper = null;

(async function () {
    let sl = new Slider("#ex6");
    $().alert();
    $('.alert').on('close.bs.alert', function (event) {
        event.preventDefault();
        let alerts  = document.getElementsByClassName("alert");
        for(let a of alerts)
        {
            a.style.display = "none"
        }
        // document.getElementById("alert_calib_success").style.display = "none";
    });

    let message = await makeRequest("GET", API_BASE_URL+"/message");
    message = JSON.parse(message);
    if (message.msg)
        document.getElementById("airing").innerHTML = message.msg;

    let evtSource = new EventSource(API_BASE_URL + "/msg");
    evtSource.onmessage = (e) => {
        message = JSON.parse(e.data);
        if(message.msg)
        {
            document.getElementById("airing").innerHTML = message.msg;
        }
    };

    document.getElementById("btn_open").onclick = update_sensors;
    update_sensors();
    window.setInterval(update_sensors, 1000);

    let stepper_data = await makeRequest("GET", API_BASE_URL+"/stepper/get_status");
    stepper = new Stepper(stepper_data, API_BASE_URL, sl);
    stepper.update_dom();


})();


// function calibration_button_clicked(stepper) {
//     let content = document.getElementById("div_calibration");
//     if (content.style.display === "") {
//         window.scrollTo({top: 0, behavior: 'smooth'});
//         $("#div_calibration").fadeOut(400);
//         stepper.toggle_buttons(true);
//     } else {
//         $("#div_calibration").fadeIn(400);
//         $("html, body").animate({scrollTop: document.body.scrollHeight}, "slow");
//         stepper.toggle_buttons(false);
//     }
// }

async function update_sensors() {
    try {
        let result = await makeRequest("GET", API_BASE_URL + "/sensors");
        let data = JSON.parse(result);

        for (const [sensors_type, sensors_values] of Object.entries(data)) {
            for (const [sensor_name, sensor_value] of Object.entries(sensors_values)) {
                let el = document.querySelector(`span.${sensors_type}.${sensor_name}`);
                if (sensor_value == null)
                    el.innerHTML = "N/A";
                else
                    el.innerHTML = sensor_value
            }
        }
    }
    catch (e) {
        // console.log(e);
    }
}



function set_stepper_status(status) {
    let element = document.getElementById("stepper_status");
    element.innerText = status;
    if (status === "Enabled")
    {
        element.classList = ["text-success"];
    }
    else if (status === "Disabled"){
        element.classList = ["text-danger"];
    }
    else if (status === "Moving"){
        element.innerText +="...";
        element.classList = ["text-primary"];
    }

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
        try{
        xhr.send();
        }
        catch (e) {
            // console.log(e)
        }
    });
}