
function removeMultiWhiteSpace(str) {
    return str.replace(/ +/g, " ");
}

function splitAllWords() {
    var str = $('#dekodeText').val();
    str = removeMultiWhiteSpace(str);
    str = str.replace(/ /g, "  ");
    $('#dekodeText').val(str);
}

//transforms the user entered markup into an array of array
function text2json(text) {
    // split text by magic delimiters 
    var json = [];
    var text = $('#dekodeText').val();
    var pars = text.split("\n");
    for (var par in pars){
        var words=pars[par].split("  ");
        parLine=[];
        for(var word in words){
            parLine.push(words[word]);
        }
        json.push(parLine);
    }
    return json;
}

//transforms the markup of the formated text into a visual preview
function json2html(json) {
    //transform to par-word-json
    var str="";
    var lastBool=false;
    for(var par in json){
        if(json[par].length==0){continue;}
        str+='<div class="par">';
        for(var w in json[par]){
            str+='<div class="w">'+json[par][w]+'</div>';
        }
        str+='</div>'
    }
    return str
}

//function used to get the dekoded words in dekoded.html 
function html2json() {
    //transform to par-word-json
    var str="";
    var lastBool=false;
    var pars = numpars["pars"];
    var par =0;
    var json=[]
    for(var p=1;p<=pars.length;p++){
        var par={}
        for (var w=1;w<=pars[p-1];w++) {
            par[$("#p"+p+"l"+w).html()]={"w":$("#p"+p+"w"+w).val()}
            if($("#p"+p+"e"+w).val())
                par[$("#p"+p+"l"+w).html()]["e"]=$("#p"+p+"e"+w).val();
        }
        json.push(par);
    }
    console.log(JSON.stringify(json))
    return json
}

//transforms the entered text
function showDekodeable() {
    var text = $('#dekodeText').val();
    var json = text2json(text);
    console.log(JSON.stringify(json))
    var html = json2html(json);
    document.getElementById("dekodeField").innerHTML=html;
}

//function to send dekoded text as AJAX
function postDekoded() {
    $('#save').click(function() {
        var json = html2json();
        $.ajax({
            url: '',
            data:JSON.stringify({"json":json}),
            contentType: 'application/json; charset=utf-8',  
            type: 'POST',
            success: function(response) {
                Materialize.toast('Formated text posted and saved.', 7000, 'rounded')
            },
            error: function(jqXHR, exception) {
                if (jqXHR.status === 0) {
                    alert('Not connect.\n Verify Network.');
                } else if (jqXHR.status == 404) {
                    alert('Requested page not found. [404]');
                } else if (jqXHR.status == 500) {
                    alert('Internal Server Error [500].');
                } else if (exception === 'parsererror') {
                    alert('Requested JSON parse failed.');
                } else if (exception === 'timeout') {
                    alert('Time out error.');
                } else if (exception === 'abort') {
                    alert('Ajax request aborted.');
                } else {
                    alert('Uncaught Error.\n' + jqXHR.responseText);
                }
            }
        });
    });
}