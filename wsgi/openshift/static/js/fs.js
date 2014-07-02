var QueryString = function () {
    // This function is anonymous, is executed immediately and 
    // the return value is assigned to QueryString!
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        // If first entry with this name
        if (typeof query_string[pair[0]] === "undefined") {
            query_string[pair[0]] = pair[1];
        // If second entry with this name
        } else if (typeof query_string[pair[0]] === "string") {
            var arr = [ query_string[pair[0]], pair[1] ];
            query_string[pair[0]] = arr;
        // If third or later entry with this name
        } else {
            query_string[pair[0]].push(pair[1]);
        }
    } 
    return query_string;
} ();

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function isLoggedIn() {
    fs_access_token = getCookie('fs_access_token')
    console.log('ili')
    $.ajax({
        type: 'GET',
        url: 'https://sandbox.familysearch.org/platform/users/current',
        headers: {'Authorization': 'Bearer ' + fs_access_token},
        success: function(result) {
            console.log(result)
            return true
        }
    })
}

function getAccessToken() {
    var fs_auth_code = QueryString.code
    if (typeof(fs_auth_code) !== 'undefined') {
        $.ajax({
            url: "https://sandbox.familysearch.org/cis-web/oauth2/v3/token",
            data: {
                grant_type:'authorization_code',
                code: fs_auth_code,
                client_id: 'WCQY-7J1Q-GKVV-7DNM-SQ5M-9Q5H-JX3H-CMJK'
            },
            type: 'POST',
            success: function(result) {
                console.log(result)
                document.cookie = 'fs_access_token=' + result.access_token
                console.log(getCookie('fs_access_token'))
            },
            fail: function() {
                console.log('failed')
            }
        })
    }
}

function logIn() {
    window.location = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/authorization?redirect_uri=http://localhost:3000/select-person&response_type=code&client_id=WCQY-7J1Q-GKVV-7DNM-SQ5M-9Q5H-JX3H-CMJK'
}
console.log('hi')
$(document).ready(function() {
    $('#authenticate').click(logIn)
    if (!isLoggedIn()) {
        console.log('not logged in')
        getAccessToken()
    } else {
        console.log('logged in')
        getAccessToken()
    }
})
