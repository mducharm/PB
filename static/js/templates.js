$.fn.load_=$.fn.load;
$.fn.load=function(){
    return $.fn.load_.apply(this,arguments).hide().fadeIn('slow');
}

$(document).ready(function() {
    $("#rec-ing-link").click(function() {
        $("#content-box").load("/recipes-ingredients/", {"data":"test"});
    });  
});