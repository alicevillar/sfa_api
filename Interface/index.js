
(function ($) {

    function generate_autenticate_key(form) {
        // Comunica com a API mandando o post com os dados do user
        alert('vai fazer o post');
        var payload = {
            'firstName': $("#firstName").val(),
            'lastName': $("#lastName").val(),
            'email': $("#email").val(),
        };
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/users/api/v1/register",
            data: payload, // pega os dados do formulário
            dataType: 'json',
            contentType: 'application/json;charset=UTF-8',
            cors: true,
            success: function (data) {
                console.log(data); // mostrar o retorno da api.
            },
            error: function (error) {
                console.log('An error occurred.');
                console.log(error);
            },
        });
    };

    $(document).ready(function () {
        // Função pega o evento de submit do form
        $("#generate_authentication_key").submit(function (event) {
            alert("function has been called");
            event.preventDefault();
            // Define o formulário
            var form = $(this);
            generate_autenticate_key(form);
        });
    });


    function download(form) {
        // Comunica com a API mandando o post com os dados do user
        alert('vai fazer o post');
        var payload = {
            'firstName': $("#firstName").val(),
            'lastName': $("#lastName").val(),
            'email': $("#email").val(),
        };
        $.ajax({
            type: "GET",
            url: "http://127.0.0.1:5000/pictures/api/v1/download",
            data: payload, // pega os dados do formulário
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                console.log(data); // mostrar o retorno da api.
            },
            error: function (error) {
                console.log('An error occurred.');
                console.log(error);
            },
        });
    };



    function upload(form) {
        // Comunica com a API mandando o post com os dados do user
        alert('vai fazer o post');
        var payload = {
            'firstName': $("#firstName").val(),
            'lastName': $("#lastName").val(),
            'email': $("#email").val(),
        };
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/pictures/api/v1/upload",
            data: payload, // pega os dados do formulário
            dataType: 'json',
            contentType: 'application/json;charset=UTF-8',
            success: function (data) {
                console.log(data); // mostrar o retorno da api.
            },
            error: function (error) {
                console.log('An error occurred.');
                console.log(error);
            },
        });
    };

// Funcao para pegar o evento de submit do form

$(document).ready(function () { // this will activate the following code

$('#sign_user').submit(function(event) {
alert("submiting form")
event.preventDefault();
    var payload = {
        'email': $("#email").val(),
        'password': $("#password").val()}

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/users/api/v1/register",
        data: payload, // pega os dados do formulário
        dataType: 'json',
        crossDomain: true,
        contentType: 'application/json;charset=UTF-8',
        success: function (data) {
            console.log(data); // mostrar o retorno da api.
           
            var user = {
                'email': $("#email").val(),
                'password': $("#password").val(), 

            }
            // setting the user (localstorage - it is a cookie of the webbrowser)
            localStorage.setItem(user)
            window.location.href = 'file:///C:/Users/Alice/Desktop/INTERFACE_SFS/gdpr.html'


        },
        error: function (error) {
            console.log('An error occurred.');
            console.log(error);
        },
    })
})
    ;
}

)






})(jQuery);



