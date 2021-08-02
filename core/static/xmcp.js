var session = '';

function login(username, password) {
    password = hex_md5(password + '_EksXmediaCenter_User'); // it's magic, do not care much about it
    to_process = username + ":" + password;
    to_process = btoa(to_process);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", '/api?(action="login",userinfo="' + to_process + '")', 0);
    xmlhttp.send();
    console.log(xmlhttp.responseText);
    if (xmlhttp.responseText != '') {
        return xmlhttp.responseText;
    }
    return xmlhttp.responseText;
}

function getfilelist(path){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", '/api?(action="getfilelist",user_sid="' + session + '")', 0);
    xmlhttp.send();
    console.log(xmlhttp.responseText);
    if (xmlhttp.responseText != '') {
        return xmlhttp.responseText;
    }
    return xmlhttp.responseText;
}

function parseJSON(event, js) {
    json = JSON.parse(js);
    if (event == 'on.login') {
        if (json['status'] == 'success') {
            session = json['user_sid'];
            return session;
        } else {
            return 'failed.' + String(json['errno']);
        }
    } else if (event == 'on.filelist.get') {
        if (json['status'] == 'success') {
            return json['list'];
        } else {
            return 'failed.' + String(json['errno']);
        }
    }
}