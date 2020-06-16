$(document).ready(function() {

    $("#sender_comment").click(function() {
        var comment = $('#comment_id').val()
        var post = $('#post_id').val()
        var token = $('input[name="csrfmiddlewaretoken"]').attr('value')
        var urlToAjax = '/publications/ create/comments';
        var url_data = $("#sender_comment").attr('data-ref')

        if (comment) {
            $.ajax({
                headers: { "X-CSRFToken": token },
                url: url_data,
                type: 'POST',
                data: {
                    'comment': comment,
                    'post': post
                },
                success: function(info) {
                    //alert(info)
                    if (info) {
                        $('#comment_id').val('')
                        $('#comment_id').attr('value', '')
                        $('#comment_id').empty()
                        $('#comments-base').html(info);
                    }

                }
            });
        } else {
            //alert("vacio")
        }
    });


});