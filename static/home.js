// login.js

$(document).ready(function () {
    // Handle form submission
    $("form#login").submit(function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get the values from the form
        var username = $("#username").val();
        var password = $("#password").val();
        var loginType = $("input[name='loginType']:checked").val();

        // Perform validation
        if (!username || !password || !loginType) {
            alert("Please fill in all fields and select a login type.");
            return;
        }

        // Prepare data for API request
        var data = {
            username: username,
            password: password,
            loginType: loginType
        };
      
        console.log("test")
        console.log(JSON.stringify(data))
        // Make an AJAX request to the REST API
        $.ajax({
            url: '/api/login', // Replace with your API endpoint
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (response) {
                // Handle the success response from the API
                console.log("Login successful. Response:", response);
                // You can redirect the user or perform other actions here
            },
            error: function (xhr, textStatus, errorThrown) {
                // Handle errors from the API
                console.error("Error:", errorThrown);
                alert("Login failed. Please try again.");
            }
        });
    });
});
