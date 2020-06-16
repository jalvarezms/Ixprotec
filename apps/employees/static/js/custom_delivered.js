$('.alert').change(function() {
    console.log("Hola")
    var thisMain = $(this)
    var inputt = thisMain.data('inp')
    console.log(inputt)
    Swal.fire({
        title: 'Warning!',
        text: 'If you click accept you agree that the supply is in good conditions and have all the certification. If you click refused please get back the supply to warehouse',
        icon: 'warning',
        showCancelButton: true,
        cancelButtonColor: '#d33',
        confirmButtonText: 'Accept',
        cancelButtonText: 'Refuse'
    }).then((result) => {
        if (result.value) {
            thisMain.prop('checked', true)
            $('#'+inputt).prop('value', 'accept')
        }
        else{
            thisMain.prop('checked', false)
            $('#'+inputt).prop('value', 'refuse')
        }
    })
})