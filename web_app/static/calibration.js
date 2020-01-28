"use strict";


let current_step = 0;

const information = ["Please move window blinds to horizontal position. (fully open)",
"Please move window blinds to vertical position (fully closed)"
];


let buttons = ["btn_plus", "btn_minus"];



let current_scale = 100;

(function() {

    let buttons_listeners = [];

    for (const btn_name of buttons){
        console.log(btn_name);
        document.getElementById(btn_name).onclick = button_clicked;
    }

    let scale_buttons = document.getElementsByClassName("scale");
    for (const scale_btn of scale_buttons)
    {
        scale_btn.onclick = scale_button_clicked;
    }
    document.getElementById("scale_value").innerText = `Current scale: ${current_scale}`;

    let step_btns = document.getElementsByClassName("step");
    for (const btn of step_btns)
    {
        btn.onclick = calibration_step_button_clicked;
    }
    handle_step_state();



})();


function button_clicked() {
    console.log(this.id);
}


function scale_button_clicked()
{
    let scale = +this.innerText;
    current_scale = scale;
    document.getElementById("scale_value").innerText = `Current scale: ${current_scale}`;
}


function calibration_step_button_clicked()
{
    if (this.id === "next")
    {
        current_step ++;
    }
    else
    {
        if (current_step > 0){
            current_step --;
        }
    }

    console.log(current_step);
    handle_step_state();
}



function handle_step_state()
{
    let previous = document.getElementById("previous");
    let next = document.getElementById("next");
    switch (current_step) {

        case 0:
        {
            previous.setAttribute("disabled", "disabled");
            break;
        }
        case 1:
            previous.removeAttribute("disabled");
            break;
    }
}