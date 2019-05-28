function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    var house_id = decodeQuery()
    house_id = house_id["id"]
    $.get("/api/v1.0/house/"+house_id,function(resp){
        if(resp.errno=="0"){
            $(".swiper-container").html(template("house-image-tmpl",{"img_urls":resp.data.house.img_urls,"price":resp.data.house.price}))
            $(".detail-con").html(template("detail-con-tmpl",{"house":resp.data.house}))
            console.log(resp.data)
            if (resp.data.user_id != resp.data.house) {
                $(".book-house").attr("href", "/booking.html?hid="+resp.data.house.hid);
                $(".book-house").show();
            }
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
        }else{
            alert(resp.errmsg)
        }
    })

})