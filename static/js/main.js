$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                //$('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').attr('src',e.target.result);
                //$('#imagePreview').hide();
                //$('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    
    function GetSelectedValue(){
				var e = document.getElementById("model");
				var result = e.options[e.selectedIndex].value;
				if (result=='Simple') 
				{
    				$('#imgPreview1').attr("src","/static/Pics/output_simple.jpg");
				}
				else if (result=='Viterbi')
				{
    				$('#imgPreview1').attr("src","/static/Pics/output_viterbi.jpg");
				}
    			//$('#model').val('');	
    				
				//document.getElementById("result").innerHTML = result;
			}
			
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        $('.dummy-section').hide();
        $('.dummy-section_1').hide();
        $('.dummy_output').hide();
        readURL(this);
    });
    
    $('#btn-predict_1').click(function () {
        $('.dummy-section').show();
        //$('.dummy-section_1').hide();
        $('.dummy_output').show();
        GetSelectedValue();
        //$("#imgPreview1").attr("src","");
        //$("#menu-open-file").attr.value = '';
        //if result=='Simple':
        //$('#imgPreview1').attr("src","/static/Pics/output_viterbi.jpg");
        //extra
    });
    
    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        //console.log('Success!');
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            //cache: false,
            processData: false,
            //async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                //$('#result').fadeIn(600);
                //$('#result').text(' Result:  ' + data);
                //$('#btn-predict_1').hide();
                $('.dummy-section_1').show();
                console.log('Success!');
            },
            complete: function (data) {
              //$('.dummy-section').show();
             }
        });
    });

});