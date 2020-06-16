$('#request-type-delete').on('show.bs.modal', function (event) {
    console.log("request-type-delete")
    var button = $(event.relatedTarget); // Button that triggered the modal
    var recipient = button.data('pk'); // Extract info from data-* attributes
    console.log(recipient);
    var modal = $(this);
    modal.find('.modal-footer #request_type_delete').val(recipient);
});