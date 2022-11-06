window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 700|| document.documentElement.scrollTop > 700) {
    document.getElementById("navbar").style.top = "0px";
  } else {
    document.getElementById("navbar").style.top = "-70px";
  }
}