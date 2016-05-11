<!DOCTYPE HTML>
<html>
  <head>
    <title>List</title>
    <style>
      #container{ margin: 3em auto; width: 960px; border: 1px solid #999; border-radius: 10px; }
      ul{ padding: 1em 2em; }
      li{
        font-size: 1.5em; font-family: '微软雅黑'; text-decoration: none;
        display: block; padding: .8em; border-radius: 10px;
      }
      li:nth-child(2n+0){ background: #EEE; }
      a{ text-decoration: none; color: #333; }
      .delete{ cursor: pointer; display: inline; color: #999; font-size: 0.7em; margin-left: 1em; }
      .delete:before{ content: ' - '; }
    </style>
  </head>
  <body>
    <div id="container">
      <img src="" style="display:none" id='remove'>
      <ul>
        % for item in items:
          <li>
            <a target="_blank" href="{{item[0]}}">{{item[1]}}</a>
            <p class="delete" href="#" data-url="list/delete?id={{item[2]}}">删除</p>
          </li>
        % end
      </ul>
    </div>
    <script src="//cdn.bootcss.com/jquery/1.11.2/jquery.min.js"></script>
    <script type="text/javascript">
      !window.jQuery && document.write('<script src="static/jquery.js"><\/script>');
    </script>
    <script>
      (function (){
        $('.delete').click(function(){
          $('#remove').attr('src', $(this).attr('data-url'))
          $(this).parent().hide()
        })
      })()
    </script>
  </body>
</html>