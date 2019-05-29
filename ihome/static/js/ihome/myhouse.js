$(document).ready(function(){
    $(".auth-warn").show();
    $.get("/api/v1.0/user/auth",function(resp){
          if(resp.errno=="4101"){
              location.href("/index.html")
            }
          else if (resp.errno==0){
            if(!(resp.data.real_name && resp.data.id_card)){
                console.log(qwe)
                $(".auth-warn").show()
                return

            }
            $(".auth-warn").hide()
            $.get("/api/v1.0/user/house",function(resp){
                    if (resp.errno=="0"){
                        $("#houses-list-2").html(template("houses-list-tmpl",{houses:resp.data.houses}))
                    }else{
                        $("#houses-list-2").html(template("houses-list-tmpl",{houses:[]}))

                    }
                })



        }
    })
})