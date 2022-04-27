$(function () {
    $(".scrollcard").slick({
      centerMode: true,
      centerPadding: "40px",
      slidesToShow: 3,
      responsive: [
        {
          breakpoint: 768,
          settings: {
            arrows: false,
            centerMode: true,
            centerPadding: "30px",
            slidesToShow: 4,
          },
        },
        {
          breakpoint: 480,
          settings: {
            arrows: false,
            centerMode: true,
            centerPadding: "10px",
            slidesToShow: 1,
          },
        },
      ],
    });
  });