function sendXhrResponseToSwift(resp){
    if (resp.request.responseURL.indexOf("/kcsapi/api_req_mission/start") !== -1){
        let data = resp.data;
        data =  JSON.parse(data.replaceAll('svdata=', ''));
        let complete_time = new Date(data.api_data.api_complatetime);
        let interval = Math.floor((complete_time - new Date()) / 1000) - 60;  // notify advance one minute
        SetIntervalNotification(interval, "Expedition accomplished!", "遠征から戻って来ました");
    }

}

function SetIntervalNotification(interval, title, body) {
    try{
        webkit.messageHandlers.timeIntervalNotificationTriggerHandler.postMessage({
            interval: interval,
            title: title,
            body: body
        })
    }catch (e) {
        console.log('The native context not exist.')
    }
}