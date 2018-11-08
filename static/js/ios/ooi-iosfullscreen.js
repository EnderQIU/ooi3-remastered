window.onload = function () {
    let scale = window.screen.height / 720.0;
    let viewport = document.querySelector("meta[name=viewport]");
    viewport.setAttribute('content', 'width=device-width user-scalable=0 initial-scale='+scale.toFixed(2));
};