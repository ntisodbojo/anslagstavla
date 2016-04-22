var page=0;
var pages;

function change_page(){
    pages[page].style.display="None";

    if (page==0){
        page=pages.length;
    }
    page --;



    pages[page].style.display="block";

    setTimeout("change_page()",2500);
}


function onload(){
    pages=document.getElementsByClassName("page");
    for (var i = 0; i<pages.length; i++)
    {
      pages[i].style.display="None";
    }

    change_page();
}