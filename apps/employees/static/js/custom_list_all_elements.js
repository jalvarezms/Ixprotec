let a=[];
Array.from(document.getElementsByClassName("collapse")).forEach(function(item) {
        a.push(item.id);
});
function showAll(){
    a.forEach(forShow =>{
            document.getElementById(forShow).classList.add("show");
    });
}
function hideAll(){
    a.forEach(forHide =>{
            document.getElementById(forHide).classList.remove("show");
    })
}