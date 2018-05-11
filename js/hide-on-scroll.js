// Hide Header on on scroll down
var didScroll;
var lastScrollTop = 0;
var delta = 5;
var navbarHeight = $('header').outerHeight();

$(window).scroll(function(event){
    didScroll = true;
});

setInterval(function() {
    if (didScroll) {
        hasScrolled();
        didScroll = false;
    }
}, 250);

function hasScrolled() {
    var st = $(this).scrollTop();
    
    // Make sure they scroll more than delta
    if(Math.abs(lastScrollTop - st) <= delta)
        return;
    
    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (st > lastScrollTop && st > navbarHeight){
        // Scroll Down
        $('header').fadeOut('slow');
    } else {
        // Scroll Up
        if(st + $(window).height() < $(document).height()) {
            $('header').fadeIn('slow');
        }
    }
    
    lastScrollTop = st;
}

// Enable Emojify and Syntax highlighting.
App = {};
App.main = function(){
    emojify.setConfig({mode : 'data-uri'});
    emojify.run();

    if( 1 === $('nav').children().length )
    {
        $('nav').remove();
        $('.menu-link').remove();
        $('.push').css({
            "width": "100%",
            "margin-left":"0"
        });
        $('.push header').css({
            "width": "100%",
        });
    }

    var current = window.location.href;
    $('nav a[href="'+current+'"]').closest('li').addClass('current');


    // Syntax highlighting
    hljs.initHighlightingOnLoad();
}

App.main();
