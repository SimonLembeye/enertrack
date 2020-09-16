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

$(document).ready(
    function () {
        let data = JSON.parse(chart_data);
        let todayData = data.today_data;
        renderChart("todayChart", todayData.values, todayData.labels);
        let tmwData = data.tmw_data;
        renderChart("tmwChart", tmwData.values, tmwData.labels);
    }
);