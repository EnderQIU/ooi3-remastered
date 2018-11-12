function sendXhrResponseToSwift(resp) {
    try {
        if (resp.request.responseURL.indexOf("/kcsapi/api_req_mission/start") !== -1) {
            let data = resp.data;
            data = JSON.parse(data.replace('svdata=', ''));
            let complete_time = new Date(data.api_data.api_complatetime);
            let interval = Math.floor((complete_time - new Date()) / 1000) - 60;  // notify advance one minute
            SetIntervalNotification(interval, "Expedition accomplished!", "遠征から戻って来ました");
        }
    } catch (e) {
        console.log('Exception occurred when handling XHR response.')
    }
}

function SetIntervalNotification(interval, title, body) {
    try {
        webkit.messageHandlers.timeIntervalNotificationTriggerHandler.postMessage({
            interval: interval,
            title: title,
            body: body
        })
    } catch (e) {
        console.log('The native context not exist.')
    }
}