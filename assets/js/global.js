$( document ).ready(function() {

  $('textarea').autogrow({onInitialize: true});


  //Cloner for infinite input lists
  $(".circle--clone--list").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    var list = $(this).parents("ul");
    var last = list.children("li").last();
    var lastId = parseInt(last.children(":first-child").attr("id").match(/\d+/)[0]);
    list.append(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
    copy.children().each(function() {
      if ($(this).attr('id')) {
        $(this).attr('id', $(this).attr('id').replace(/\d+/g, lastId + 1));
        $(this).attr('name', $(this).attr('name').replace(/\d+/g, lastId + 1));
      }
    });
    $("input#id_form-TOTAL_FORMS").val(parseInt($("input#id_form-TOTAL_FORMS").val())+1);
  });

  $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    if (parent.children("[id$='-id']").val()) { // id attribute ends in '-id'
      parent.children('input.hidden-delete').prop('checked', true);
      parent.hide();
    } else {
      parent.remove();
      $("input#id_form-TOTAL_FORMS").val(parseInt($("input#id_form-TOTAL_FORMS").val())-1);
    };
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });




});