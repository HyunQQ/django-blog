$(document).ready(function() {
    $('#summernote').summernote();
  });

  function edit(){
    $('.click2edit').summernote({focus: true});
  };

  function save(){
    var markup = $('.click2edit').summernote('code');
    $('.click2edit').summernote('destroy');
  };