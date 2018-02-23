<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN" />

<xsl:template match="rss/channel">
  <html>
    <head>
      <title><xsl:value-of select="title" /> - RSSGen</title>
      <meta name="viewport" content="width=device-width, user-scalable=no" />
      <link rel="shortcut icon" href="../favicon.ico" />
      <style>
        body{
          font-size: 14px;
          max-width: 1100px;
          margin: 0 auto;
          padding: 0 1em;
          background-color: #FBE9E7;
          line-height: 1.5;
          color: #333;
          word-break:break-all;
        }
        a ,h1{
          text-decoration: none;
          color: #D84315;
          font-weight: bolder;
        }
        a:hover{
          color: #FF7043;
        }
        body>header{
          margin: 1em 0;
          padding: 2em .5em;
        }
        body>header h1{
          font-size: 4em;
          margin: 0;
        }
        body>header a{
          padding: 1em .2em;
        }
        body>footer{
          text-align: center;
          padding: 2em 0 4em;
        }
        section{
          background: white;
          padding: 3em;
          box-shadow: 0 0 5px rgba(0,0,0,.1);
          margin-bottom: 2.5em;
          padding-bottom: 5em;
        }
        section>header{
          font-size: 2em;
        }
        section>.time{
          color: #999;
          border-bottom: 1px solid #ccc;
          padding: .5em .3em;
          margin-bottom: 2em;
        }
        section>.content img{
          display: block;
          max-width: 100%;
        }
        @media (max-width:700px){
          section{
            padding: 1em;
            padding-bottom: 3em;
          }
        }
      </style>
    </head>
    <body>
      <header>
        <h1><xsl:value-of select="title" /></h1>
      </header>
      <xsl:apply-templates select="item" />
      <footer>
        <a target="_blank" href="{link}">Powered By Miaowm5</a>
      </footer>
    </body>
  </html>
</xsl:template>

<xsl:template match="item">
  <section>
    <header>
      <a href="{link}" target="_blank"><xsl:value-of select="title" /></a>
    </header>
    <div class="time">
      <xsl:value-of select="pubDate" />
    </div>
    <div class="content">
      <xsl:value-of select="description" disable-output-escaping="yes" />
    </div>
  </section>
</xsl:template>

</xsl:stylesheet>
