var page=0;
var pages;

function change_page(){
    pages[page].style.display="None";

    if (page==0){
        page=pages.length;
    }
    page --;


    var test_id = 1;
    self['update_page' + test_id]();

    //update_page1();
    pages[page].style.display="block";

    setTimeout("change_page()",5000);
}

function update_page1() {

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("page1_text").innerHTML = xhttp.responseText;
    }
  };
  xhttp.open("GET", "/api/v1/busstop", true);
  xhttp.send();
}


function onload(){
    pages=document.getElementsByClassName("page");
    for (var i = 0; i<pages.length; i++)
    {
      pages[i].style.display="None";
    }


    change_page();
}