// ------------------------------------------------------------------------------------
// Widget Pie Chart 
var randomScalingFactor = function() {
    return Math.round(Math.random() * 100);
};

var config1 = {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [
                randomScalingFactor(),
                randomScalingFactor()
            ],
            backgroundColor: [
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 0.3)',
            ],
            hoverBackgroundColor: [
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 0.3)',
            ],
            borderWidth: [
                0, 0
            ],
            label: 'Dataset 1'
        }],
        labels: [
            "Done",
            "Undone"
        ]
    },
    options: {
        responsive: true,
        legend: false,
        cutoutPercentage: 60,
        title: {
            display: false,
        },
        animation: {
            animateScale: true,
            animateRotate: true,
            easing: 'easeOutQuint',
        },
        tooltips: {
            mode: 'index',
            intersect: true,
            position: 'average',
            backgroundColor: 'rgba(0,0,0,.4)',
            titleFontFamily: 'Helvetica Neue',
            cornerRadius: 3,


            custom: function(tooltip) {
                if (!tooltip) return;
                // disable displaying the color box;
                tooltip.displayColors = false;
            },




        },
    }
};
var config2 = {
    type: 'doughnut',
    data: {
        datasets: [{
            data: [
                randomScalingFactor(),
                randomScalingFactor(),
                randomScalingFactor(),
            ],
            backgroundColor: [
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 0.7)',
                'rgba(255, 255, 255, 0.3)',
            ],
            hoverBackgroundColor: [
                'rgba(255, 255, 255, 1)',
                'rgba(255, 255, 255, 0.7)',
                'rgba(255, 255, 255, 0.3)',
            ],
            borderWidth: [
                0, 0, 0
            ],
            label: 'Dataset 1'
        }],
        labels: [
            "Gold",
            "Silver",
            "Bronze",
        ]
    },
    options: {
        responsive: true,
        legend: false,
        cutoutPercentage: 60,
        title: {
            display: false,
        },
        animation: {
            animateScale: true,
            animateRotate: true,
            easing: 'easeOutQuint',
        },
        tooltips: {
            mode: 'index',
            intersect: true,
            position: 'average',
            backgroundColor: 'rgba(0,0,0,.4)',
            titleFontFamily: 'Helvetica Neue',
            cornerRadius: 2,


            custom: function(tooltip) {
                if (!tooltip) return;
                // disable displaying the color box;
                tooltip.displayColors = false;
            },




        },
    }
};




setTimeout(function() {
    var ctx1 = document.getElementById("chart-area1").getContext("2d");
    window.myDoughnut1 = new Chart(ctx1, config1);

}, 1300);

setTimeout(function() {
    var ctx2 = document.getElementById("chart-area2").getContext("2d");
    window.myDoughnut2 = new Chart(ctx2, config2);

}, 1500);


// ------------------------------------------------------------------------------------
// Widget Line Chart 


var chart = document.getElementById('lineChart').getContext('2d');
//     gradient = chart.createLinearGradient(0, 0, 0, 550),
//     gradient2 = chart.createLinearGradient(0, 0, 0, 550);
//     gradient3 = chart.createLinearGradient(0, 0, 0, 550);    


// gradient.addColorStop(0, 'rgba(78, 214,226, 0.5)');
// gradient.addColorStop(0.5, 'rgba(78, 214,226, 0.25)');
// gradient.addColorStop(.9, 'rgba(78, 214,226, 0)');

// gradient2.addColorStop(0, 'rgba(73, 178, 227, 0.5)');
// gradient2.addColorStop(0.5, 'rgba(73, 178, 227, 0.25)');
// gradient2.addColorStop(.9, 'rgba(73, 178, 227, 0)');

// gradient3.addColorStop(0, 'rgba(255 , 204 , 0 , 0.5)');
// gradient3.addColorStop(0.5, 'rgba(255 , 204 , 0 , 0.25)');
// gradient3.addColorStop(.9, 'rgba(255 , 204 , 0 , 0)');


var data = {


    labels: ['Jan ', 'Feb ', 'March', 'Apr', 'May', 'Jun', 'Jul ', 'Aug ', 'Sep', 'Oct', 'Nov', 'Dec'],

    datasets: [{
            label: 'Task Type 1',
            backgroundColor: 'rgba( 73, 178, 227, .01)',
            pointBackgroundColor: 'rgba( 73, 178, 227, 0)',
            pointBorderColor: 'rgba( 73, 178, 227, 0)',
            pointRadius: 10,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba( 73, 178, 227, .5)',
            pointHoverBorderColor: 'rgba( 73, 178, 227, .0)',
            borderWidth: 1,
            borderColor: 'rgba( 73, 178, 227, 1)',
            data: [1, .5, 2, .3, 1.5, 3, 2.25, 5, 3.5, 4, 3, .5],
            hidden: false,

        },
        {
            label: 'Task Type 2',
            backgroundColor: 'rgba( 235, 112, 100, .01) ',
            pointBackgroundColor: 'rgba( 235, 112, 100, 0) ',
            pointBorderColor: 'rgba( 73, 178, 227, 0)',
            pointRadius: 10,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba( 235, 112, 100, .5)',
            pointHoverBorderColor: 'rgba( 235, 112, 100, 0)',
            borderWidth: 1,
            borderColor: 'rgba( 235, 112, 100, 1)',
            data: [3, 6, 2, .1, 6, 1, 10, 1, 4, 2.5, 8, 6],
            hidden: false,

        },
        {
            label: 'Task Type 3',
            backgroundColor: 'rgba( 255 , 204 , 0 , .01 )',
            pointBackgroundColor: 'rgba( 255 , 204 , 0 , 0 )',
            pointBorderColor: 'rgba( 73, 178, 227, 0)',
            pointRadius: 10,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba( 255 , 204 , 0 , .5 )',
            pointHoverBorderColor: 'rgba( 255 , 204 , 0 , 0 )',
            borderWidth: 1,
            borderColor: 'rgba( 255 , 204 , 0 , 1 )',
            data: [8, 5, 10, 3, 15, 6, 5, 11, 7, 10, 30, 9],
            hidden: false,

        },


    ]
};


var options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        easing: 'easeOutExpo',
        duration: 5000,
    },
    scales: {
        xAxes: [{
            gridLines: {
                color: 'rgba(223,232,241,.5)',
                lineWidth: .5,
                drawTicks: false,
                zeroLineWidth: 1,

            },
            ticks: {
                fontColor: 'rgba(168, 176, 185, .7)',
                padding: 20

            },
        }],
        yAxes: [{
            gridLines: {
                color: 'rgba(223,232,241,.5)',
                lineWidth: .5,
                drawTicks: false,
                zeroLineWidth: 0



            },
            ticks: {
                fontColor: 'rgba(168, 176, 185, .7)',
                padding: 10
            },
        }]
    },
    elements: {
        line: {
            tension: 0.4
        }
    },
    legend: {
        display: false
    },
    point: {},
    tooltips: {
        mode: 'index',
        intersect: true,
        position: 'average',
        backgroundColor: 'rgba(0,0,0,.4)',
        titleFontFamily: 'Open Sans',
        cornerRadius: 2,


        custom: function(tooltip) {
            if (!tooltip) return;
            // disable displaying the color box;
            tooltip.displayColors = false;
        },
    },
    layout: {
        padding: {
            left: 15,
            right: 40,
            top: 40,
            bottom: 40
        }
    },


};


var chartInstance = new Chart(chart, {
    type: 'line',
    data: data,
    options: options
});


$(document).on('change', '.chart-legend', function() {
    var index = parseInt($(this).attr('chart-dataset'));
    chartInstance.data.datasets[index].hidden = !this.checked;
    chartInstance.update();
});