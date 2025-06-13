$(document).ready(function () {

    const content = document.getElementById('bcontent')
    window.addEventListener("load", function(){
        if(localStorage.getItem('popState') != 'shown'){
            content.classList.add('freeze')
            document.querySelector(".popup").style.display = "block";
            localStorage.setItem('rePop',1)
        }
    });
    document.querySelector("#close").addEventListener("click", function(){
        content.classList.remove('freeze')
        document.querySelector(".popup").style.display = "none";

        setTimeout(
            function open(event){
                content.classList.add('freeze')
                document.querySelector(".popup").style.display = "block";
            },
            10000 // 10 Secs
        )
    });

    document.querySelector("#close1").addEventListener("click", function(){
        content.classList.remove('freeze')
        document.querySelector(".popup").style.display = "none";
        localStorage.setItem('popState','shown')
        localStorage.setItem('rePop',0)
    });

    // Init
    $('.image-section').hide();
    $('.image-section2').hide();
    $('.loader').hide();
    $('.loader2').hide();
    $('#result').hide();
    $('#btn-showTumor').hide();

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
                    return failValidation('Image uploaded is not of an MRI Image!');
                }else{
                    if(imgURL !== ""){
                        $('.image-section').show();
                        $('#btn-predict').show();
                        $('#imagePreview').css('background-image', 'url(' + imgURL + ')');
                        $('#imagePreview').hide();
                        $('#imagePreview').fadeIn(650);
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
        const formDataObj = {};
        form_data.forEach((value, key) => (formDataObj[key] = value));

        if(formDataObj.length == 0){
            alert("Please select an image!");
//            localStorage.setItem("selected", 1);
        }else{
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    var imageFileType = "";
                    fileURL = e.target.result;
                    var startIndex = fileURL.indexOf('/');
                    var endIndex = fileURL.indexOf(';', startIndex + 1);
                    var textBetweenChars = fileURL.substring(startIndex + 1, endIndex);
                    imageFileType = fileURL.substring(startIndex + 1, endIndex);

                    $('.image-section2').hide();
                    $('.loader2').hide();
                    $('#btn-showTumor').hide();

                    if (!isImage(imageFileType)) {
                        $('.image-section').hide();
                        $('#btn-predict').hide();
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
                $('#result').hide();
                $('#btn-showTumor').hide();
            }
        }
    }

    var input = document.getElementsByTagName('input')[0];

    input.onclick = function () {
        $('.loader').hide();
        $('.loader2').hide();
        $("#row1").remove();
        $('#result').hide();
        $('#btn-showTumor').hide();
        $('.image-section').hide();
        $('.image-section2').hide();
        $('#imagePreview2').hide();
        $('#btn-showTumor').hide();
        this.value = null;
    };

    input.onchange = function () {
        var divtoDel = document.getElementById("imagePreview2");
        if(divtoDel){
            divtoDel.parentNode.removeChild(divtoDel);
        }
        var form_data = new FormData($('#upload-file')[0]);

        readURL(this, form_data);
    };

    //Show Tumor
    $('#btn-showTumor').click(function(){
        var img_Loc = "";

        if (localStorage && 'theImg' in localStorage) {
            img_Loc = localStorage.getItem("theImg");
        }

        var form_data = new FormData($('#upload-file')[0]);

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
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.resultdiv').show();
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#btn-showTumor').fadeIn(600);

                var tableContent = '';

                tableContent += '<tr id="row1" class="active-row">';
                tableContent += '<td style="text-align: center;">' + data['detectTumor'] + '</td>';
                tableContent += '<td style="text-align: center;">' + data['typeTumor'] + '</td>';
                tableContent += '</tr>';

                $('#result tbody').append(tableContent);
            },
        });
    });

});