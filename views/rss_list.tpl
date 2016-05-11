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
    </style>
  </head>
  <body>
    <div id="container">
      <ul>
        % for item in rss:
          <li>
            <a target="_blank" href="rss/{{item}}">{{item}}</a>
          </li>
        % end
      </ul>
    </div>
  </body>
</html>