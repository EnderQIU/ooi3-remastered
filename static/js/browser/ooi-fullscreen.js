function openFullscreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullScreen();
    }
}

function exitFullScreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
        document.msExiFullscreen();
    } else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen();

    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    }
}

document.getElementById("fullScreenButton").addEventListener('click', function () {
    let ele = document.getElementById("htmlWrap");
    document.fullscreenEnabled ? exitFullScreen(ele) : openFullscreen(ele);
}, false);