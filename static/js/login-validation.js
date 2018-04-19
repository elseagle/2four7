$(document).ready(function(){
	$(".navbar-expand-sm").css("box-shadow","0 2px 3px rgba(0,0,0,.4)");
	$('.row').css("margin-top", "90px");
});
$('.toggleVisibility').click(function(){
	$('.form-signin').toggleClass('no-display');
	$('.form-signup').toggleClass('no-display');
});