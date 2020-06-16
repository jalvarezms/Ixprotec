$(document).ready(function() {

    $('.slick_image').slick({
        arrows: false,
        prevArrow: false,
        nextArrow: false,
        lazyLoad: 'ondemand',
        slidesToShow: 3,
        slidesToScroll: 1

    });
    $(".slick-arrow").addClass(" bg-primary")
});