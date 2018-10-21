$.fn.load_=$.fn.load;
$.fn.load=function(){
    return $.fn.load_.apply(this,arguments).hide().slideDown();
}

$(document).ready(function() {
    $("#rec-ing-link").click(function() {
        $("#content-box").load("/recipes-ingredients/", {'data': 'pad thai'});
    });  
});

$('form.ajax').on('submit', function() {
    var that = $(this),
        url = that.attr('action'),
        method = that.attr('method'),
        data = {};
    that.find('[name]').each(function() {
        console.log(value);
    });
    return false;
});