$(".delete-commentss").click(function() {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
    var url_data = $(this).attr('data-ref')
        //alert(url_data)
    if (url_data) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_data,
            type: 'POST',
            data: {

            },
            success: function(info) {
                //alert(info)
                if (info) {
                    $('#comments-base').html(info);
                }

            }
        });
    } else {
        //alert("vacio")
    }
});

function delete_comments(url_data) {
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        //alert("delete_comments")
    if (url_data) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url_data,
            type: 'POST',
            data: {

            },
            success: function(info) {
                //alert(info)
                if (info) {
                    $('#comments-base').html(info);
                }

            }
        });
    } else {
        //alert("vacio")
    }
}