if (window.self !== window.top) {
    window.top.location.href = window.self.location.href;
}