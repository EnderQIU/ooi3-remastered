function setScale() {
    let scale = window.screen.width / 720.0;
    let viewport = document.querySelector("meta[name=viewport]");
    viewport.setAttribute('content', 'width=device-width user-scalable=yes initial-scale=' + scale.toFixed(2));
}
