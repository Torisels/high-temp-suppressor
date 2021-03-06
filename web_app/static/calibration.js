"use strict";


let current_step = 0;

const information = ["Please move window blinds to horizontal position. \n Then click `next step`.",
    "Please move window blinds to vertical position (fully closed). <br>Click `Complete!` to finish the process."
];


let buttons = ["btn_plus", "btn_minus"];


let current_scale = 100;

(function () {


    for (const btn_name of buttons) {
        console.log(btn_name);
        document.getElementById(btn_name).onclick = button_clicked;
    }

    let scale_buttons = document.getElementsByClassName("btn_scale");
    for (const scale_btn of scale_buttons) {
        scale_btn.onclick = scale_button_clicked;
    }
    document.getElementById("scale_value").innerText = `Current scale: ${current_scale}`;

    let step_btns = document.getElementsByClassName("step");
    for (const btn of step_btns) {
        btn.onclick = calibration_step_button_clicked;
    }
    handle_step_state();


})();


function button_clicked() {
    if (this.id === "btn_plus") {
        if (current_step === 0) {
            console.log("plus");
            stepper.move_step_zero(current_scale)
        } else if (current_step === 1) {
            console.log("here");
            stepper.move_step_one(current_scale);
        }

    } else if (this.id === "btn_minus") {
        if (current_step === 0) {
            stepper.move_step_zero(-1 * current_scale);
            console.log("minus")
        } else if (current_step === 1) {
              stepper.move_step_one(-1*current_scale);
        }
    }

}


function scale_button_clicked() {
    console.log("here");
    let scale = +this.innerText;
    console.log(this.innerText);
    current_scale = scale;
    document.getElementById("scale_value").innerText = `Current scale: ${current_scale}`;
}


function calibration_step_button_clicked() {
    if (this.id === "next") {
        current_step++;
        if (current_step > 1)
            current_step = 1;
    } else if (this.id === "previous") {
        if (current_step > 0)
            current_step--;
    } else {
        window.scrollTo({top: 0, behavior: 'smooth'});
        $("#div_calibration").fadeOut(400);
        current_step = 0;
        stepper.move_step_complete();
        document.getElementById("alert_calib_success").style.display = "";
        document.getElementById("alert_calib_success").classList.add("show");
    }

    console.log(current_step);
    handle_step_state();
}


function handle_step_state() {
    let previous = document.getElementById("previous");
    let next = document.getElementById("next");
    let complete = document.getElementById("btn_complete");
    let information_box = document.getElementById("information_box");
    information_box.innerHTML = information[current_step];
    switch (current_step) {

        case 0: {
            previous.setAttribute("disabled", "disabled");
            complete.setAttribute("disabled", "disabled");
            next.removeAttribute("disabled");
             document.getElementById("btn_minus").removeAttribute("disabled");
            information_box.innerText = information[current_step];
            break;
        }
        case 1:
            previous.removeAttribute("disabled");
            complete.removeAttribute("disabled");
            next.setAttribute("disabled", "disabled");
            if (stepper.current_pos===0)
                document.getElementById("btn_minus").setAttribute("disabled", "disabled");
            break;
    }
}