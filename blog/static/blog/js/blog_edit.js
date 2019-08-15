$(document).ready(function() {
    $('#summernote').summernote({
      height: 400,
      focus:true,
      callbacks:{
        onImageUpload: function(files, editor, welEditable){
          for(var i=files.length-1; i >=0 ; i--){
            sendFile(fiels[i], this);
          }
        }
      }
    });
  });

function sendFile(file, el){
  var form_data = new FormData();
  form_data.append('file',file);
  $.ajax({
    data:form_data,
    type:"POST",
    url:file_up_url,
    cache:false,
    enctype:'multipart/form-data',
    processData:false,
    success: function(url){
      alert(url)
      // $(el).summernote('editor.insertImage', url);
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