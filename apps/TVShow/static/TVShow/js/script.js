$(document).ready(function () {
    $('#title').keyup(function () {
        var data = $("#addForm").serialize(); // capture all the data in the form in the variable data
        $.ajax({
                method: "POST", // we are using a post request here, but this could also be done with a get
                url: "/shows/new",
                data: data
            })
            .done(function (res) {
                $('#titleMsg').html(res); // manipulate the dom when the response comes back
            });
    });
});