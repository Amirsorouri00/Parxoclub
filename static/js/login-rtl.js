$('.login-forget span').click(function() {
    $(".login-input-wrapper").addClass("forget");
    $(".login-logo").addClass("forget");
    $(".login-text").removeClass("forgetCancel");    
    $(".login-text").addClass("forget");
    document.getElementById("idLoginText").innerHTML = "برای بازیابی گذرواژه، پست الکترونیک خود را وارد نمایید.";
});
$('.login-forget-cancel span').click(function() {
    $(".login-input-wrapper").removeClass("forget");
    $(".login-logo").removeClass("forget"); 
    $(".login-text").removeClass("forget");
    $(".login-text").addClass("forgetCancel");
    document.getElementById("idLoginText").innerHTML = "به پنل مدیریت پراکسو خوش آمدید. برای دست‌رسی به حساب خود، نام کاربری و گذرواژه را وارد کنید.";
       
});
