$('.equip-ajax').on('change', function() {
    var id = $(this).data("pk");
    var txt = "#supply_"+id;
    var pk = this.value;
    var urlToAjax = $(this).data("url");
    var token = $(this).data("tk");
    var wareh = $(this).data("ware");
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'POST',
        data: { 'id': pk, 'warehouse' : wareh },
        success: function(info) {
            var htmldata = "";
            if (info.response == ".") {
                htmldata += '<tr class="odd"><td valign="top" colspan="11" class="dataTables_empty">No data available in table</td></tr>'
            } else {
                htmldata += 
                '<h4 class="widget-list-title equip-tittle" id="supp_'+pk+'" data-supply="'+pk+'"><b>Supplie: </b><span class="badge badge-success">'+info.supply_code+'</span> '+info.supply_name+'</h4>\
                <h4 class="widget-list-title equip-tittle"><b>Provider: </b>'+info.supply_brand+'</h4>\
                <h4 class="widget-list-title equip-tittle"><b>Actual Stock: </b>'+info.stock+'</h4>\
                <input id="stock_flag_'+id+'" type="hidden" value="'+info.stock_flag+'">'
            }
            $(txt).html(htmldata);
        }
    });
});

$('.status_select').on('change', function() {
    var stat = this.value;
    var urlToAjax = $(this).data("url");
    if(stat==2){
        var thisMain=$(this);
        var pk = thisMain.data("pk");
        var supply = $("#supply_"+pk).children().first().data("supply");
        var stock_flag = $("#stock_flag_"+pk).val();
        console.log(stock_flag)
        if(supply != null){
            if(parseInt(stock_flag)==1){
                var amount = $("#amount_"+pk).val();
                Swal.fire({
                    title: 'Are you sure?',
                    text: "I have reviewed and confirmed every detail of inventory dispatch, and I agree to confirm inventory out!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Yes, Confirm it!'
                }).then((result) => {
                    if (result.value) {
                        token=thisMain.data("tk");
                        $.ajax({
                            headers: { "X-CSRFToken": token },
                            url: urlToAjax,
                            type: 'POST',
                            data: { 'pk': pk, 'supp' : supply, 'amount' : amount },
                            success: function(info) {
                                Swal.fire({
                                    title: 'Confirmed!',
                                    text: 'Supply Dispatched',
                                    icon: 'success',
                                    confirmButtonText: 'Ok!'
                                }).then((result) => {
                                    var redirect = thisMain.data("redir");
                                    console.log(redirect)
                                    var dominen = window.location.host;
                                    var url_redirec = 'http://' + dominen + redirect;
                                    $(location).attr('href', url_redirec);
                                })
                            }
                        }); 
                    } else{
                        $('option:selected', 'select[name="select_'+pk+'"]').removeAttr('selected');
                        $('select[name="select_'+pk+'"]').find('option[value="1"]').prop("selected", true);
                    }
                }) 
            }else{
                Swal.fire({
                    title: 'Warning',
                    text: 'This supply has not entrances',
                    icon: 'warning',
                    confirmButtonText: 'Ok'
                }).then((result) => {
                    $('option:selected', 'select[name="select_'+pk+'"]').removeAttr('selected');
                    $('select[name="select_'+pk+'"]').find('option[value="1"]').prop("selected", true);
                })     
            }
        }else{
            Swal.fire({
                title: 'Error',
                text: 'Please select a supply',
                icon: 'error',
                confirmButtonText: 'Ok'
            }).then((result) => {
                $('option:selected', 'select[name="select_'+pk+'"]').removeAttr('selected');
                $('select[name="select_'+pk+'"]').find('option[value="1"]').prop("selected", true);
            })
        }
    }
})