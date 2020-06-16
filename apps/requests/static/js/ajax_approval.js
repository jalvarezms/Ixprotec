$('.btn-response').on('click', function() {
    var dominen = window.location.host;
    var token = $("#csrf_token").val()
    var success_url = $('#succes_url').val()
    var code_resp = $(this).attr('data-response');
    var protocolo = 'https';
    if (window.location.protocol != "https:") {
        protocolo = "http";
    }
    var urlToAjax = protocolo + '://' + dominen + '/requests/manage/approval/';
    var observation = $('#observation').val()
    var request_id = $('#employee_request_id').val()
    urlToAjax = urlToAjax + request_id + '/' + code_resp
    success_url = protocolo + '://' + dominen + success_url
    console.log(success_url);
    if (code_resp) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: urlToAjax,
            type: 'POST',
            data: { 'observa': observation, 'pk': request_id, 'pks': code_resp },

            success: function(info) {
                if (info) {
                    console.log(info);
                    Swal.fire({
                        position: 'top-end',
                        icon: 'success',
                        title: 'Your reply has been saved',
                        showConfirmButton: false,
                        timer: 1500
                    })
                    $(location).attr('href', success_url);

                }

            }
        });
    } else {
        console.log("NO CODE REPONSE" + code_resp);

    }


});