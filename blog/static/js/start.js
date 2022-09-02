//Different plugins are initiated here

(function($){
	$(document).ready(function(){

        //Initializing WOW aninations
          new WOW().init();

		//Scroll Spy
		//-----------------------------------------------
		if($(".scrollspy").length>0) {
			$("body").addClass("scroll-spy");
			$('body').scrollspy({
				target: '.scrollspy',
				offset: 152
			});
		}

		//Smooth Scroll - Done - As you click at links, the gap
		//-----------------------------------------------
		if ($(".smooth-scroll").length>0) {
			$('.smooth-scroll a[href*=#]:not([href=#]), a[href*=#]:not([href=#]).smooth-scroll').click(function() {
				if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
					var target = $(this.hash);
					target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
					if (target.length) {
						$('html,body').animate({
							scrollTop: target.offset().top-151
						}, 1000);
						return false;
					}
				}
			});
		}

		// Animations - Done - Content appears in MS (modernizr plugin)


	//Small carosel code set here
    jQuery('.carousel[data-type="multi"] .item').each(function(){
		var next = jQuery(this).next();
		if (!next.length) {
			next = jQuery(this).siblings(':first');
		}
		next.children(':first-child').clone().appendTo(jQuery(this));

		for (var i=0;i<2;i++) {
			next=next.next();
			if (!next.length) {
				next = jQuery(this).siblings(':first');
			}
			next.children(':first-child').clone().appendTo($(this));
		}
	});
    //Ending of small carosel

        //Code to send email
        //   $("form").submit(function(event){
        //     strname=$("#yname").val();
        //     stremail=$("#email2").val();
		// 	strmessage=$("#message2").val();

		// 	$("#messageconfirm").html('result');

        //     // $.post("email/send-email.php", {name:strname, email:stremail, message:strmessage },function(result){
        //     //     $("#messageconfirm").html(result);
        //     // });
        //      event.preventDefault();

        //   });


	});
})(this.jQuery);