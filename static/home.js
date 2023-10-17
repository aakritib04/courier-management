  $(document).ready(function () {
  
      $("form#login").submit(function (event) {
          event.preventDefault(); // Prevent the default form submission
          
  
          var username = $("#username").val();
          var password = $("#password").val();
          var loginType = $("input[name='loginType']:checked").val();
  
  
          if (!username || !password || !loginType) {
              alert("Please fill in all fields and select a login type.");
              return;
          }
  
  
          var data = {
              username: username,
              password: password,
              loginType: loginType
          };
        
          console.log(JSON.stringify(data))
  
          $.ajax({
              url: '/login', 
              type: 'POST',
              data: JSON.stringify(data),
              contentType: 'application/json',
              success: function (response) {
                
                  console.log("Login successful. Response:", response);
                  
                var uid = response.uid
                var loginType = response.loginType
                window.location.href ='login/'+loginType+'/'+uid
              },
              error: function (xhr, textStatus, errorThrown) {
                  
                  console.error("Error:", errorThrown);
                  alert("Login failed. Please try again.");
              }
          });
      });
  
  
    $("form#signup").submit(function (event) {
          event.preventDefault(); 
          
          
  
          var username = $("#signupUsername").val();
          var email = $("#signupEmail").val();
          var password = $("#signupPassword").val();
          var signupType = $("input[name='signupType']:checked").val();
          console.log(username)
          
          if (!username || !password || !signupType || !email) {
              alert("Please fill in all fields and select a signup type.");
              return;
          }
  
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
  