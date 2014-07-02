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

var fs_access_token = document.cookie
function isLoggedIn() {}
function getAccessToken() {
    var fs_auth_code = QueryString.code
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
        }
    })
}

function logIn() {
    window.location = 'https://sandbox.familysearch.org/cis-web/oauth2/v3/authorization?redirect_uri=http://localhost:3000/select-person&response_type=code&client_id=WCQY-7J1Q-GKVV-7DNM-SQ5M-9Q5H-JX3H-CMJK'
}
console.log('hi')
$(document).ready(function() {
    $('#authenticate').click(logIn)
    getAccessToken()
})
