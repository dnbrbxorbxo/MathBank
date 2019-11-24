function charts(ctx, type, label, data, option){
    var c = new Chart(ctx, {
        type: type,
        data: {
            labels: label,
            datasets:[{
                data: data,
                backgroundColor: [
                    "#E8203A",
                    "#281CEB",
                    "#7DFFD4",
                    "#E8EB02",
                    "#FFA159"
                ]
            }]
        },
        options: option
    });
}

function barcharts(ctx, type, label, data, option){
    var c = new Chart(ctx, {
        type: type,
        data: {
            label: "Location",
            labels: label,
            datasets:[{
                backgroundColor: "#4e73df",
                hoverBackgroundColor: "#2e59d9",
                borderColor: "#4e73df",
                data: data
            }]
        },
        options: option
    });
}

window.onload = function () {
    doughnut_options = {cutoutPercentage: 70};

    bar_options = {
        
        layout: {
            padding: {
              left: 10,
              right: 25,
              top: 25,
              bottom: 0
            }
        },

        scales: {yAxes:[{
            
            ticks:{min:0, padding: 10},
            maxBarThickness: 25,

            gridLines: {
                display: false,
                drawBorder: false
            }

        }]}
    };


    var ctx1 = document.getElementById("myPieChart");
    charts(ctx1, 'doughnut', column, count, doughnut_options);

    var attraction = document.getElementById("attraction");
    barcharts(attraction, 'bar', attraction_label, attraction_data, bar_options);

    var travel = document.getElementById("travel");
    barcharts(travel, 'bar', travel_label, travel_data, {});

    var restaurant = document.getElementById("restaurant");
    barcharts(restaurant, 'bar', restaurant_label, restaurant_data, bar_options);

    var weather = document.getElementById("weather");
    barcharts(weather, 'bar', weather_label, weather_data, bar_options);

    var dust = document.getElementById("dust");
    barcharts(dust, 'bar', dust_label, dust_data, bar_options);
}