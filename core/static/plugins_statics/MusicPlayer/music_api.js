function do_add_playlist(){
    var name = prompt('Input playlist name')
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

function do_import(path){
    if(path == null){
        alert('Canceled.')
        return;
    }
    var pname = prompt('Input playlist name:')
    if(path == null){
        alert('Canceled.')
        return;
    }

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET','/api?action=music_api&request=get_playlist_id&name=' + pname,0);
    xmlhttp.send()
    var result = JSON.parse(xmlhttp.responseText);
    if(result['status'] == 'error'){
        alert('Failed with ' + result['reason']);
        return;
    }
    var pid = result['id'];

    xmlhttp = new XMLHttpRequest();
    xmlhttp.open('GET','/api?action=music_api&request=add_song&pid=' + String(pid) + '&path=' + path,0);
    xmlhttp.send();
    result = JSON.parse(xmlhttp.responseText);
    if(result['status'] == 'error'){
        alert('Failed with ' + result['reason']);
        return;
    }
}