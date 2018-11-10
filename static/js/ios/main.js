window.onload = function () {
    setScale();
};

document.getElementById('htmlWrap').onload = function () {
    window.frames[0].axios.interceptors.response.use(function (response) {
        sendXhrResponseToSwift(response);
        return response;
    }, function (error) {
        return Promise.reject(error);
    });
};
