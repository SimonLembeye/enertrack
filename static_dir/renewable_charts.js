function renderChart(divId, data, labels) {
    let ctx = document.getElementById(divId).getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                data: data.sum,
                borderColor: 'rgba(0, 0, 0, 1)',
            },{
                data: data.solar,
                borderColor: 'rgba(255, 192, 0, 1)',
                backgroundColor: 'rgba(255, 192, 0, 0.2)',
            },{
                data: data.wind,
                borderColor: 'rgba(0, 192, 255, 1)',
                backgroundColor: 'rgba(0, 192, 255, 0.2)',
            }
            ]
        },
          options: {
            responsive: true,
              legend: { display: false },
            title: {
              display: false,
            },
            tooltips: {
              mode: 'index',
              intersect: true
            },
            annotation: {
              annotations: [{
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                value: 10600,
                borderColor: '#ffc107',
                borderWidth: 1,
                label: {
                  enabled: true,
                  content: 'Capacitées installées solaire',
                    fontSize: 8,
                    position: "left",
                    fontColor: "black",
                    xPadding: 1,
                    yPadding: 1,
                    backgroundColor: 'white',
                }
              },{
                type: 'line',
                mode: 'horizontal',
                scaleID: 'y-axis-0',
                value: 16500,
                borderColor: '#5b80b2',
                borderWidth: 1,
                label: {
                  enabled: true,
                  content: 'Capacitées installées éolien',
                    fontSize: 8,
                    position: "left",
                    fontColor: "black",
                    xPadding: 1,
                    yPadding: 1,
                    backgroundColor: 'white',
                }
              }, {
                  type: 'line',
                  mode: 'horizontal',
                  scaleID: 'y-axis-0',
                  value: 27100,
                  borderColor: 'black',
                  borderWidth: 1,
                  label: {
                      enabled: true,
                      content: 'Capacitées installées total enr',
                      fontSize: 8,
                      position: "left",
                      fontColor: "black",
                      xPadding: 1,
                      yPadding: 1,
                      backgroundColor: 'white',
                  }
              }]
            }
          }
        });
}

function renderProductionChart(data) {
    let ctx = document.getElementById("productionChart").getContext('2d');
    var myBarChart = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: ["Solaire", "Eolien"],
            datasets: [{
                backgroundColor: ["rgba(255, 192, 0, 0.2)", "rgba(0, 192, 255, 0.2)"],
                data: [data.solar_installed_capacities, data.wind_installed_capacities],
            },{
                backgroundColor: ["#ffc107", "#5b80b2"],
                data: [data.solar_last_production, data.wind_last_production],
            }],
        },
        options: {
            responsive: false,
            legend: { display: false },
            scales: {
                xAxes: [{
                    ticks: {
                        min: 0
                    },
                    stacked: false,
                    scaleLabel: {
                        display: true,
                        labelString: 'Production en GW'
                    }
                }],
                yAxes: [{
                    stacked: true,
                    barPercentage: 0.6,
                }]
            }
        }
    });
}


$(document).ready(
    function () {
        renderProductionChart(JSON.parse(prod_data));
        let data = JSON.parse(chart_data);
        let todayData = data.today_data;
        renderChart("todayChart", todayData.values, todayData.labels);
        let tmwData = data.tmw_data;
        renderChart("tmwChart", tmwData.values, tmwData.labels);
    }
);
