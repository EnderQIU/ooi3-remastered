function resp2Json(resp) {
    return JSON.parse(resp.data.replace('svdata=', ''));
}

function getCompleteIntervalFromData(data) {
    return Math.floor((new Date(data.api_data.api_complatetime) - new Date()) / 1000);
}

function getCompleteIntervalFromAPIData(api_data) {
    return Math.floor((new Date(api_data.api_complete_time) - new Date()) / 1000);
}

function sendXhrResponseToSwift(resp) {
    try {
        if (resp.request.responseURL.indexOf("/kcsapi/api_req_mission/start") !== -1) {
            // Expedition accomplishment notification
            let data = resp2Json(resp);
            let interval = getCompleteIntervalFromData(data, true);
            SetIntervalNotification("expedition" + data.api_data.api_complatetime_str,
                interval,
                "Expedition accomplished!",
                "舰队、作戦终了です。お疲れ様でした。",
                "sound/ooyodo/expedition_complete.caf");
        }
        else if (resp.request.responseURL.indexOf("/kcsapi/api_get_member/ndock") !== -1) {
            // Docking accomplishment notification
            let data = resp2Json(resp);
            for (let api_data of data.api_data) {
                if (api_data.api_state > 0) {
                    // -1: locked; 0: empty; 1: in use
                    let interval = getCompleteIntervalFromAPIData(api_data, true);
                    SetIntervalNotification("docking" + api_data.api_complete_time_str,
                        interval,
                        "Docking completed!",
                        "入渠中の舰の修理が完了しました。",
                        "sound/ooyodo/docking_complete.caf");
                }
            }
        }
        else if (resp.request.responseURL.indexOf("/kcsapi/api_get_member/kdock") !== -1) {
            // Create new ship notification
            let data = resp2Json(resp);
            for (let api_data of data.api_data) {
                if (api_data.api_state === 2) {
                    // -1: locked; 0: empty; 1: complete; 2: in use
                    let interval = getCompleteIntervalFromAPIData(api_data, true);
                    SetIntervalNotification("createship" + api_data.api_complete_time_str,
                        interval,
                        "New friend have arrived!",
                        "新建造舰が完成致しました。",
                        "sound/ooyodo/ship_complete.caf");
                }
            }
        }
    } catch (e) {
        console.log('Exception occurred when handling XHR response.')
    }
}

function SetIntervalNotification(identifier, interval, title, body, soundName) {
    try {
        webkit.messageHandlers.timeIntervalNotificationTriggerHandler.postMessage({
            identifier: identifier,
            interval: interval,
            title: title,
            body: body,
            soundName: soundName
        })
    } catch (e) {
        console.log('The native context not exist.')
    }
}