$(document).ready(function() {
    $('#summernote').summernote({
      height: 400,
      focus:true,
      callbacks:{
        onImageUpload: function(files, editor, welEditable){
          for(var i=files.length-1; i >=0 ; i--){
            sendFile(files[i], this);
          }
        }
      }
    });
  });

function sendFile(file, el){
  
  var form_data = new FormData();
  form_data.append('file',file);
  $.ajax({
    headers: {"X-CSRFToken":csrf_token},
    data:form_data,
    type:"POST",
    url:file_up_url,
    cache:false,
    contentType:false,
    enctype:'multipart/form-data',
    processData:false,
    success: function(url){
      file = "/media/"+url;
      $(el).summernote('editor.insertImage', file);
    }
  })


}


  // 글 수정 및 저장
  // function edit(){
  //   $('#summernote').summernote({focus: true});
  // };

  // function save(){
  //   var markup = $('#summernote').summernote('code');
  //   $('#summernote').summernote('destroy');
  // };