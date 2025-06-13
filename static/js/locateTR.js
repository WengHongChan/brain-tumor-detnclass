$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.image-section2').hide();
    $('.loader').hide();
    $('.loader2').hide();

    function isImage(fileType) {
      switch (fileType.toLowerCase()) {
        case 'jpg':
        case 'jpeg':
        case 'png':
          return true;
      }
      return false;
    }

    function checkMRIImg(form_data, imgURL){

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/checkGreyscale',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                if (data === "0"){
                    $('.image-section').hide();
                    return failValidation('Image uploaded is not of an MRI Image!');
                }else{
                    if(imgURL !== ""){
                        $('.image-section').show();
                        $('#imagePreview').css('background-image', 'url(' + imgURL + ')');
                        $('#imagePreview').hide();
                        $('#imagePreview').fadeIn(650);

                        // Show loading animation
                        $(this).hide();
                        $('.loader2').show();

                        // Make prediction by calling api /predict
                        $.ajax({
                            type: 'POST',
                            url: '/highlightTumorRegion',
                            data: form_data,
                            contentType: false,
                            cache: false,
                            processData: false,
                            async: true,
                            success: function (data) {
                                // Get and display the result
                                $('.loader2').hide();
                                $('.image-section2').show();
                                $('#btn-showTumor').hide();

                                div = "<div id=\"imagePreview2\" style=\"background-image: url(\'" + data + "\');\"></div>"
                                $('#imgTumorRegion').append(div);

                                $('#imagePreview2').hide();
                                $('#imagePreview2').fadeIn(650);
                            },
                        });
                    }
                }
            },
        });
    }

    function failValidation(msg) {
      alert(msg);
    }

    // Upload Preview
    function readURL(input, form_data) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var imageFileType = "";
                fileURL = e.target.result;
                var startIndex = fileURL.indexOf('/');
                var endIndex = fileURL.indexOf(';', startIndex + 1);
                var textBetweenChars = fileURL.substring(startIndex + 1, endIndex);
                imageFileType = fileURL.substring(startIndex + 1, endIndex);
                localStorage.setItem("theImg", fileURL);

                $('.image-section2').hide();
                $('.loader2').hide();

                if (!isImage(imageFileType)) {
                    $('.image-section').hide();
                    return failValidation('Only image with format .png, .jpg and .jpeg is allowed!');
                }else{
                    localStorage.setItem("theImg", fileURL);
                    checkMRIImg(form_data, fileURL);
                }

            }
            reader.readAsDataURL(input.files[0]);
        }else{
            $('.image-section').hide();
            $('.image-section2').hide();
            $('.loader').hide();
            $('.loader2').hide();
        }
    }

    $("#imageUpload").change(function () {
        $('.loader').hide();
        $('.loader2').hide();
        $('.image-section2').hide();
        $('#imagePreview2').hide();
        var divtoDel = document.getElementById("imagePreview2");
        if(divtoDel){
            divtoDel.parentNode.removeChild(divtoDel);
        }

        var form_data = new FormData($('#upload-file')[0]);

        readURL(this, form_data);

        //--------------------------------------------------------
        var img_Loc = "";

        if (localStorage && 'theImg' in localStorage) {
            img_Loc = localStorage.getItem("theImg");
        }
    });

});