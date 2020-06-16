$(document).ready(function() {
    $('.slick_image').slick({
        lazyLoad: 'ondemand',
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2000,
    });
    $(".slick-arrow").addClass(" bg-primary")
});