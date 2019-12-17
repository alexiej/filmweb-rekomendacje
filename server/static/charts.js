
function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function getRandomColor(n) {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    var colors = [];
    for(var j = 0; j < n; j++){
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        colors.push(color);
        color = '#';
    }
    return colors;
}

var ctx = document.getElementById('pieChart');
var pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: Object.keys(pie),
         datasets: [{
            label: '# of Votes',
            data:  Object.values(pie),
            backgroundColor: getRandomColor( Object.values(pie).length)
         }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

var flw = document.getElementById('flowChart');
var flowChart = new Chart(flw, {
    type: 'line',
    data: {
        labels: Object.values(flow['Data']),
        datasets: [{
            label: 'Filmweb',
            data:  Object.values(flow['Ocena']),
            backgroundColor: '#FF0000',
            borderWidth: 0,
            tension: 0,
            fill: false
        },{
            label: 'IMDb',
            data:  Object.values(flow['averageRating']),
            backgroundColor: '#0000FF',
            borderWidth: 0,
            tension: 0,
            fill: false
        },{
            label: 'Rating difference',
            data:  Object.values(flow['diff']),
            backgroundColor: '#00FF00',
            borderWidth: 0,
            tension: 0,
            fill: false
        }]
    },
    options: {
        title: {
            text: 'SCORE FLOW',
            display: true
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    min: -10,
                    max: 10,
                    stepSize: 1
                },
                gridLines: {
                    zeroLineWidth: 3
                }
            }]
        },
        layout: {
            padding: 40
        },
        elements:{
            point: {
                radius:2,
                pointStyle: 'circle'
            }
        }
    }
});

var rdr = document.getElementById('radarChart');
var radarChart = new Chart(rdr, {
    type: 'radar',
    data: {
        labels: Object.keys(radar['fw']),
        datasets: [{
            label: 'Filmweb',
            data:  Object.values(radar['fw']),
            borderColor: '#FF0000',
            backgroundColor: 'rgba(255, 0, 0, 0.5)',
            borderWidth: 2,
            fill: true
        },{
            label: 'IMDb',
            data:  Object.values(radar['imdb']),
            borderColor: '#0000FF',
            backgroundColor: 'rgba(0, 0, 255, 0.5);',
            borderWidth: 2,
            fill: true
        }]
    },
    options: {
        title: {
            text: 'SCORE RADAR',
            display: true
        }
    }
});

var dsh = document.getElementById('Dashboard');
var Dashboard = new Chart(dsh, {
     type: 'radar',
    data: {
        labels: Object.keys(radar['fw']),
        datasets: [{
            label: 'Filmweb',
            data:  Object.values(radar['fw']),
            borderColor: '#FF0000',
            backgroundColor: 'rgba(255, 0, 0, 0.5)',
            borderWidth: 2,
            fill: true
        },{
            label: 'IMDb',
            data:  Object.values(radar['imdb']),
            borderColor: '#0000FF',
            backgroundColor: 'rgba(0, 0, 255, 0.5);',
            borderWidth: 2,
            fill: true
        }]
    },
    options: {
        title: {
            text: 'Dashboard',
            display: true
        }
    }
});