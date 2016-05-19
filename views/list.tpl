<!DOCTYPE HTML>
<html>
  <head>
    <title>List</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="static/style.css">
  </head>
  <body>
    <div id="container">
      <img src="" style="display:none" id='remove'>
      <div class="list">
        % for item in items:
          <div>
            <a class="link" target="_blank" href="{{item[0]}}">{{item[1]}}</a>
            <p class="handle" data-url="list/delete?id={{item[2]}}">删除</p>
          </div>
        % end
      </div>
    </div>
    <script src="//cdn.bootcss.com/jquery/1.11.2/jquery.min.js"></script>
    <script type="text/javascript">
      !window.jQuery && document.write('<script src="static/jquery.js"><\/script>');
    </script>
    <script>
      (function (){
        $('.handle').click(function(){
          $('#remove').attr('src', $(this).attr('data-url'))
          $(this).parent().hide()
        })
      })()
    </script>
  </body>
</html>