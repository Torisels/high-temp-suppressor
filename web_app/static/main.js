"use strict";


(async function () {
    let slider = new Slider("#ex6");
    slider.setValue(22.2);
    slider.on("slide", function(sliderValue) {
        document.getElementById("ex6SliderVal").textContent = sliderValue;
    });

    let calib_buton = document.getElementById("btn_calibration");
    calib_buton.onclick = calibration_button_clicked;
})();


function calibration_button_clicked() {
    let content = document.getElementById("div_calibration");
    if (content.style.display==="")
    {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        $("#div_calibration").fadeOut(400);
    }
    else{
        $("#div_calibration").fadeIn(400);
        $("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");
    }
}