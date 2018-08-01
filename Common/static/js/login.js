$('.login-forget span').click(function() {
    $(".login-input-wrapper").addClass("forget");
    $(".login-logo").addClass("forget");
    $(".login-text").removeClass("forgetCancel");    
    $(".login-text").addClass("forget");
    document.getElementById("idLoginText").innerHTML = "Enter your email to receive your lost password.";
});
$('.login-forget-cancel span').click(function() {
    $(".login-input-wrapper").removeClass("forget");
    $(".login-logo").removeClass("forget"); 
    $(".login-text").removeClass("forget");
    $(".login-text").addClass("forgetCancel");
    document.getElementById("idLoginText").innerHTML = "Welcome to PR&#923XO panel. please input your username and password to reach out your dashboard section. ";
       
});
