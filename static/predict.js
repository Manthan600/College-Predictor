let open = document.getElementById("symbol-1");

open.addEventListener("click",function run(){
    let element1 = document.getElementById("section-1");
    let element2 = document.getElementById("section-2");

    element1.style.display = "none";
    element2.style.display = "flex";
    element2.classList.add("toggle");
});

let cls = document.getElementById("symbol-2");

cls.addEventListener("click",function end(){
    let element3 = document.getElementById("section-1");
    let element4 = document.getElementById("section-2");

    element3.style.display = "flex";
    element4.style.display = "none";
    element3.classList.add("toggle");
    element4.classList.remove("toggle");
});