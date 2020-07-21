Dropzone.autoDiscover = false;

function init() {
    let dz1 = new Dropzone("#dropzone1", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    let dz2 = new Dropzone("#dropzone2", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz1.on("addedfile", function() {
        if (dz1.files[1]!=null) {
            dz1.removeFile(dz1.files[0]);        
        }
    });

    dz2.on("addedfile", function () {
        if (dz2.files[1] != null) {
            dz2.removeFile(dz2.files[0]);
        }
    });


    dz1.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/signature_verification1";

        $.post(url, {
            image_data1: file.dataURL
        },function(data, status) {
            
            console.log(data);
            if (!data || data.length==0) {
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            
            
            // dz.removeFile(file);            
        });
    });

    dz2.on("complete", function (file) {
        let imageData = file.dataURL;

        var url = "http://127.0.0.1:5000/signature_verification2";

        $.post(url, {
            image_data2: file.dataURL
        }, function (data, status) {

            console.log(data);
            if (!data || data.length == 0) {
                $("#divClassTable").hide();
                $("#error").show();
                return;
            }


            // dz.removeFile(file);            
        });
    });

    $("#submitBtn1").on('click', function (e) {
        dz1.processQueue();
    });

    $("#submitBtn2").on('click', function (e) {
        dz2.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});