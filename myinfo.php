
<form id="target" method="POST" action="/" enctype="multipart/form-data">
    {{ form.hidden_tag() }}
    <p>Enter the name of the output file <p>
    {{ form.name.label }} {{ form.name(size=20) }}<br>
    <p>Select video file which you would like to estimate <p>
    {{ form.file.label }} {{ form.file(size=20) }}<br>
    <br>
    {{ form.label }} {{ form.Ger(size=30) }}<br>
    <input type="submit" id="form-btn" value="Send"/><br>
    <br>
    <p>Below you can see the status of data processing and size of your file<p>
</form>

<p id="size"></p>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>


<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>

t = genID();

document.getElementById("name").pattern = '[a-zA-Z0-9]+';

document.getElementById("Ger").value = t;
document.getElementById('Ger').readOnly = true;
document.getElementById("Ger").type = "hidden";

document.getElementById("file").accept = "video/mp4,video/x-m4v,video/*";


Filevalidation = () => 
{
    const fi = document.getElementById('file');
    // Check if any file is selected.
    if (fi.files.length > 0) {
        for (const i = 0; i <= fi.files.length - 1; i++) {
 
            const fsize = fi.files.item(i).size;
            const file = Math.round(((fsize / 1024)/1024));
            // The size of the file.
            if (file >= 30) {
                alert(
                    "File too Big, please select a file less than 30mb");
                document.getElementById("file").value = "";
            } else {
                document.getElementById('size').innerHTML = '<b>'+ "Your file size: "
                + file + '</b> MB';
            }
        }
    }
}

var el = document.getElementById("file");
el.addEventListener("change", Filevalidation, false);

 $( "#form-btn" ).click( function() {
     state = t;
     setInterval(function() {load(state);}, 1000);


});


function genID() {
    return(String((new Date).getTime()));
}

function load(state) { 
     var xhttp = new XMLHttpRequest();
     xhttp.onreadystatechange = function() {
     if (this.readyState == 4 && this.status == 200) {
        document.getElementById("demo").innerHTML =
        this.responseText;
    }
    };

    xhttp.open("GET", "/status/"+state , true);
    xhttp.send();
 
    }


</script>

<div id="demo">

