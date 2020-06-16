var token = '{{csrf_token}}';
$('#id_equipment').on('change', function() {
    var equipment = this.value;
    var urlToAjax = '/equipments/get';
    var empty_image = '../../../../../static/img/gallery/empty.jpg';
    console.log(equipment);
    if (equipment != 0) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: urlToAjax,
            type: 'GET',
            data: { 'id': equipment },
            success: function(info) {
                if (info) {
                    $('#image_equipment').attr('src', info.image);
                    $('#equipment_code').html(info.code);
                    $('#equipment_name').html(info.name);
                    $('#equipment_description').html(info.description);
                }

            }
        });
    } else {
        $('#image_equipment').attr('src', empty_image);
        $('#equipment_description').html("");
        $('#equipment_code').html("");
        $('#equipment_name').html("");

    }


});