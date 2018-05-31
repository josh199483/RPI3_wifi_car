// 所有 js 函數的起始點，等同於 $(document).ready(function(){})
$(function () {
    $("#output1").text('start~~~~');
    $("#control").delegate('a', 'click', function() {
        $.get('/' + $(this).attr('id'), callback);
    });
});


var callback = function (value, status) {
    if (status == 'success') {
        $("#output1").text(value);
    }else{
        $("#output1").text('Error!');
    }
};