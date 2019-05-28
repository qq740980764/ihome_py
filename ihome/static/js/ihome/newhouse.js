function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){

    // 发布新房源
    $(".houses-list").submit(function(e){
        e.preventDefault()
        var data = {}
        $("#form-house-info").serializeArray().map(function(x){data[x.name]=x.value})
        var lst = []
        $(":checked[name=facility]").each(function(index,x){lst[index] = $(x).val()})
        data["facility"] = lst
        $.ajax({
            url:"/api/v1.0/house/info",
            type:"POST",
            data:JSON.stringify(data),
            contentType:"application/json",
            dataType:"json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success:function(resp){
                if(resp.errno=="4101"){
                    location.href="/index.html"
                }else if(resp.errno==0){
                    $("#form-house-info").hide()
                    $("#form-house-image").show()
                    $("#house-id").val(resp.data.house_id);
                }else{
                    alert(resp.errmsg)
                }
            }

        })
    })

    $.get("/api/v1.0/areas",function(resp){
        // 显示城区
        if (resp.errno==0){
            // for(Num=0;Num<resp.areas.length;Num++){
            //     area = resp.areas[Num]
            //     $(".form-control").append('<option value="'+area.id+'">'+area.name+'</option>')
            //
            // }
            areas = resp.data
            var html = template("areas-tmpl",{"areas":areas})
            $("#area-id").html(html)
        }
    })

    $("#form-house-image").submit(function(e){
        e.preventDefault()
        $(this).ajaxSubmit({
            url:"/api/v1.0/house/image",
            type:"POST",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    $(".house-image-cons").append('<img src="' + resp.data.image_url +'">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })
})