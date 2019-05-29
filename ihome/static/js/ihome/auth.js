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
    $.get("/api/v1.0/user/auth",function(resp){
        if(resp.errno==0){
            if(resp.data.real_name && resp.data.id_card){
                console.log("已经进入")
                var real_name = $("#real-name").val(resp.data.real_name)
                var id_card = $("#id-card").val(resp.data.id_card)
                $("#real-name").prop("disabled",true)
                $("#id-card").prop("disabled",true)
                $("#form-auth>input[type=submit]").hide();
            }
        }
        else{
                alert(resp.errmsg)
            }
    })


    $("#form-auth").submit(function(e){
        e.preventDefault()
        var real_name = $("#real-name").val()

        var id_card = $("#id-card").val()
        if (real_name == "" ||  id_card == "") {
            $(".error-msg").show();
        }
        dict_info = {
            "real_name":real_name,
            "id_card":id_card,
        }
        json_info = JSON.stringify(dict_info)
        $.ajax({
            url:"/api/v1.0/user/auth",
            type:"POST",
            data:json_info,
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function(resp){
                if (resp.errno==0){
                    $(".error-msg").hide()
                    showSuccessMsg()
                    $("#real-name").prop("disabled",true)
                    $("#id-card").prop("disabled",true)
                     $("#form-auth>input[type=submit]").hide();
                }

            }

        })
    })
})
