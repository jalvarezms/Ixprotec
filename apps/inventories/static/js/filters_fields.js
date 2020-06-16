$('#warehouse_id').on('change', function() {
    var warehouse_pk = $('#warehouse_id').val();
    var supply_pk = $('#supply_id').val();
    var dominen = window.location.host;
    var url_ref = 'http://' + dominen + "/inventories/inventory/movements/" + warehouse_pk + "/" + supply_pk;
    $(location).attr('href', url_ref);
});

$('#supply_id').on('change', function() {
    var warehouse_pk = $('#warehouse_id').val();
    var supply_pk = $('#supply_id').val();
    var dominen = window.location.host;
    var url_ref = 'http://' + dominen + "/inventories/inventory/movements/" + warehouse_pk + "/" + supply_pk;
    $(location).attr('href', url_ref);
});