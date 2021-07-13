/* global NexT: true */

$(document).ready(function () {

  var html = $('html');
  var hasVelocity = $.isFunction(html.velocity);

  initScrollSpy();
  NexT.utils.needAffix() && initAffix();
  initTOCDimension();


  

  var $itemHasChild = $(".post-toc-content .nav-item:has(> .nav-child)");
  var $titleHasChild = $itemHasChild.children(".nav-link");
  // $itemHasChild.prepend("<i class='fa fa-caret-down'></i><i class='fa fa-caret-right'></i>");

  var $tocTitle = $(".sidebar-nav-toc");
  // $tocTitle.prepend("<i class='fa fa-caret-down'></i><i class='fa fa-caret-right'></i>");
  $tocTitle.prepend("<i class='fa fa-minus-square'></i><i class='fa fa-plus-square'></i>");

  var $iconToFold = $(".sidebar-nav-toc > .fa-minus-square");
  var $iconToExpand = $(".sidebar-nav-toc > .fa-plus-square");
  $iconToFold.addClass("hide");
  
  // var clickIcon = function(){
  //     $(".post-toc-content .nav-item > i").click(function(){
  //         $(this).siblings(".nav-child").slideToggle(100);
  //         $(this).toggleClass("hide");
  //         $(this).siblings("i").toggleClass("hide");
  //     })
  // }()

  var temp_timer = null;
  var temp_timer2 = null;

  var clickTitle = function(){
    $titleHasChild.dblclick(function(){
          clearTimeout(temp_timer);
          clearTimeout(temp_timer2);
          $(this).siblings(".nav-child").hide(100);
          // $(this).siblings("i").toggleClass("hide");
    })
    // After dblclick enent
    $titleHasChild.click(function(){
        clearTimeout(temp_timer);
        var that = this;
        temp_timer = setTimeout(function() {

            // 展开当前toc下的所有toc
            var $curentTocChild = $(that).siblings(".nav-child");
            if ($curentTocChild.is(":hidden")) {
                $curentTocChild.show(100);
                // $(that).siblings("i").toggleClass("hide");
            }
            // var $subToc = $titleHasChild.next(".nav-child");
            // alert(1);
            var $currentSubToc = $(that).siblings(".nav-child").find(".nav-link").next(".nav-child");
            // if ($(that).siblings(".nav-child").is(":hidden")) {
            if ($currentSubToc.is(":hidden")) {
                // $curentTocChild.show(100);
                $currentSubToc.show(100);
                // $(that).siblings("i").toggleClass("hide");
            }
        }, 250);
    })
  }()

  
  // TOC item animation navigate & prevent #item selector in adress bar.
  // $('.post-toc a').on('click', function (e) {
  // 上面两行的注释已无效, 下面这段代码用于实现锚点链接的平滑滚动, 且在浏览器URL处不显示锚点(即#之后的内容), 即URL地址不会发生变化
  // $('a[href^=#],area[href^=#]') 表示 href开头为#的元素
  // $('a[href*=#],area[href*=#]') 表示 href含有#的元素
  $('a[href^=#],area[href^=#]').on('click', function (e) {
    e.preventDefault();  // 取消事件的默认动作。注释这一行则可以在浏览器URL处显示锚点(即#之后的内容)
    
    clearTimeout(temp_timer2);
    var that = this;
    temp_timer2 = setTimeout(function() {
        var cur_href = that.getAttribute('href');
        if (window.history){ 
          // 如果支持History API 
          // 比如此时window.location为http://localhost:9009/2018/10/23/algo_newbie/#快速排序
          // 但因为 `e.preventDefault();`导致浏览器的地址还是http://localhost:9009/2018/10/23/algo_newbie/
          var state = {title:'',url:cur_href.split("#")[0]};
          history.pushState(state, '', "#" + cur_href.split("#")[1]);
          //现在浏览器的地址变为http://localhost:9009/2018/10/23/algo_newbie/#快速排序
        } 
        // 处理滚动动画
        var targetSelector = NexT.utils.escapeSelector(cur_href);
        var offset = $(targetSelector).offset().top - 170; // 此处减去 170 是为了防止页面滚动后  headroom 会挡住锚点跳转之后的标题
        hasVelocity ?
          html.velocity('stop').velocity('scroll', {
            offset: offset  + 'px',
            mobileHA: false
          }) :
          $('html, body').stop().animate({
            scrollTop: offset
          }, 500);
    }, 250);

  });


  var clickTocTitle = function(){
    // var $iconToExpand = $(".sidebar-nav-toc > .fa-caret-right");
    // var $iconToFold = $(".sidebar-nav-toc > .fa-caret-down");

    var $subToc = $titleHasChild.next(".nav-child");
    
    function showSubToc() {
      $(this).toggleClass("hide");

      $subToc.show(150, scrollToCenter);
      $iconToFold.removeClass("hide");
      $iconToExpand.addClass("hide");
    }

    if ($titleHasChild.length) {
        // $titleHasChild.click(showSubToc);

        // $tocTitle.addClass("clickable");
        $(".sidebar-nav-toc > i").click(function(){
            if ($iconToFold.is(":hidden")) {
                showSubToc();
                // $(this).toggleClass("hide");

                // $subToc.show(150, scrollToCenter);
                // $iconToExpand.removeClass("hide");
                // $iconToFold.addClass("hide");
            } else {
                $subToc.hide(100, scrollToCenter);
                $iconToFold.addClass("hide");
                $iconToExpand.removeClass("hide");
            }
        })
        // // TOC on mobile
        // if ($(".left-col").is(":hidden")) {
        //     $("#container .toc-article .toc").css("padding-left", "1.4em");
        //     $("#container .toc-article .toc-title").css("display", "initial");
        // }
    }
  }()



  function scrollToCenter() {
    var tocSelector = '.post-toc';
    var $tocElement = $(tocSelector);
    // var activeCurrentSelector = '.active-current';
    var $currentActiveElement = $(tocSelector + ' .active').last();
    // removeCurrentActiveClass();
    // $currentActiveElement.addClass('active-current');
    // Scrolling to center active TOC element if TOC content is taller then viewport.
    if ($currentActiveElement.offset() == undefined) {
      return;
    }
    $tocElement.scrollTop($currentActiveElement.offset().top - $tocElement.offset().top + $tocElement.scrollTop() - ($tocElement.height() / 2));
  }

  function initScrollSpy () {
    var tocSelector = '.post-toc';
    var $tocElement = $(tocSelector);
    var activeCurrentSelector = '.active-current';

    $tocElement
      .on('activate.bs.scrollspy', function () {
        var $currentActiveElement = $(tocSelector + ' .active').last();

        removeCurrentActiveClass();
        $currentActiveElement.addClass('active-current');
        // console.log("$currentActiveElement.offset().top")
        // console.log($currentActiveElement.offset().top)
        // console.log("$tocElement.offset().top")
        // console.log($tocElement.offset().top)
        // console.log("$tocElement.scrollTop()")
        // console.log($tocElement.scrollTop())
        // console.log("$tocElement.height() / 2")
        // console.log($tocElement.height() / 2)

        // console.log($currentActiveElement.offset().top - $tocElement.offset().top + $tocElement.scrollTop() - ($tocElement.height() / 2));
        // Scrolling to center active TOC element if TOC content is taller then viewport.
        $tocElement.scrollTop($currentActiveElement.offset().top - $tocElement.offset().top + $tocElement.scrollTop() - ($tocElement.height() / 2));


        // var $itemHasChild = $(".post-toc-content .nav-item:has(> .nav-child)");
        var that = $(tocSelector + ' .active').first().children(".nav-link");
        // 展开当前toc下的所有toc
        var $curentTocChild = $(that).siblings(".nav-child");
        if ($curentTocChild.is(":hidden")) {
            $curentTocChild.show(100);
            // $(that).siblings("i").toggleClass("hide");
        }
        // var $subToc = $titleHasChild.next(".nav-child");
        // alert(1);
        var $currentSubToc = $(that).siblings(".nav-child").find(".nav-link").next(".nav-child");
        // if ($(that).siblings(".nav-child").is(":hidden")) {
        if ($currentSubToc.is(":hidden")) {
            // $curentTocChild.show(100);
            $currentSubToc.show(100);
            // $(that).siblings("i").toggleClass("hide");
        }

      })
      // .on('clear.bs.scrollspy', removeCurrentActiveClass);
      .on('clear.bs.scrollspy', function() {
        // $(tocSelector + ' .active').first().children(".nav-link").siblings(".nav-child").hide(100);
        removeCurrentActiveClass();
      });

    $('body').scrollspy({ target: tocSelector });

    function removeCurrentActiveClass () {
      $(tocSelector + ' ' + activeCurrentSelector)
        .removeClass(activeCurrentSelector.substring(1));
    }
  }

  // Sidebar float
  function initAffix () {
    var headerHeight = $('.header-inner').height();
    var footerOffset = parseInt($('.main').css('padding-bottom'), 10);

    /*jshint camelcase: false */
    var sidebarTop = (CONFIG.sidebar.offset_float === 0) ?
      headerHeight + CONFIG.sidebar.offset :
      headerHeight;
    /*jshint camelcase: true */

    $('.sidebar-inner').affix({
      offset: {
        top: sidebarTop,
        bottom: footerOffset
      }
    });

    $(document)
      .on('affixed.bs.affix', function () {
        updateTOCHeight(document.body.clientHeight - 200);  // 为了防止toc sidebar底部有一些目录看不见
      });
  }

  function initTOCDimension () {
    var updateTOCHeightTimer;

    $(window).on('resize', function () {
      updateTOCHeightTimer && clearTimeout(updateTOCHeightTimer);

      updateTOCHeightTimer = setTimeout(function () {
        var tocWrapperHeight = document.body.clientHeight - 200;

        updateTOCHeight(tocWrapperHeight);
      }, 0);
    });

    // Initialize TOC Height.
    updateTOCHeight(document.body.clientHeight - 200);

    // Initialize TOC Width.
    var scrollbarWidth = NexT.utils.getScrollbarWidth();
    // $('.post-toc').css('width', 'calc(100% + ' + scrollbarWidth + 'px)');
  }

  function updateTOCHeight (height) {
    height = height || 'auto';
    $('.post-toc').css('max-height', height);
  }

});

$(document).ready(function () {
  var html = $('html');
  var TAB_ANIMATE_DURATION = 200;
  var hasVelocity = $.isFunction(html.velocity);

  $('.sidebar-nav li').on('click', function () {
    var item = $(this);
    var activeTabClassName = 'sidebar-nav-active';
    var activePanelClassName = 'sidebar-panel-active';
    if (item.hasClass(activeTabClassName)) {
      return;
    }

    var currentTarget = $('.' + activePanelClassName);
    var target = $('.' + item.data('target'));
    hasVelocity ?
      currentTarget
        .removeClass(activePanelClassName)
        .velocity('stop').velocity('transition.slideUpOut', TAB_ANIMATE_DURATION, function () {
          target
            .velocity('stop')
            .velocity('transition.slideDownIn', TAB_ANIMATE_DURATION)
            .addClass(activePanelClassName);
        }) :
      currentTarget.animate({ opacity: 0 }, TAB_ANIMATE_DURATION, function () {
        currentTarget.hide();
        target
          .stop()
          .css({'opacity': 0, 'display': 'block'})
          .animate({ opacity: 1 }, TAB_ANIMATE_DURATION, function () {
            currentTarget.removeClass(activePanelClassName);
            target.addClass(activePanelClassName);
          });
      });

    item.siblings().removeClass(activeTabClassName);
    item.addClass(activeTabClassName);
  });

  // Expand sidebar on post detail page by default, when post has a toc.
  var $tocContent = $('.post-toc-content');
  var isSidebarCouldDisplay = CONFIG.sidebar.display === 'post' ||
      CONFIG.sidebar.display === 'always';
  var hasTOC = $tocContent.length > 0 && $tocContent.html().trim().length > 0;
  if (isSidebarCouldDisplay && hasTOC) {
    CONFIG.motion ?
      (NexT.motion.middleWares.sidebar = function () {
          NexT.utils.displaySidebar();
      }) : NexT.utils.displaySidebar();
  }
});
