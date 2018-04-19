var fixed_head = $(".navbar-expand-sm");
$(window).scroll(function(){
	if ($(this).scrollTop() > 60) {
		fixed_head.css("box-shadow","0 2px 3px rgba(0,0,0,.4)");
		$('#mainCarousel').css("margin-top", "60px");
		fixed_head.addClass("fixed-top");
	} else {
		fixed_head.css("box-shadow","none");
		$('#mainCarousel').css("margin-top", "0px");
		fixed_head.removeClass("fixed-top");
	}
})