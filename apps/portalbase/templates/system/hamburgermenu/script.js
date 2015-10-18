var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

function injectIframe() {
    $('.flatTheme > .container').html('')
    .addClass('height-full')
    .html("<iframe id='external-iframe' class='border-none' src='" + getUrlParameter('url') + "'></iframe>")
    .removeClass('container');
    $('.flatTheme').addClass('padding-top-none');
    $('.navbar-inverse').remove();
    $('.navmenu-fixed-left.offcanvas').remove();
    var div = $("<div class='navmenu navmenu-default navmenu-fixed-left offcanvas'><a class=''></a></div>");
    div.find('a').html($('#portalsHamburgerStructure').html());
    $('.height-full').prepend(div);
};

function injectHamburgerButton(theme, external) {
    function applyHamburgerButton() {
      $('.slider-container').append("<button id='PortalsHamburgerMenu' class='c-hamburger c-hamburger--htla left side-nav-btn position-fixed " + theme + "' title='Portals'><span></span></button>");
      if(external === true){
        $('#PortalsHamburgerMenu').addClass('margin-top-small');
        $('#external-iframe').one("load", function() {
          if($("#external-iframe").contents().find(".logo").length > 0){
            if( $("#external-iframe").contents().find(".logo").hasClass("margin-left-large") === false){
                $("#external-iframe").contents().find(".logo").addClass('margin-left-large');
            }
          }
        });
      }
    }
    if($('#PortalsHamburgerMenu').length > 0){
      $('#PortalsHamburgerMenu').remove();
      applyHamburgerButton();
    }else{
      applyHamburgerButton();
    }
};

$(function () {
    function getSpaceinfo(){
      var SpacesNavBtnTheme = "light";
      var isSpaceExternal = false;
      $('.navmenu-default').find('a.space').each(function() {
        if(window.location.href.toLowerCase().indexOf($(this)[0].href.toLowerCase()) > -1){
          SpacesNavBtnTheme = $(this).data().theme;
          isSpaceExternal = $(this).data().external;
          $(this).siblings('.accordion-toggle').click();
          return false;
        }
      });
      return {"theme":SpacesNavBtnTheme, "external":isSpaceExternal};
    };

    $(document).on('click', '.accordion-toggle', function(e) {
      $('.panel-collapse').removeClass('in');
      $('.accordion-toggle').removeClass('collapsed');
      $(this).addClass('collapsed');
    });

    if($('.navmenu.navmenu-default').length === 0){
      var div = $("<div class='navmenu navmenu-default navmenu-fixed-left offcanvas'></div>");
      div.html($('#portalsHamburgerStructure').html());
      $('.navbar-inner.navbar-form').prepend(div);
      var spaceinfo = getSpaceinfo();
      injectHamburgerButton(spaceinfo["theme"], spaceinfo["external"]);
    }

    var currentPage = '';
    if(window.location.pathname.indexOf('external') > -1){
        currentPage = 'external';
    }

    if(currentPage == 'external'){
        injectIframe();
        var spaceinfo = getSpaceinfo();
        injectHamburgerButton(spaceinfo["theme"], spaceinfo["external"]);
    }

    $( ".openIframe" ).click(function(event) {
        if( $(this).data().external === true ){
            event.preventDefault();
            window.location.replace("/home/external?url=" + this["href"]);
            injectIframe();
            injectHamburgerButton($(this).data().theme, $(this).data().external);
        }
    });

    $('.side-nav-btn').click(function(){
        $('.portals-navigation').toggleClass('visible');
        $('.slider-container').toggleClass('visible');
        $('.portals-navigation').toggleClass('show-on-large');
    });

    function checkChangedBrowserSize() {

        function showMenu(){
          $('.portals-navigation').addClass('visible').addClass('show-on-large');
          $('.slider-container').addClass('visible');
        }
        function hideMenu() {
          $('.portals-navigation').removeClass('visible').removeClass('show-on-large');
          $('.slider-container').removeClass('visible');
        }

        if(window.location.pathname.indexOf('wiki_gcb') > -1){
          if($( window ).width() + 21 < 1710){
              hideMenu();
          }else{
              showMenu();
          }
        }else{
          if($( window ).width() + 21 < 1560){
              hideMenu();
          }else{
              showMenu();
          }
        }
        
    }

    checkChangedBrowserSize();
    $('.container').click(function() {
        checkChangedBrowserSize();
    });

    window.onresize = function (){
        checkChangedBrowserSize();
    };

});