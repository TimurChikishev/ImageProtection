var file_list = []
var dt = new DataTransfer();

function readURL(input) {

    console.log(input.files)
    if (file_list.length < 2) {
        dt.items.add(input.files[0]);
        file_list = dt.files;
    } else {
        removeUpload();
    }

    if (input.files.length < file_list.length)
        input.files = file_list

    if (input.files && file_list[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            if (file_list.length == 2)
                $('.image-upload-wrap').hide();

            $('.file-upload-image' + file_list.length).attr('src', e.target.result);
            $('.file-upload-content').show();
        };


        reader.readAsDataURL(file_list[file_list.length - 1]);


    } else {
        removeUpload();
    }
}

function removeUpload() {
    file_list = [];
    dt.clearData();
    document.getElementById('image1').src = "";
    document.getElementById('image2').src = "";
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}
$('.image-upload-wrap').bind('dragover', function() {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function() {
    $('.image-upload-wrap').removeClass('image-dropping');
});