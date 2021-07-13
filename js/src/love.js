// //平台、设备和操作系统 
// var system = { 
//     win: false, 
//     mac: false, 
//     xll: false, 
//     ipad:false 
// }; 
// //检测平台 
// var p = navigator.platform; 
// system.win = p.indexOf("Win") == 0; 
// system.mac = p.indexOf("Mac") == 0; 
// system.x11 = (p == "X11") || (p.indexOf("Linux") == 0); 
// system.ipad = (navigator.userAgent.match(/iPad/i) != null)?true:false; 
// //跳转语句，如果是手机访问就自动跳转到wap.baidu.com页面 
// if (system.win || system.mac || system.xll||system.ipad) {

//     !function(e,t,a){function n(){c(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),o(),r()}function r(){for(var e=0;e<d.length;e++)d[e].alpha<=0?(t.body.removeChild(d[e].el),d.splice(e,1)):(d[e].y--,d[e].scale+=.004,d[e].alpha-=.013,d[e].el.style.cssText="left:"+d[e].x+"px;top:"+d[e].y+"px;opacity:"+d[e].alpha+";transform:scale("+d[e].scale+","+d[e].scale+") rotate(45deg);background:"+d[e].color+";z-index:99999");requestAnimationFrame(r)}function o(){var t="function"==typeof e.onclick&&e.onclick;e.onclick=function(e){t&&t(),i(e)}}function i(e){var a=t.createElement("div");a.className="heart",d.push({el:a,x:e.clientX-5,y:e.clientY-5,scale:1,alpha:1,color:s()}),t.body.appendChild(a)}function c(e){var a=t.createElement("style");a.type="text/css";try{a.appendChild(t.createTextNode(e))}catch(t){a.styleSheet.cssText=e}t.getElementsByTagName("head")[0].appendChild(a)}function s(){return"rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"}var d=[];e.requestAnimationFrame=function(){return e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.oRequestAnimationFrame||e.msRequestAnimationFrame||function(e){setTimeout(e,1e3/60)}}(),n()}(window,document);
    
// } 

!function(e,t,a){function n(){c(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),o(),r()}function r(){for(var e=0;e<d.length;e++)d[e].alpha<=0?(t.body.removeChild(d[e].el),d.splice(e,1)):(d[e].y--,d[e].scale+=.004,d[e].alpha-=.013,d[e].el.style.cssText="left:"+d[e].x+"px;top:"+(d[e].y-5)+"px;opacity:"+d[e].alpha+";transform:scale("+d[e].scale+","+d[e].scale+") rotate(45deg);background:"+d[e].color+";z-index:99999");requestAnimationFrame(r)}function o(){var t="function"==typeof e.onclick&&e.onclick;e.onclick=function(e){t&&t(),i(e)}}function i(e){var a=t.createElement("div");a.className="heart",d.push({el:a,x:e.clientX-5,y:e.clientY-5,scale:1,alpha:1,color:s()}),t.body.appendChild(a)}function c(e){var a=t.createElement("style");a.type="text/css";try{a.appendChild(t.createTextNode(e))}catch(t){a.styleSheet.cssText=e}t.getElementsByTagName("head")[0].appendChild(a)}function s(){return"rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"}var d=[];e.requestAnimationFrame=function(){return e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.oRequestAnimationFrame||e.msRequestAnimationFrame||function(e){setTimeout(e,1e3/60)}}(),n()}(window,document);

// !function(e,t,a)
// {
//     function n()
//     {
//         c("
//             .heart
//             {
//                 width: 10px;
//                 height: 10px;
//                 position: fixed;
//                 background: #f00;
//                 transform: rotate(45deg);
//                 -webkit-transform: rotate(45deg);
//                 -moz-transform: rotate(45deg);
//             }
//             .heart:after,.heart:before
//             {
//                 content: '';
//                 width: inherit;
//                 height: inherit;
//                 background: inherit;
//                 border-radius: 50%;
//                 -webkit-border-radius: 50%;
//                 -moz-border-radius: 50%;
//                 position: fixed;
//             }
//             .heart:after
//             {
//                 top: -5px;
//             }
//             .heart:before
//             {
//                 left: -5px;
//             }
//         "), 
        
//         o(), 
//         r()

//     }
    
//     function r()
//     {
//         for(var e=0;e<d.length;e++)
//             d[e].alpha<=0 
//             ? 
//             (t.body.removeChild(d[e].el),d.splice(e,1))
//             : 
//             (d[e].y--,d[e].scale+=.004,d[e].alpha-=.013,d[e].el.style.cssText="left:"+d[e].x+"px;top:"+d[e].y+"px;opacity:"+d[e].alpha+";transform:scale("+d[e].scale+","+d[e].scale+") rotate(45deg);background:"+d[e].color+";z-index:99999");
        
//         requestAnimationFrame(r)
//     }

//     function o()
//     {
//         var t="function"==typeof e.onclick&&e.onclick;
//         e.onclick=function(e){t&&t(),i(e)}
//     }

//     function i(e)
//     {
//         var a=t.createElement("div");
//         a.className="heart",d.push({el:a,x:e.clientX-5,y:e.clientY-5,scale:1,alpha:1,color:s()}),t.body.appendChild(a)
//     }
    
//     function c(e)
//     {
//         var a=t.createElement("style");
//         a.type="text/css";
//         try
//         {
//             a.appendChild(t.createTextNode(e))
//         }
//         catch(t)
//         {
//             a.styleSheet.cssText=e
//         }
//         t.getElementsByTagName("head")[0].appendChild(a)
//     }
    
//     function s()
//     {
//         return"rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"
//     }
    
//     var d=[];
//     e.requestAnimationFrame=function()
//     {
//         return e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.oRequestAnimationFrame||e.msRequestAnimationFrame||function(e){setTimeout(e,1e3/60)}
//     }(),n()

// }(window,document);