/* Display image */
var imageInput = document.getElementById('file-input');
var imageContainer = document.getElementById('image-container');
var maxImageSize = 16000000;

imageInput.addEventListener('change', function() {
    var imageFile = this.files[0];

    if (imageFile.size > maxImageSize) {
        console.error('max size' + maxImageSize + 'exceeded');
    }

    var reader = new FileReader();

    reader.onload = function(e) {
        var image = new Image();
        image.src = e.target.result;

        $(imageContainer).empty();
        $('#predictions-container').empty();
        imageContainer.appendChild(image);
    };

    reader.readAsDataURL(imageFile);
});

/* POST image */
$('#image-upload-form').on('submit', function(e) {
    e.preventDefault();

    if (!imageInput.files.length) {
        // $('#error').text('Please upload an image before you submit');
        return;
    }

    var form_data = new FormData($(this)[0]);

    $.ajax({
        cache: false,
        contentType: false,
        data: form_data,
        processData : false,
        type: 'POST',
        url: '/classify'
   })
   .done(function(data) {
        console.log('SUCCESS!');
        console.log('data', data);

        var dataArray = [];
        for (var prop in data) {
            var temp = {};
            temp.style = prop;
            temp.value = data[prop];
            dataArray.push(temp);
        }

        var sortedData = dataArray.sort(function(style1, style2){
            return style2.value - style1.value;
        });

        sortedData.forEach(function(obj) {
            $('#predictions-container').append(
                '<span style="margin-right: 45px; font-weight: bold; text-transform: uppercase">' +
                    '<a title="See more ' + obj.style + ' styles" class="style-link" target="_blank" href="https://google.com/search?q=' + obj.style + '+interior+design&tbm=isch">' + obj.style + '</a>: '  + obj.value +
                '</span>'
            );
        });

        $("html, body").animate({ scrollTop: $('#predictions-container').offset().top }, 600);
   })
   .fail(function(xhr, status, errorThrown) {
        alert("Sorry, there was a problem!");
        console.log("Error: " + errorThrown);
        console.log("Status: " + status);
        console.dir(xhr);
    });
});
