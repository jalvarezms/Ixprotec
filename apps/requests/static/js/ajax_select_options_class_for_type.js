$(".ec-tags").select2({tags: true});
$(".select2-data").select2();
	

    $("#id_element_type").change(function () {
      var type_id = $(this).val();       
      $.ajax({                      
        url: 'http://127.0.0.1:8000/elements/ajax/select_options_class_for_type',                   
        data: {
          'type_id': type_id      
        },
        success: function (data) { 
            console.log(data)
            $("#id_element_classification").html(data); 
        }
      });

    });
