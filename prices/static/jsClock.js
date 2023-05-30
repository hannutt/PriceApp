//globaalin muuttujan alustus, riittää että muuttuja alustetaan
//funktioiden ulkopuolella. 
var currentTime = ''
var sound = new Audio()
//tallennetaan valitun tiedoston polku+nimi muuttujaan
var fullName = document.getElementById('fullName').value

function song() {
    track = URL.createObjectURL(document.getElementsByTagName('sel')[0].files[0]);
    console.log(track)
}

setInterval(showTime, 1000);
function showTime() {
    let time = new Date();
    let hour = time.getHours();
    let min = time.getMinutes();
    //let sec = time.getSeconds();
   
 
    hour = hour < 10 ? "0" + hour : hour;
    min = min < 10 ? "0" + min : min;
    //sec = sec < 10 ? "0" + sec : sec;
 
    currentTime = hour + ":"
            + min // ":"+ sec
 
    document.getElementById("clock")
            .innerHTML = currentTime;
}
showTime()



/*
function createStopBtn() {
    var Div = document.getElementById('stopBtnDiv')
    var stopBtn = document.createElement('button')
    
    var text = document.createTextNode('Stop')
    stopBtn.appendChild(text)
    Div.appendChild(stopBtn)
    //onclick eventin luonti fuktiolla luodulle painikkeelle
    function stopAlarm() {
        sound.pause()
        
    }
    stopBtn.addEventListener('click',stopAlarm)
    
    
} */

function stopAlarm() {
    sound.pause()
}


function setAlarm()
{
    
    var hrs = document.getElementById("hours").value
    var mins = document.getElementById("minutes").value
    var final = hrs+":"+mins
    
    

    //niin kauan kuin kellonaika ja asetettu aika ovat eri, kutsutaan showtime funktiota, eli kello
    //toimii normaalisti
    while (currentTime != final)
    {
        showTime()
    }
    //kun asetettu aika on sama kuin nykyinen aika, tulostetaan herätysiloitus
    if (currentTime == final)
    {
        
        alert(fullName)
       // sound.play(fullName)
        
    }
}

/*
function selFile() {
    var sound2 = new Audio()
    var input =document.createElement('input')
    input.type='file'
    
    input.onchange = _this => {
        var files = Array.from(input.files)
        console.log(files)
        sound2.play('/static/'+files)
        
    }
    input.click()
}*/

