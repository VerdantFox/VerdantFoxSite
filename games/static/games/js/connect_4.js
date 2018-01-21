console.log('testing, testing, 1,2,3...');

$('h2').css('color', 'green');

var grid = $('.grid').children().children();

var player1Turn = false;


$('.grid').click(function () {
    if (player1Turn){
        player1Turn = false;
    }else{
        player1Turn = true;
    }
});

function turnAnnounce() {
    if (player1Turn) {
        $('h3').text("Player 1's turn!")
    }else{
        $('h3').text("Player 2's turn!")
    }
}



$('.column0').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column0').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column0').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column0').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column0').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column0').click(function () {
    turnAnnounce();
    if ($('.column0').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column0').eq(5).addClass("blue");
        } else {
            $('.column0').eq(5).addClass("red");
        }
    }
});

$('.column1').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column1').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column1').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column1').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column1').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column1').click(function () {
    turnAnnounce();
    if ($('.column1').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column1').eq(5).addClass("blue");
        } else {
            $('.column1').eq(5).addClass("red");
        }
    }
});

$('.column2').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column2').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column2').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column2').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column2').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column2').click(function () {
    turnAnnounce();
    if ($('.column2').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column2').eq(5).addClass("blue");
        } else {
            $('.column2').eq(5).addClass("red");
        }
    }
});

$('.column3').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column3').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column3').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column3').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column3').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column3').click(function () {
    turnAnnounce();
    if ($('.column3').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column3').eq(5).addClass("blue");
        } else {
            $('.column3').eq(5).addClass("red");
        }
    }
});

$('.column4').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column4').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column4').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column4').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column4').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column4').click(function () {
    turnAnnounce();
    if ($('.column4').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column4').eq(5).addClass("blue");
        } else {
            $('.column4').eq(5).addClass("red");
        }
    }
});

$('.column5').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column5').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column5').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column5').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column5').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column5').click(function () {
    turnAnnounce();
    if ($('.column5').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column5').eq(5).addClass("blue");
        } else {
            $('.column5').eq(5).addClass("red");
        }
    }
});

$('.column6').click(function () {
    turnAnnounce();
    for (var i=0; i<6; i++) {
        if (($('.column6').eq(i-1).css('background-color') === 'rgb(105, 105, 105)')
        && ($('.column6').eq(i).css('background-color') !== 'rgb(105, 105, 105)')){
            if (player1Turn) {
                $('.column6').eq(i - 1).addClass("blue");
            }else if (!player1Turn) {
                $('.column6').eq(i - 1).addClass("red");
            }
        }
    }
});

$('.column6').click(function () {
    turnAnnounce();
    if ($('.column6').eq(5).css('background-color') === 'rgb(105, 105, 105)') {
        if (player1Turn) {
            $('.column6').eq(5).addClass("blue");
        } else {
            $('.column6').eq(5).addClass("red");
        }
    }
});

