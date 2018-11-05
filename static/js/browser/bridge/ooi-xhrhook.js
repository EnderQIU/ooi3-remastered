/* ooi-xhrhook.js
 *
 * Principle:
 * main.js?version=4.2.1.0:formatted @line: 334
 * The KCS uses the axios js which is based on XMLHttpRequest but it won't
 * work if you just hook the xhr out of the game iframe. That because the request
 * was created from the index.php iframe which is inside the top page. So you
 * must hook xhr from "window.iframs[0]" instead of the root page.
 *
 * Hook Example:
 *
 * Parameter 'config' in request:
 * {
 *     ...
 *     data: "",
 *     headers: {
 *         Accept: "",
 *         Content-Type: "",
 *         ...
 *     },
 *     ...
 *     method: "post"/"get",
 *     url: "",
 *     ...
 * }
 *
 * Parameter 'response' in response.use:
 * {
 *     ...
 *     data: "",
 *     status: "",
 *     headers: "",
 *     ...
 * }
 *
 * Usage:
 *
 * $("#ooi-trigger").on("ooiXhrEventEmitterReady", function () {
 *     let trigger = $("#ooi-trigger");
 *     trigger.on('beforeXhrSend', function(event, config){console.log(config)});
 *     trigger.on('onXhrReceive', function(event, response){console.log(response)});
 * });
*/

document.getElementById('htmlWrap').onload = function () {

    // Add a request interceptor
    window.frames[0].axios.interceptors.request.use(function (config) {
        // Do something before request is sent
        $("#ooi-trigger").trigger('beforeSend', config);
        return config;
    }, function (error) {
        // Do something with request error
        $("#ooi-trigger").trigger('beforeRequestReject', error);
        return Promise.reject(error);
    });

    // Add a response interceptor
    window.frames[0].axios.interceptors.response.use(function (response) {
        // Do something with response data
        $("#ooi-trigger").trigger('onReceive', response);
        return response;
    }, function (error) {
        // Do something with response error
        $("#ooi-trigger").trigger('beforeResponseReject', error);
        return Promise.reject(error);
    });

    // OOI XHR event emitter ready state trigger,
    // all event above should be triggered after the emitter is ready.
    $("#ooi-trigger").trigger('ooiXhrEventEmitterReady');
};
