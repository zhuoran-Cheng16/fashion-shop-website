// $('.like, .dislike').on('click', function() {
//     event.preventDefault();
//     $('.active').removeClass('active');
//     $(this).addClass('active');
// });

// https://www.w3schools.com/howto/howto_js_collapse_sidebar.asp
/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidebar").style.width = "15%";
    document.getElementById("main").style.marginLeft = "15%";
  }
  
  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
  }

//https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_toggle_hide_show
  function hide_review() {
    var x = document.getElementById("review-section");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

// Update the current slider value (each time you drag the slider handle)
function slider_set_value() {
  document.getElementById("slider-right").innerHTML = document.getElementById("price-slider").value;
}
