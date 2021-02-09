let light = document.getElementById("Light")
let ambient = document.getElementById("Ambient")
let onboard = document.getElementById("onboard")
let humidity = document.getElementById("humidity")
let pressure = document.getElementById("pressure")
let motion = document.getElementById("motion")

let onehour = document.getElementById("1 hour")
let threehours = document.getElementById("3 hours")
let sevenhours = document.getElementById("7 hours")

let interval = {'days':0, 'hours':3, 'minutes':0}

onehour.addEventListener('click', function () {
    interval = {'days':0, 'hours':1 , 'minutes':0}
    liveUpdate()
})

threehours.addEventListener('click', function () {
    interval = {'days':0, 'hours':3 , 'minutes':0}
    liveUpdate()
})

sevenhours.addEventListener('click', function () {
    interval = {'days':0, 'hours':7 , 'minutes':0}
    liveUpdate()
})

let pressuretoplot = []
let temptoplot = []
let humiditytoplot = []
let time = []

let updateInterval = 1000


function liveUpdate () {

        fetch('/sensor_update',{
            method: 'POST',
            body:JSON.stringify(interval),
            headers:{
                'Content-Type':'application/json'
            }
        }).then(function (response){
            return response.json();
        }).then(function (data){
            let readings = data
            // light.innerHTML = `Light intensity = ${readings.lux} lux`
            // ambient.innerHTML = `Ambient temperature = ${readings.ambient_temp} ˚C`
            // onboard.innerHTML = `On_board temperature = ${readings.on_board_temp} ˚C`
            // humidity.innerHTML = `Humidity  = ${readings.humidity} %`
            // pressure.innerHTML = `Pressure = ${readings.pressure} Pascal`
            // if (readings.motion == true){
            //     motion.innerHTML = "Someone is in the room"
            // }
            // else {
            //     motion.innerHTML = "The room is empty"
            // }
            //

            pressuretoplot = []
            time = []

            for (i of readings){
                pressuretoplot.push(i.pressure)
                time.push(i.timestamp.split('2021')[1].split('GMT')[0].trim().slice(0,5))
            }
            // pressuretoplot.push(readings.pressure)

            console.log(pressuretoplot)
            console.log(i.timestamp.split('2021')[1].split('GMT')[0].trim().slice(0,5))

            // temptoplot.push(readings.ambient_temp)
            // if (temptoplot.length > 25) {
            //     temptoplot.shift()
            // }
            // humiditytoplot.push(readings.humidity)
            // if (humiditytoplot.length > 25) {
            //     humiditytoplot.shift()
            // }
            return readings
        }).catch(function (error){
            console.log(error)
        })
}

document.addEventListener('DOMContentLoaded', function(){
    liveUpdate();
})

var ctx_pressure = document.getElementById('my pressure Chart').getContext('2d');
// var ctx_temp = document.getElementById('my temp Chart').getContext('2d');
// var ctx_humid = document.getElementById('my humidity Chart').getContext('2d');

function livePlot() {
    setInterval(function (){
        var chart = new Chart(ctx_pressure, {
            type: 'line',
            data: {
                labels: time,
                datasets: [{
                    label: 'Pressure',
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: pressuretoplot
                }]
            },
            options: {
                responsive: true,
                elements: {
                    point:{
                        radius: 0
                    }
                },
                scales: {
                    xAxes: [{
                        display: true,
                        labelString: "Time (hours)"
                    }],
                    yAxes: [{
                        display: true,
                        labelString: "Atmospheric Pressure (Pascal)"
                    }]
                },
                animation: {
                    duration: 0
                }
            }
        });
},updateInterval);
}


// function livePlotTemp() {
//     setInterval(function (){
//         var chart = new Chart(ctx_temp , {
//             type: 'line',
//             data: {
//                 labels: temptoplot,
//                 datasets: [{
//                     label: 'Ambient temperature',
//                     backgroundColor: 'rgb(87, 160, 230)',
//                     borderColor: 'rgb(87, 160, 230)',
//                     data: temptoplot
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 elements: {
//                     point:{
//                         radius: 0
//                     }
//                 },
//                 scales: {
//                     xAxes: [{
//                         display: false
//                     }],
//                     yAxes: [{
//                         display: true,
//                     }]
//                 },
//                 animation: {
//                     duration: 0
//                 }
//             }
//         });
//     },updateInterval);
// }
//
// function livePlotHumid() {
//     setInterval(function (){
//         var chart = new Chart(ctx_humid , {
//             type: 'line',
//             data: {
//                 labels: humiditytoplot,
//                 datasets: [{
//                     label: 'Humidity',
//                     backgroundColor: 'rgb(109, 190, 191)',
//                     borderColor: 'rgb(109, 190, 191)',
//                     data: humiditytoplot
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 elements: {
//                     point:{
//                         radius: 0
//                     }
//                 },
//                 scales: {
//                     xAxes: [{
//                         display: false
//                     }],
//                     yAxes: [{
//                         display: true,
//                     }]
//                 },
//                 animation: {
//                     duration: 0
//                 }
//             }
//         });
//     },updateInterval);
// }


document.addEventListener('DOMContentLoaded', function(){
    livePlot();
})

// document.addEventListener('DOMContentLoaded', function(){
//     livePlotTemp();
// })
//
// document.addEventListener('DOMContentLoaded', function(){
//     livePlotHumid();
// })





