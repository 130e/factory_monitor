$(document).ready(function () {
    setInterval("ask()",5000);
    function ask()
    $.ajax(
        {
            type: "get",
            url: "/api/machine/controler/time/latest/",
            dataType: "json",
            success: function (msg) {       //msg为返回的json数据
                $.each(msg.data.list, function (index, sport) {
                    $(".water_in").html(sport.water_in);
                    $(".water_out").html(sport.water_out);
                    $(".COD").html(sport.COD);
                    $(".BOD").html(sport.BOD);
                })
            }
        }
    )

    $.ajax(
        {
            type: "get",
            url: "/api/machine/processor/time/latest/",
            dataType: "json",
            success: function (msg) {
                 $.each(msg.data.list, function (index, sport) {
                    $(".level").html(sport.level);
                    $(".temperature").html(sport.temperature);
                    $(".PH").html(sport.PH);
                    $(".density").html(sport.density);

                }）
        }
    )
});