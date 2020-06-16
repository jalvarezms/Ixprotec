$(document).ready(function() {
    console.log("ready!");
    $("h5#doc_title1").removeClass("bg-grey-transparent-1 text-inverse");
    $("h5#doc_title1").addClass("bg-success text-white");

    $(".list-documet-title").click(function() {
        $(".list-documet-title").removeClass("bg-success text-white");
        var url_doc = $(this).attr('value');
        var objet_embed = "<object data='" + url_doc + "'  type='application/pdf' width='900px' height='900px'></object>"
        $("#object_document").html(objet_embed);
        $(this).removeClass("bg-grey-transparent-1 text-inverse");
        $(this).addClass("bg-success text-white");

    });
});