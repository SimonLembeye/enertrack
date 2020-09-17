function renderChart(divId, data, labels) {
    let ctx = document.getElementById(divId).getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                label: 'SUM',
                data: data.sum,
                borderColor: 'rgba(0, 0, 0, 1)',
            },{
                label: 'SOLAR',
                data: data.solar,
                borderColor: 'rgba(255, 192, 0, 1)',
                backgroundColor: 'rgba(255, 192, 0, 0.2)',
            },{
                label: 'WIND',
                data: data.wind,
                borderColor: 'rgba(0, 192, 255, 1)',
                backgroundColor: 'rgba(0, 192, 255, 0.2)',
            }
            ]
        },
    });
}

function renderProductionChart(data) {
    console.log('YES')
    let ctx = document.getElementById("productionChart").getContext('2d');
    var myBarChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: ["Solaire", "Eolien"],
            datasets: [{
                backgroundColor: ["rgba(255, 192, 0, 0.2)", "rgba(0, 192, 255, 0.2)"],
                data: [50.56, 34.32],
            },{
                backgroundColor: ["#ffc107", "#5b80b2"],
                data: [20, 10],
            }],
        },
        options: {
            legend: { display: false },
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0
                    },
                    staked: false
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });
}


$(document).ready(
    function () {
        renderProductionChart("DD");
        let data = JSON.parse(chart_data);
        let todayData = data.today_data;
        renderChart("todayChart", todayData.values, todayData.labels);
        let tmwData = data.tmw_data;
        renderChart("tmwChart", tmwData.values, tmwData.labels);
    }
);