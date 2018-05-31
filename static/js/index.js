// 所有 js 函數的起始點，等同於 $(document).ready(function(){})
$(function () {
    $("#output").text('start~~~~');
});

var change_direction = function (command) {
    $.get('/' + command, callback);
};

var callback = function (value, status) {
    if (status == 'success') {
        $("#output").text(value);
    }else{
        $("#output").text('Error!');
    }
};