function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function logout() {
    $.ajax({
        url:"/api/v1.0/session",
            type:"delete",
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function(resp){
                if(resp.errno==0){
                    location.href="/index.html"
                }
            }

    })
}

$(document).ready(function(){
    $.get("/api/v1.0/user",function(resp){
        if(resp.errno==0){
            $("#user-name").html(resp.data.name)
            $("#user-mobile").html(resp.data.mobile)
            if (resp.data.avatar_url){
                $("#user-avatar").attr("src",resp.data.avatar_url)
            }

        }
        else{
            alert(resp.errmsg)
        }
    })
})