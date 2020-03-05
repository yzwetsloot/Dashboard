function htmlDecode(input) {
    const doc = new DOMParser().parseFromString(input, "text/html");
    return doc.documentElement.textContent;
}

function setCollapsible() {
    const coll = document.getElementsByClassName("collapsible");
    let i;

    for (i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
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
        });
    }
}

function render(data, id) {
    let figure = JSON.parse(htmlDecode(data));
    Plotly.newPlot(id, figure.data, figure.layout);
}

window.addEventListener('load', function () {
    setCollapsible();
});
