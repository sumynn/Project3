$(function(){

    /* ---------- 기본 사용 ---------- */

    $('.basic_slider').bxSlider({
        mode: 'horizontal',
        speed: 5000
    });


    /* ---------- 좌우 컨트롤 ---------- */

    $('.control_slider').bxSlider({
    //controls:false
    nextText : '<i class="fas fa-chevron-right"></i>',
    prevText : '<i class="fas fa-chevron-left"></i>',
    pager:false
    });

    $('.img_control_slider').bxSlider({
    //controls:false,
    pager:false,
    prevSelector:'.img_controls .imgcontrols .prev',
    nextSelector:'.img_controls .imgcontrols .next'
    });

    /* ---------- 멀티플 슬라이드 ---------- */
    $('.multiple_slider').bxSlider({
    minSlides:1,
    maxSlides:4,
    moveSlides : 1,
    slideWidth:200,
    slideMargin:30,
    pager:false
    });
    /* --------- 현재 슬라이드 구분하기 ------------- */

    
	$('.active_slider').bxSlider({
		onSliderLoad:function(currentIndex){
			$('.active_slider li').eq(currentIndex + 1).addClass('active');
		},
		onSlideAfter:function($slideElement){
			$slideElement.addClass('active').siblings().removeClass('active');
		}
	});
});

