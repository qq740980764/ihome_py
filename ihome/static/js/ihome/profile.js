function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(document).ready(function(){
    $("#form-avatar").submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url:"/api/v1.0/users/avatar",
            type:"post",
            contentType:"json",
            headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            success:function(resp){
                if(resp.errno==0){
                    $("#user-avatar").attr("src",resp.data.avatar_url)
                }else{
                    alert(resp.errmsg)
                }
            }

        })
    })

    $("#form-name").submit(function(e){
        var name = $("#user-name").val();
        if (!name){
            alert("请填写用户名")
            return;
        }
        data_name = {"name":name}
        name = JSON.stringify(data_name)
        e.preventDefault()
        $.ajax({
            url:"/api/v1.0/user/name",
            type:"PUT",
            data:name,
            contentType: "application/json",
            dataType: "json",
             headers:{
                "X-CSRFToken": getCookie("csrf_token")
            },
            success:function(resp){
                if (resp.error==0){
                    $("#error-msg").hide()
                    showSuccessMsg();
                } else if (resp.errno == "4101") {
                    location.href = "/login.html";
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })
})