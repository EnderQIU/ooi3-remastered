function sendXhrResponseToSwift(resp){
    try{
        webkit.messageHandlers.XhrResponseHandler.postMessage({
            data: resp.data,
            statusText: resp.statusText,
            url: resp.request.responseURL
        })
    }catch (e) {
        console.log('The native context not exist.')
    }
}