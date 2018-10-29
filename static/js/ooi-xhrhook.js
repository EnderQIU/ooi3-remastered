/* ooi-xhrhook.js
 *
 * Principle:
 * main.js?version=4.2.1.0:formatted @line: 334
 * The KCS uses the axios js which is based on XMLHttpRequest but it won't
 * work if you just hook the xhr in the outer page. That because the request
 * was created from the index.php iframe which inside the top page. So you
 * must hook xhr from the iframe instead of root page.
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
 * $.ooiXhrEventEmitter.on('beforeXhrSend', function(config){...});
 * $.ooiXhrEventEmitter.on('onXhrReceive', function(response){...});
*/

document.getElementById('htmlWrap').onload = function () {
    let term = new Terminal();
    term.open(document.getElementById('debugTerminal'));
    $.ooiXhrEventEmitter = $({});

    // Add a request interceptor
    window.frames[0].axios.interceptors.request.use(function (config) {
        // Do something before request is sent
        $.ooiXhrEventEmitter.trigger('beforeXhrSend', config);
        return config;
    }, function (error) {
        // Do something with request error
        return Promise.reject(error);
    });

    // Add a response interceptor
    window.frames[0].axios.interceptors.response.use(function (response) {
        // Do something with response data
        $.ooiXhrEventEmitter.trigger('onXhrReceive', response);
        return response;
    }, function (error) {
        // Do something with response error
        return Promise.reject(error);
    });
};