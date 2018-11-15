function setScale() {
    let scale = 1.0;
    if (window.screen.width / window.screen.height < 1.67){
        // iPad
        scale = window.screen.height / 1200.0;
    }else{
        // iPhone
        scale = window.screen.width / 720.0;
    }
    let viewport = document.querySelector("meta[name=viewport]");
    viewport.setAttribute('content', 'width=device-width user-scalable=yes initial-scale=' + scale.toFixed(2));

    // center the iframe
    let left = (document.body.scrollWidth  - 1200) / 2;
    let top = (document.body.scrollHeight  - 720) / 2;
    document.getElementById('htmlWrap').style.marginLeft = left + 'px';
    document.getElementById('htmlWrap').style.marginTop = top + 'px';
}
