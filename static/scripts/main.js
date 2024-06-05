function showSidebar() {
    const sidebar = document.querySelector('.sidebar') 
    sidebar.style.display = 'flex'
}

function hideSidebar() {
    const sidebar = document.querySelector('.sidebar') 
    sidebar.style.display = 'none'  
}

$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
            data : {
                name :$('#name').val(),
                email :$('#email').val(),
                number :$('#phone').val(),
                message :$('#message').val()
            },
            type : 'POST',
            url : '/contact'
        })
        .done(function(data) {
            if (data.error) {
                $('#alert').text(data.error).show();
                $('#success').hide();
            }
            else {
                $('#suceess').text(data.name).show();
                $('#alert').hide();
            }
        })
        event.preventDefault();
    });
});

function alert() {
    const mx = document.querySelector('.alert') 
    mx.style.display = 'block'  
}