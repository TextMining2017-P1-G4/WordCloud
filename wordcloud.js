function submitWordCloud() {
    var keyword_input = $('#keyword_input').val();
    if (keyword_input.length == 0) {
        // Do nothing
    } else {
        getWordCloud(keyword_input);
    }
}

function getWordCloud(keyword_input) {
    $.ajax({
        type: 'GET',
        url: '/get_word_cloud?' + keyword_input,
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

