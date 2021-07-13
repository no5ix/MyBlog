$(document).ready(function () {

  $(":header").each(function(){
	  var curId = $(this).attr("id");
    if (!curId) {
      $(this).attr("id", encodeURI($(this).text()));
    } 
  });

  // $(".header-inner").animate({padding: "25px 0 20px"}, 1000);

  // $('#header').wobbleWindow({radius: 50, movementTop: false, offsetX: 50, debug: false});
  // $('blockquote').wobbleWindow({radius: 40, movementTop: false, movementBottom: false, lineColor: '', debug: false});
  // $('#footer').wobbleWindow({radius: 50, movementBottom: false, offsetX: 50, position: 'absolute', debug: false});
  // $('#reward').wobbleWindow({radius: 40, offsetX: 0, offsetY: 5, bodyColor: '#FAF2C7', lineColor: '', debug: false});

});
