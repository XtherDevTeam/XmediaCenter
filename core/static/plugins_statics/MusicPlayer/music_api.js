function do_add_playlist(){
    name = prompt('Input playlist name')
    if(name == null) return;
    if(name == ""){
        alert('Failed with empty playlist name')
    }
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", '/api?action=music_api&request=create_playlist&name="'+name+'"', 0);
    xmlhttp.send();
    console.log(xmlhttp.responseText);
    var response = JSON.parse(xmlhttp.responseText)
    if(response["status"] == "error"){
        alert('Failed with ' + response['reason'])
    }
    //document.execCommand('Refresh')
}