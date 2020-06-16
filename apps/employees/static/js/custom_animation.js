$(document).ready(()=>{
    $(".toAppend").css("display", "none");
    let flag=false;
    $(".btn-info").click(()=>{
        if(flag){
            $(".comment").slideUp(600, ()=>{
                $(".toAppend").css("display", "none");
            });
            flag=false;
        }else{
            flag=true;
            $(".toAppend").css("display", "inline");
            $(".comment").slideDown(600);
        }
    });
})