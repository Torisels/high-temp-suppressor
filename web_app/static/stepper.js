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
        try {
            xhr.send();
        } catch (e) {
            // console.log(e)
        }
    });
}

function set_stepper_status(status) {
    let element = document.getElementById("stepper_status");
    element.innerText = status;
    if (status === "Enabled") {
        element.classList = ["text-success"];
    } else if (status === "Disabled") {
        element.classList = ["text-danger"];
    } else if (status === "Moving") {
        element.innerText += "...";
        element.classList = ["text-primary"];
    }

}


class Stepper {


    constructor(info, url, slider) {

        this.slider = slider;
        this.slider.on("slide", function (sliderValue) {
            document.getElementById("ex6SliderVal").textContent = sliderValue;
        });
        this.slider.on("change", function (value) {
            document.getElementById("ex6SliderVal").textContent = value.newValue;
        });

        this.mode = "man";
        let information = JSON.parse(info);
        this.status = information.status;
        this.calibration = false;
        this.steps = information.steps;
        this.min_pos = parseInt(information.min_position);
        this.max_pos = parseInt(information.max_position);
        this.current_pos = parseInt(information.current_position);
        this.url = url + "/stepper";
        this.slider.setValue(this.current_pos);
        this.scheduled_pos = -1;
        console.log("here");

        document.getElementById("btn_mode_auto").onclick = (ev)=>{
            console.log("here");
            this.mode_btn_clicked("Auto");
            this.mode = "aut";
            this.toggle_buttons(false);
        };

        document.getElementById("btn_mode_manual").onclick = (ev)=>{
            console.log("her2e");
            this.mode_btn_clicked("Manual");
            this.mode = "man";
            this.toggle_buttons(true);
        };

        this.btn_toggle = document.getElementById("btn_toggle");
        this.btn_toggle.onclick = (event) => this.toggle_button_clicked(event);
        this.btn_move = document.getElementById("btn_move");
        this.btn_move.onclick = (event) => this.move_btn_clicked(event);
        document.getElementById("btn_open").onclick = (event) => this.open_close_btn_clicked("open");
        document.getElementById("btn_close").onclick = (event) => this.open_close_btn_clicked("close");

        this.calib_buton = document.getElementById("btn_calibration");
        this.calib_buton.onclick = (event) => this.calibration_button_clicked();

        document.getElementById("manually").onclick = (ev) => {
            this.current_pos = 880;
            this.max_pos = 880;
            makeRequest("GET", this.url + "/set_current_position/" + this.current_pos);
            makeRequest("GET", this.url + "/set_max_position/" + this.current_pos);
        };

        if (this.status) {
            this.change_btn_toggle("Disable");
            set_stepper_status("Enabled");
            this.calib_buton.removeAttribute("disabled");

        } else {
            this.change_btn_toggle("Enable");
            set_stepper_status("Disabled");
            this.calib_buton.setAttribute("disabled", "disabled");

        }

        let evtSource = new EventSource(url + "/stream");
        const that = this;
        evtSource.onmessage = (e) => {
            info = JSON.parse(e.data);
            if (info.status === false) {
                document.getElementById("alert_stepper_disabled").style.display = "";
                document.getElementById("alert_stepper_disabled").classList.add("show");
                this.calib_buton.setAttribute("disabled", "disabled");
                this.status = false;
                that.change_btn_toggle("Enable");

                this.current_pos = info.current_pos;
                this.scheduled_pos = this.current_pos;
                set_stepper_status("Disabled");

            } else if (info.status === true && this.status && this.calibration===false) {

                set_stepper_status("Moving");
                this.current_pos = info.current_pos;
                if (this.scheduled_pos === this.current_pos)
                    set_stepper_status("Enabled");
                this.update_dom();
            }
        };
        this.update_dom();

        this.slider.setValue(this.calculate_percentage());
        document.getElementById("ex6SliderVal").textContent = this.calculate_percentage();

    }


    mode_btn_clicked(mode)
    {
        if (mode ==="Auto")
        {

        }
    }

    change_btn_toggle(state) {
        this.btn_toggle.innerText = state;
        if (state === "Enable") {
            btn_toggle.classList.remove("btn-danger");
            btn_toggle.classList.add("btn-success");
            this.toggle_buttons(false);
        } else {
            btn_toggle.classList.add("btn-danger");
            btn_toggle.classList.remove("btn-success");
            if (this.calibration === false)
                this.toggle_buttons(true);
        }
    }

    async toggle_button_clicked() {
        if (this.status) {
            let response = await makeRequest("GET", this.url + "/set_status/0");
            // let response = true;
            response = JSON.parse(response);
            if (response.success === true && response.value === false) {
                this.status = false;

                this.change_btn_toggle("Enable");
                set_stepper_status("Disabled");
                this.calib_buton.setAttribute("disabled", "disabled");

            }
        } else {
            let response = await makeRequest("GET", this.url + "/set_status/1");
            // let response = true;
            response = JSON.parse(response);
            if (response.success === true && response.value === true) {
                document.getElementById("alert_stepper_disabled").style.display = "none";
                this.status = true;
                this.change_btn_toggle("Disable");
                set_stepper_status("Enabled");
                this.calib_buton.removeAttribute("disabled");
            }
        }
    }

    calculate_percentage() {
        if (this.max_pos === 0)
            return 0;
        return Math.round(((this.current_pos + Number.EPSILON) / this.max_pos) * 100)
    }

    update_dom() {
        document.getElementById("stepper_val").innerText = this.calculate_percentage().toString();
        // document.getElementById("progress_bar").style.width = this.calculate_percentage().toString()+"%";
    }

    move_btn_clicked(event, val = -1) {
        if (this.status) {
            if (val === -1)
                val = this.slider.getValue();
            val = Math.round((val / 100) * this.max_pos);
            this.scheduled_pos = val;
            console.log(val);
            makeRequest("GET", this.url + "/set_position/" + val)
        }
    }

    open_close_btn_clicked(ty) {
        if (ty === "open") {
            document.getElementById("ex6SliderVal").textContent = 0;
            this.slider.setValue(0);
            this.move_btn_clicked(0);
        } else {
            document.getElementById("ex6SliderVal").textContent = 100;
            this.slider.setValue(100);
            this.move_btn_clicked(100);
        }
    }

    move_by_val(val)
    {

        if (this.mode==="aut" && this.calibration===false)
        {
            val = Math.round((val / 100) * this.max_pos);
            this.scheduled_pos = val;
            makeRequest("GET", this.url + "/set_position/" + val)
        }

    }

    toggle_buttons(enable) {
        let l = document.querySelectorAll("button.toggle");


        for (const el of l) {
            if (enable)
                el.removeAttribute("disabled");
            else
                el.setAttribute("disabled", "disabled");
        }

    }

    calibration_button_clicked() {
        this.calibration = true;
        let content = document.getElementById("div_calibration");
        if (content.style.display === "") {
            window.scrollTo({top: 0, behavior: 'smooth'});
            $("#div_calibration").fadeOut(400);
            this.toggle_buttons(true);
        } else {
            $("#div_calibration").fadeIn(400);
            $("html, body").animate({scrollTop: document.body.scrollHeight}, "slow");
            this.toggle_buttons(false);
            this.current_pos = 0;
            this.scheduled_pos = 0;
            makeRequest("GET", this.url + "/set_current_position/0");
            this.update_dom();
        }

    }

    move_step_zero(value) {
        makeRequest("GET", this.url + "/set_steps/" + value);
        makeRequest("GET", this.url + "/set_max_position/" + 1000);

    }

    move_step_one(value) {
        this.current_pos += value;
        if (this.current_pos <= 0) {
            this.current_pos = 0;
            document.getElementById("btn_minus").setAttribute("disabled", "disabled");
        } else {
            document.getElementById("btn_minus").removeAttribute("disabled");
        }
        makeRequest("GET", this.url + "/set_position/" + this.current_pos);
    }

    move_step_complete() {
        this.calibration = false;
        this.max_pos = this.current_pos;
        makeRequest("GET", this.url + "/set_max_position/" + this.current_pos);
        this.toggle_buttons(true);
        this.update_dom();
    }
}
