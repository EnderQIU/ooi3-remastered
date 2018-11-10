function setupSwiftJSBridge(callback) {
    if (window.SwiftJSBridge) {
        return callback(SwiftJSBridge);
    }
    if (window.SwiftJSBridgeReadyCallbacks) {
        return window.SwiftJSBridgeReadyCallbacks.push(callback);
    }
    window.SwiftJSBridgeReadyCallbacks = [callback];
    SwiftJSBridgeInject()
}

function isWebKit() {
    return window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.SwiftJSBridgeInject;
}

function SwiftJSBridgeInject() {
    console.log("SwiftJSBridgeInject");
    if (isWebKit()) {
        window.webkit.messageHandlers.SwiftJSBridgeInject.postMessage("SwiftJSBridgeInject")
    } else {
        var src = "https://SwiftJSBridgeInject/" + Math.random()
        var req = new XMLHttpRequest;
        req.open("GET", src);
        req.send()
    }
}

setupSwiftJSBridge(function (bridge) {
    function log(message, data) {
        console.log(message + data)
    }

    bridge.addJSBridge('sendMessageToJS', function (data, responseCallback) {
        log('Native called sendMessageToJS with', data)
        var responseData = {message: 'Hi, I am JS'}
        log('JS responding with', responseData)
        // register axios listener
        let trigger = $("#ooi-trigger");
        trigger.on('onXhrReceive', function (event, response) {
            SwiftJSBridge.callNativeBridge("webViewFinishedLoading", {"data": response}, function (data) {
                console.log("callback");
                console.log(data)
            })
        });
        // resp callback
        responseCallback(responseData)
    })
})
