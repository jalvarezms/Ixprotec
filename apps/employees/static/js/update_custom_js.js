$(document).ready(function() {
    $(".select2-data").select2({tags: true});
    $('.js-example-basic-single').select2();
    $("#myArea").select2("enable");
    $("#mySizeOuter").select2("enable");

    var token = $("token_input").val();
    var urlToAjax = $("#url_ajax").val();
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'GET',
        data: { 'id': $("#areaid_input").val()},
        success: function(info) {	
            data=[]
            data=[{id :"" , text: "Select body size", sizeid: "",sizeCode:"Not Select", sizeGender: "Not Select", sizeDescription: "Not Select", sizeName: "Not Select"} ] ;
            $('#mySize').empty();
            for (let i in info){
                data.push({id :info[i].id ,value :info[i].id,  text: info[i].name, sizeid: info[i].id,sizeCode:info[i].code,sizeGender: info[i].gender, sizeDescription: info[i].description, sizeName: info[i].name});
            }
            $('#mySize').select2({data:data})

        }
    });

    $('#myArea').on('select2:select', function (e) {
        var data = e.params.data;
        area_id = $(this).val()
        document.getElementById("area-code").innerHTML=data.element.dataset.areaCode;
        document.getElementById("area-description").innerHTML=data.element.dataset.areaDescription;
        document.getElementById("area-name").innerHTML=data.element.dataset.areaName;
    
        var token = '{{csrf_token}}';
        var urlToAjax = $("#url_ajax").val();
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: urlToAjax,
            type: 'GET',
            data: { 'id': area_id  },
            success: function(info) {
                data=[{id :"" , text: "Select body size", sizeid: "",sizeCode:"Not Select", sizeGender: "Not Select", sizeDescription: "Not Select", sizeName: "Not Select"} ] ;
                $('#mySize').empty();
                for (let i in info){	
                    if(info.length === 1){
                        data.push({id :info[i].id , text: info[i].name, sizeid: info[i].id,sizeCode:info[i].code,sizeGender: info[i].gender, sizeDescription: info[i].description, sizeName: info[i].name});
                    } else {
                        data.push({id :info[i].id , text: info[i].name, sizeid: info[i].id,sizeCode:info[i].code,sizeGender: info[i].gender, sizeDescription: info[i].description, sizeName: info[i].name});
                    }				
                }
                clear_table_size();
                $('#mySize').select2({data:data});
    
            }
        });
    });
    
    $('#mySizeOuter').on('select2:select', function(e){
        data=$("#mySize").select2('data')[0];
        console.log(data.sizeid)
        document.getElementById("id-size").value = data.sizeid;
        clear_table_size()
        $("#size-code").append(data.sizeid);
        $("#size-description").append(data.sizeDescription);
        $("#size-code").append(data.sizeCode);
        $("#size-gender").append(data.sizeGender);
        $("#size-name").append(data.sizeName)  ;
    
    })
    
    function clear_table_size(){
        $("#size-code").empty();
        $("#size-description").empty();
        $("#size-code").empty();
        $("#size-gender").empty();
        $("#size-name").empty();
    }
});
