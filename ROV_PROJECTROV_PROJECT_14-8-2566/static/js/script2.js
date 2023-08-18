// Dropdown
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

// upload img
  function fncSubmit() {
    var email = document.forms["form_upload"]["file_statistic"].value;
    var password = document.forms["form_upload"]["file_details"].value;

    if (email === "" || password === "") {
      Swal.fire({
        icon: 'warning',
        title: 'กรุณาเพิ่มรูปภาพ!',
        showConfirmButton: false,
        timer: 1500
      });
      return false;
    }
  }


function result_teamA() {
  var resulta = document.getElementById("resultsA");
  var resultb = document.getElementById("resultsB");
  // var win_a = document.getElementById("win_a");
  // var win_b = document.getElementById("win_b");

  resulta.addEventListener("change", function () {
    var selectedOption = resulta.value;
    if (selectedOption === "win") {
      resultb.value = "lose";
      // win_a.value = "Win";
      // win_b.value = "Lose";
    } else if (selectedOption === "lose") {
      resultb.value = "win";
      // win_b.value = "Win";
      // win_a.value = "Lose";
    } else if (selectedOption === "always") {
      resultb.value = "always";
      // win_a.value = "Always";
      // win_b.value = "Always";
    } else {
      resultb.value = "0";
      // win_a.value = "";
      // win_b.value = "";
    }
  });
}

function result_teamB() {
  var resulta = document.getElementById("resultsA");
  var resultb = document.getElementById("resultsB");
  // var win_a = document.getElementById("win_a");
  // var win_b = document.getElementById("win_b");

  resultb.addEventListener("change", function () {
    var selectedOption = resultb.value;
    if (selectedOption === "win") {
      resulta.value = "lose";
      // win_b.value = "Win";
      // win_a.value = "Lose";
    } else if (selectedOption === "lose") {
      resulta.value = "win";
      // win_a.value = "Win";
      // win_b.value = "Lose";
    } else if (selectedOption === "always") {
      resulta.value = "always";
      // win_a.value = "Always";
      // win_b.value = "Always";
    } else {
      resulta.value = "0";
      // win_a.value = "";
      // win_b.value = "";
    }

  });
}

// dropdrow-search
$(document).ready(function () {
  $('#select-box').select2();
});
$(document).ready(function () {
  $('#select-box2').select2();
});

// popup_img-------
function openModal() {
  document.getElementById("myModal2").style.display = "block";
}

function closeModal() {
  document.getElementById("myModal2").style.display = "none";
}

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides2");
  var dots = document.getElementsByClassName("demo2");
  var captionText = document.getElementById("caption2");
  if (n > slides.length) {
    slideIndex = 1
  }
  if (n < 1) {
    slideIndex = slides.length
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
  captionText.innerHTML = dots[slideIndex - 1].alt;
}


