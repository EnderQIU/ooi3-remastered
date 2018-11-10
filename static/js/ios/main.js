window.onload = function () {
    setScale();
};

$("#ooi-trigger").on("ooiXhrEventEmitterReady", function () {
    SwiftJSBridge.callNativeBridge("webViewFinishedLoading", {"data": "v1"}, function (data) {
        console.log("callback");
        console.log(data)
    })
});