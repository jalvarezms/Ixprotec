var token = '{{csrf_token}}';
$('#Position').on('change', function() {
    var position = this.value;
    var urlToAjax = '/equipments/asign_equipment_list';
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'GET',
        data: { 'id': position },
        success: function(info) {
            console.log(info);
            var htmldata = "";
            if (info.response == ".") {
                htmldata += '<tr class="odd"><td valign="top" colspan="11" class="dataTables_empty">No data available in table</td></tr>'
            } else {
                for (var i = 0; i < info.length; i++) {
                    htmldata += '<tr class="odd gradeX" >\
                    <td >\
                        <span class="badge badge-success">' + info[i].position_code + '</span>\
                        <strong class="f-s-12">' + info[i].position_name + '</strong>\
                    </td>\
                    <td >\
                        <div class="panel-body">\
                            <ul class="media-list">\
                                <li class="media media-xs">\
                                    <a class="media-left" href="javascript:;">\
                                        <img src="' + info[i].equipment_photo + '" alt="" class="media-object rounded-corner" />\
                                    </a>\
                                    <div class="media-body align-self-center">\
                                        <p class="m-b-0">\
                                            <span class="badge badge-success">' + info[i].equipment_code + '</span>\
                                        </p>\
                                        <span >\
                                            <strong class="f-s-12">' + info[i].equipment_name + '</strong>\
                                        </span>\
                                    </div>\
                                </li>\
                            </ul>\
                        </div>\
                    </td>\
                    <td >' + info[i].description + '</td>\
                    <td >' + info[i].maximum + '</td>\
                    <td >' + info[i].start_date + '</td>\
                    <td >' + info[i].end_date + '</td>\
                    <td >' + info[i].inspection_period + '</td>\
                    <td > <a class="btn btn-white" href="/equipments/perposition/update/' + info[i].id + '?val=1"><i class="fas fa-lg fa-fw m-r-10 fa-edit"></i></a>\
                    <a class="btn btn-white" href="#" data-toggle="modal" data-target="#delete_perposition" data-pos="' + info[i].pos + '" data-pk="' + info[i].id + '"><i class="fas fa-lg fa-fw m-r-10 fa-trash"></i></a>\
                    </td></tr>'
                }
            }
            $('#PositionList').html(htmldata);
            var html = '<a class="btn btn-white" id="posdata" data-pos="' + info[0].pos + '"</a> '
            $('#pos').html(html);
        }
    });

});

$('#delete_perposition').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data('pk'); // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this);
    modal.find('.modal-footer #delete-perbutton').val(recipient);
});

$('#delete-perbutton').on('click', function() {
    var pk = $(this).val();
    var urlToAjax = $(this).data("url");
    var token = $(this).data("tk");
    var posi = $('#posdata').data("pos");
    console.log(posi);
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'POST',
        data: { 'id': pk, 'pos': posi },
        success: function(info) {
            console.log(info);
            var htmldata = "";
            if (info.response == ".") {
                htmldata += '<tr class="odd"><td valign="top" colspan="11" class="dataTables_empty">No data available in table</td></tr>'
            } else {
                for (var i = 0; i < info.length; i++) {
                    htmldata += '<tr class="odd gradeX" >\
                    <td >\
                        <span class="badge badge-success">' + info[i].position_code + '</span>\
                        <strong class="f-s-12">' + info[i].position_name + '</strong>\
                    </td>\
                    <td >\
                        <div class="panel-body">\
                            <ul class="media-list">\
                                <li class="media media-xs">\
                                    <a class="media-left" href="javascript:;">\
                                        <img src="' + info[i].equipment_photo + '" alt="" class="media-object rounded-corner" />\
                                    </a>\
                                    <div class="media-body align-self-center">\
                                        <p class="m-b-0">\
                                            <span class="badge badge-success">' + info[i].equipment_code + '</span>\
                                        </p>\
                                        <span >\
                                            <strong class="f-s-12">' + info[i].equipment_name + '</strong>\
                                        </span>\
                                    </div>\
                                </li>\
                            </ul>\
                        </div>\
                    </td>\
                    <td >' + info[i].description + '</td>\
                    <td >' + info[i].maximum + '</td>\
                    <td >' + info[i].start_date + '</td>\
                    <td >' + info[i].end_date + '</td>\
                    <td >' + info[i].inspection_period + '</td>\
                    <td > <a class="btn btn-white" href="/equipments/perposition/update/' + info[i].id + '?val=1"><i class="fas fa-lg fa-fw m-r-10 fa-edit"></i></a>\
                    <a class="btn btn-white" href="#" data-toggle="modal" data-target="#delete_perposition" data-pk="' + info[i].id + '"><i class="fas fa-lg fa-fw m-r-10 fa-trash"></i></a>\
                    </td></tr>'
                }
            }
            $('#PositionList').html(htmldata);
            var html = '<a class="btn btn-white" id="posdata" data-pos="' + info[0].pos + '"</a> '
            $('#pos').html(html);
        }
    });
});

var token = '{{csrf_token}}';
$('#btn_save').click(function() {
    var form = $('#form_perpos').serialize()
    console.log(form);
    var urlToAjax = '/equipments/perposition_save';
    $('#id_equipment').val("");
    $('#id_description').val("");
    $('#id_maximum').val("");
    $('#ppsd').val("");
    $('#pped').val("");
    $('#id_inspection_period').val("");
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'POST',
        data: form,
        success: function(info) {
            console.log(info);
            var htmldata = "";
            if (info.response == ".") {
                htmldata += '<tr class="odd"><td valign="top" colspan="11" class="dataTables_empty">No data available in table</td></tr>'
            } else {
                for (var i = 0; i < info.length; i++) {
                    htmldata += '<tr class="odd gradeX" >\
                    <td >\
                        <span class="badge badge-success">' + info[i].position_code + '</span>\
                        <strong class="f-s-12">' + info[i].position_name + '</strong>\
                    </td>\
                    <td >\
                        <div class="panel-body">\
                            <ul class="media-list">\
                                <li class="media media-xs">\
                                    <a class="media-left" href="javascript:;">\
                                        <img src="' + info[i].equipment_photo + '" alt="" class="media-object rounded-corner" />\
                                    </a>\
                                    <div class="media-body align-self-center">\
                                        <p class="m-b-0">\
                                            <span class="badge badge-success">' + info[i].equipment_code + '</span>\
                                        </p>\
                                        <span >\
                                            <strong class="f-s-12">' + info[i].equipment_name + '</strong>\
                                        </span>\
                                    </div>\
                                </li>\
                            </ul>\
                        </div>\
                    </td>\
                    <td >' + info[i].description + '</td>\
                    <td >' + info[i].maximum + '</td>\
                    <td >' + info[i].start_date + '</td>\
                    <td >' + info[i].end_date + '</td>\
                    <td >' + info[i].inspection_period + '</td>\
                    <td > <a class="btn btn-white" href="/equipments/perposition/update/' + info[i].id + '?val=1"><i class="fas fa-lg fa-fw m-r-10 fa-edit"></i></a>\
                    <a class="btn btn-white" href="#" data-toggle="modal" data-target="#delete_perposition" data-pk="' + info[i].id + '"><i class="fas fa-lg fa-fw m-r-10 fa-trash"></i></a>\
                    </td></tr>'
                }
            }
            $('#PositionList').html(htmldata);
            var html = '<a class="btn btn-white" id="posdata" data-pos="' + info[0].pos + '"</a> '
            $('#pos').html(html);
        }
    });
});

var token = '{{csrf_token}}';
$('#equipment').on('change', function() {
    var url = $('#equipment').data('url');
    var equipment = this.value;
    var urlToAjax = $('#equipment').data('url');
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: urlToAjax,
        type: 'GET',
        data: { 'id': equipment },
        success: function(info) {
            var htmldata = "";
            if (info.response == ".") {
                htmldata += ''
            } else {
                console.log(info)
                htmldata += '<div class="row">\
                    <div class="col-md-1 col-sm-3 col-xs-3 col-md-offset-2 ">\
                        <div class="form-group">\
                            <div class="media media-sm m-t-0 ">\
                                <a class="media center-block text-center" href="javascript:;" >\
                                <img src="' + info.image + '" class="media-object rounded height-80 width-80  center-block text-center" />\
                                </a>\
                            </div>  \
                        </div>\
                    </div>\
                    <div class="col-md-4  col-sm-3 col-xs-3 col-md-offset-2 ">\
                        <div class="form-group">\
                            <ul class="list-group">\
                                <li class="list-group-item"><span class="badge badge-lime">Name </span><span>  ' + info.name + '</span></li>\
                                <li class="list-group-item"><span class="badge badge-lime">Description </span><span class="f-s-10">  ' + info.description + '</span></li>\
                            </ul>\
                        </div>\
                    </div>\
                    <div class="col-md-4  col-sm-3 col-xs-3 col-md-offset-2 ">\
                        <div class="form-group">\
                            <ul class="list-group">\
                                <li class="list-group-item"><span class="badge badge-lime">Type </span>  <span>  ' + info.type + '</span></li>\
                                <li class="list-group-item"><span class="badge badge-lime">Class </span><span>  ' + info.class + '</span></li>\
                            </ul>\
                        </div>\
                    </div>\
                    <div class="col-md-3  col-sm-3 col-xs-3 col-md-offset-2 ">\
                        <div class="form-group">\
                            <ul class="list-group">\
                                <li class="list-group-item"><span class="badge badge-lime">Usefull Life  </span><span>  ' + info.time_of_life + '</span></li>\
                                <li class="list-group-item"><span class="badge badge-lime">Body Part  </span><span>  ' + info.area + '</span></li>\
                            </ul>\
                        </div>\
                    </div>\
                </div>'
            }
            $('#equipment-detail').html(htmldata);
        }
    });

});