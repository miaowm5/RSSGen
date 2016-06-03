<!DOCTYPE HTML>
<html>
  <head>
    <title>List</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, user-scalable=no" />
    <link rel="shortcut icon" href="static/favicon.ico">
    <link rel="stylesheet" href="static/style.css">
  </head>
  <body>
    <div id="container">
      <div class="list">
        % for item in rss:
          <div>
            <a class="link" target="_blank" href="rss/{{item}}">{{item}}</a>
            <a class="handle" target="_blank" href="rss/save?type=rss&recipe={{item}}">立刻更新</a>
          </div>
        % end
        % for item in orss:
          <div>
            <a class="link" target="_blank" href="rss/ol-{{item}}">[Online] {{item}}</a>
            <a class="handle" target="_blank" href="rss/save?type=orss&recipe={{item}}">立刻更新</a>
            <!-- <a class="handle delete" href="javascript:void(0)" data-name="{{item}}">删除</a> -->
          </div>
        % end
      </div>
    </div>
  </body>
</html>