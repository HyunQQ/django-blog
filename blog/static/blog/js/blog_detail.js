

$(document).ready(function () {
    $(".edit_comment textarea").attr('placeholder','댓글 입력');
    $(".edit_comment input").attr('placeholder','사용자 이름');
    
    var test = htmlDecode(post_text);
    $("#post_text").append(test);
}); 


