let light = document.getElementById("Light")
let ambient = document.getElementById("Ambient")
let onboard = document.getElementById("onboard")
let humidity = document.getElementById("humidity")
let pressure = document.getElementById("pressure")
let motion = document.getElementById("motion")

function liveUpdate () {

    setInterval(function (){
        fetch('/sensor_update',{
            method: 'POST'
        }).then(function (response){
            return response.json();
        }).then(function (data){
            console.log(data)
            let readings = data
            light.innerHTML = `Light intensity = ${readings.lux} lux`
            ambient.innerHTML = `Ambient temperature = ${readings.ambient_temp} ˚C`
            onboard.innerHTML = `On_board temperature = ${readings.on_board_temp} ˚C`
            humidity.innerHTML = `Humidity  = ${readings.humidity} %`
            pressure.innerHTML = `Pressure = ${readings.pressure} Pascal`
            if (readings.motion == true){
                motion.innerHTML = "Someone is in the room"
            }
            else {
                motion.innerHTML = "The room is empty"
            }
            return readings
        }).catch(function (error){
            console.log(error)
        })
    },2000);
}

document.addEventListener('DOMContentLoaded', function(){
    liveUpdate();
})

