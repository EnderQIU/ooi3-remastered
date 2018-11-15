function setScale() {
    let scale = window.screen.width / 720.0;
    let viewport = document.querySelector("meta[name=viewport]");
    viewport.setAttribute('content', 'width=device-width user-scalable=yes initial-scale=' + scale.toFixed(2));

    // center the iframe
    let left = (document.body.scrollWidth  - 1200) / 2;
    document.getElementById('htmlWrap').style.marginLeft = left + 'px';
}
