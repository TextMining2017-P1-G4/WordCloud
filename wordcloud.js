function submitWordCloud() {
    var keyword_input = $('#keyword_input').val();
    var select_input = $('#select_input').val();
    if (keyword_input.length == 0) {
        // Do nothing
    } else {
        getWordCloud(keyword_input, select_input);
    }
}

function getWordCloud(keyword_input, select_input) {
    var url =  '/get_word_cloud?' + 'keyword=' + keyword_input + '&select=' + select_input;
    console.log(url);
    $.ajax({
        type: 'GET',
        url: url,
        success: function(json_str) {
            var list = JSON.parse(json_str);
            WordCloud(document.getElementById('canvas'), {
                list: list,
                gridSize: 12,
                weightFactor: 20,
                click: function(item) {
                    //alert(item[0] + ': ' + item[1]);
                    getWordCloud(item[0]);
                },
                //fontFamily: 'Finger Paint, cursive, sans-serif',
            });
        }
    });
}

$("#keyword_input").keyup(function(event){
    if(event.keyCode == 13){
        submitWordCloud();
    }
});