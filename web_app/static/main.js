"use strict";


(async function () {

    $().alert();
    $('.alert').on('close.bs.alert', function (event) {
        event.preventDefault();
        document.getElementById("alert_calib_success").style.display = "none";
    });
    // $('.alert').alert();
    // $('.alert').show();
    let slider = new Slider("#ex6");
    slider.setValue(50);
    slider.on("slide", function(sliderValue) {
        document.getElementById("ex6SliderVal").textContent = sliderValue;
    });
    slider.on("change", function(value) {
        // console.log(old);
        document.getElementById("ex6SliderVal").textContent = value.newValue;
    });

    let calib_buton = document.getElementById("btn_calibration");
    calib_buton.onclick = calibration_button_clicked;

    // $('.alert').on('close.bs.alert', function (event) {
    //     event.preventDefault();
    //     document.getElementById(alert_calib_success).style.display = "none";
    // });
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