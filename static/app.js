/**
 * @author: Aberdeen Morrow
 * Last Modified: 12-11-21
 * Macalester College
 * COMP 446 Internet Computing
 * with Joslenne Pena
 */

var acc = document.getElementsByClassName("accordion");
var i;

// Makes navbar responsive to window size
function myFunction() {
  var x = document.getElementById("top-nav");
  if (x.className === "nav-bar") {
    x.className += " responsive";
  } else {
    x.className = "nav-bar";
  }
}

// Controls opening and closing accordions (i.e. on user profile page)
for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
};

// Toggles saved icon appearance
// $("#saved-button").on({click: function(){  /* Toggle between adding and removing the "active" class,
//   to highlight the button that controls the panel */
//   $("#saved-button").toggleClass("saved");
//   if ($("#saved-button").hasClass("saved")) {
//     $("#saved-button").html('<i class="fa fa-bookmark saved-button" aria-hidden="true"></i>')
//   } else {
//     $("#saved-button").html('<i class="fa fa-bookmark-o saved-button" aria-hidden="true"></i>')
//   }
// }})

$(function() {
  $('#saved-button').on('click', function(e) {
    e.preventDefault()
    var id = $(this).attr("name")
    $("#saved-button").toggleClass("saved");
    if ($("#saved-button").hasClass("saved")) {
      $("#saved-button").html('<i class="fa fa-bookmark saved-button" aria-hidden="true"></i>');
      $.getJSON('/background_save/'+id,
          function(data) {
        //do nothing
      });
      return false;
    } else {
      $("#saved-button").html('<i class="fa fa-bookmark-o saved-button" aria-hidden="true"></i>');
      $.getJSON('/background_unsave/'+id,
          function(data) {
        //do nothing
      });
      return false;
  }})
});