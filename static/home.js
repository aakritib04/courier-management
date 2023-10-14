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
      
        console.log("test LOGIN")
        console.log(JSON.stringify(data))
        // Make an AJAX request to the REST API
        $.ajax({
            url: '/login', // Replace with your API endpoint
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (response) {
                // Handle the success response from the API
                console.log("Login successful. Response:", response);
                // You can redirect the user or perform other actions here
              var uid = response.uid
              var loginType = response.loginType
              window.location.href ='login/'+loginType+'/'+uid
            },
            error: function (xhr, textStatus, errorThrown) {
                // Handle errors from the API
                console.error("Error:", errorThrown);
                alert("Login failed. Please try again.");
            }
        });
    });


  $("form#signup").submit(function (event) {
        event.preventDefault(); // Prevent the default form submission
        
        // Get the values from the form

        var username = $("#signupUsername").val();
        var email = $("#signupEmail").val();
        var password = $("#signupPassword").val();
        var signupType = $("input[name='signupType']:checked").val();
        console.log(username)
    console.log(password)
    console.log(signupType)
    console.log(email)
        // Perform validation
        // Perform validation
        if (!username || !password || !signupType || !email) {
            alert("Please fill in all fields and select a signup type.");
            return;
        }

        // Prepare data for API request
        var data = {
            username: username,
            password: password,
            signupType: signupType,
            email: email
        };
      
        console.log("test signup")
        console.log(JSON.stringify(data))
    $.ajax({
        url: '/signup',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (response) {
            console.log("Signup successful. Response:", response);
            var uid = response.uid
            var signupType = response.signupType
            window.location.href ='register/'+signupType+'/'+uid
        },
        error: function (xhr, textStatus, errorThrown) {
            console.error("Error:", errorThrown);
            alert("Signup failed. Please try again.");
        }
    });
   

    
    });
});
