function create_like(url_data, data_pk) {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')

    if (url_data) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_data,
            type: 'GET',
            data: {},
            success: function(info) {
                if (info) {
                    $('#footer_btn_like_' + data_pk).empty()
                    $('#footer_btn_like_' + data_pk).append(info);
                }

            }
        });
    } else {
        //alert("vacio")
    }
}