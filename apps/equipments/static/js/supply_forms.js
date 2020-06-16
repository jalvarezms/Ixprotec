$(document).ready(function() {
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
                        $('#equipment_class').html(info.class);
                        $('#equipment_name').html(info.code + " " + info.name);
                        $('#equipment_area').html(info.area);
                        $('#equipment_type').html(info.type);
                        $('#equipment_usefull').html(info.time_of_life);
                        $('#equipment_description').html(info.description.substring(0, 64));
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


});