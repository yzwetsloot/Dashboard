function htmlDecode(input) {
    const doc = new DOMParser().parseFromString(input, "text/html");
    return doc.documentElement.textContent;
}

function setCollapsible() {
    const coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function(event) {
            if (event.target.className !== "treshold-search" && event.target.className !== "treshold-button") {
                this.classList.toggle("active");
                let content = this.nextElementSibling;

                let price_info = content.children[0];
                let price_chart = content.children[2];

                let quantity_info = content.children[1];
                let quantity_chart = content.children[3];

                render(price_info.getAttribute("data-chart"), price_chart.id);
                render(quantity_info.getAttribute("data-chart"), quantity_chart.id);

                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            }
        });
    }
}

function postTreshold(form) {
    if (form.children.length === 3) {
        form.removeChild(form.children[2]);
    }

    form.children[0].style.borderColor = "lightgrey";
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("successful submission");

                let icon = document.createElement("i");
                icon.className = "fa fa-check-circle";
                icon.style.color = "#4bae50";
                icon.style.position = "absolute";
                icon.style.right = "auto";
                icon.style.padding = "4px 0 0 2px";
                form.appendChild(icon);

                form.reset();
            } else {
                let icon = document.createElement("i");
                icon.className = "fa fa-times-circle";
                icon.style.color = "tomato";
                icon.style.position = "absolute";
                icon.style.right = "auto";
                icon.style.padding = "4px 0 0 2px";
                form.appendChild(icon);

                console.log("submission failed")
            }
        }
    };

    xhr.open("POST", "/treshold");

    let url = form.getAttribute("data-url");

    let payload = new FormData(form);
    payload.append("url", url);
    xhr.send(payload);

    return false;
}

function postAutoBuy(toggle) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log("successful submission");
            } else {
                toggle.checked = false;
                console.log("submission failed")
            }
        }
    };

    xhr.open("POST", "/auto_buy");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    let url = toggle.getAttribute("data-url");
    xhr.send(`url=${url}&auto_buy=${toggle.checked}`);
}

function warn(textbox) {
    textbox.style.borderColor = "tomato";
}

function render(data, id) {
    let figure = JSON.parse(htmlDecode(data));
    Plotly.newPlot(id, figure.data, figure.layout, {staticPlot: true});
}

window.addEventListener('load', function () {
    setCollapsible();
});
