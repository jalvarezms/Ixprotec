var token = '{{csrf_token}}';
var dominen = window.location.host;
var redirect = "/inventories/inventory/entry/list"

$('#id_supply').on('change', function() {
    var equipment = this.value;
    var urlToAjax = '/equipments/supply/get';
    var empty_image = '../../../../static/img/gallery/empty.jpg';
    if (equipment != 0) {
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: urlToAjax,
            type: 'GET',
            data: { 'id': equipment },
            success: function(info) {
               if (info) { 
                   $('#image_supply').attr('src', info.Source_URL);
                   $('#supply_name').html(info.name);
                   $('#supply_material').html(info.material);
                   $('#supply_brand').html(info.brand);
                   $('#supply_size').html(info.size);
                   $('#supply_color').html(info.color);
                   $('#supply_unid').html(info.units);
               }

            }
        });
    } else {
        $('#image_supply').attr('src', empty_image);
        $('#supply_description').html("");
        $('#supply_name').html("");
        $('#supply_brand').html("");
        $('#supply_size').html();
        $('#supply_color').html();
        $('#supply_unid').html();

    }


});

$('#id_status').on('change', function() {
    var check_entry_id = $('#id_status').attr('data-value');
    var ajax_service = $('#id_status').attr('data-href');

    if (this.value == 2) {
        Swal.fire({
                title: 'Are you sure?',
                text: "I have reviewed and confirmed every detail of inventory entry, and I agree to confirm inventory entry!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, Confirm it!'
            }).then((result) => {
                if (result.value) {
                    $.ajax({
                        headers: { "X-CSRFToken": token },
                        url: ajax_service,
                        type: 'GET',
                        data: { 'pk': check_entry_id },
                        success: function(info) {
                            //console.log(info);
                            Swal.fire({
                                title: 'Confirmed!',
                                text: 'Inventory entry is confirmed.',
                                icon: 'success',
                                confirmButtonText: 'Ok!'
                            }).then((result) => {
                                var url_redirec = 'http://' + dominen + redirect;
                                $(location).attr('href', url_redirec);
                            })
                        }
                    }); //ajax
                } //if
            }) //then

    } //if
})



$('#confirm').on('click', function() {
    var check_entry_id = $('#confirm').attr('data-value');
    var ajax_service = $('#confirm').attr('data-href');
    Swal.fire({
            title: 'Are you sure?',
            text: "I have reviewed and confirmed every detail of inventory entry, and I agree to confirm inventory entry!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Confirm it!'
        }).then((result) => {
            if (result.value) {
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    url: ajax_service,
                    type: 'GET',
                    data: { 'pk': check_entry_id },
                    success: function(info) {
                        //console.log(info);
                        Swal.fire({
                            title: 'Confirmed!',
                            text: 'Inventory entry is confirmed.',
                            icon: 'success',
                            confirmButtonText: 'Ok!'
                        }).then((result) => {
                            var url_redirec = 'http://' + dominen + redirect;
                            $(location).attr('href', url_redirec);
                        })
                    }
                }); //ajax
            } //if
        }) //then



});