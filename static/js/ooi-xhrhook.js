var term = new Terminal();
term.open(document.getElementById('debugTerminal'));

hookAjax({
    //拦截回调
    onreadystatechange: function (xhr) {
        term.write(xhr.toString());
    },
    onload: function (xhr) {
        term.write(xhr.toString());
    },
    //拦截方法
    open: function (arg, xhr) {
        term.write(xhr.toString());
        console.log("open called: method:%s,url:%s,async:%s", arg[0], arg[1], arg[2])
    }
});