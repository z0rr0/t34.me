<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title or 'No title' }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="short urls">
    <meta name="author" content="tank@t34.me">
    <!-- CSS -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=PT+Sans+Caption:400,700' rel='stylesheet' type='text/css'>
    <link href="/media/css/custom.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
      <div class="header">
        <ul class="nav nav-pills pull-right">
          <li><a href="/about/">About project</a></li>
          <!-- <li><a href="/api/">API</a></li>  -->
          <li><a href="https://github.com/z0rr0/t34.me">Sources on GitHub</a></li>
        </ul>
        <h3 class="text-muted">T-34</h3>
      </div>
      <hr>
      <div class="jumbotron">
        <h1>Easy and fast!</h1>
        {{ !base }}
      </div>
      <div class="row marketing">
        <div class="col-xs-6">
          <h4>Why</h4>
          <p>Sometimes addresses of interesting web pages are long. But you want to send them to your friends (email, sms, etc.) or use some other way. Then <strong>t34.me</strong> will help you.</p>
        </div>
        <div class="col-xs-6">
          <h4>Rules</h4>
          <p>
            You can't use this service for:
          </p>
          <ul>
            <li>promotional mailings</li>
            <li>spam mailing</li>
            <li>the dissemination of malicious programs</li>
            <li>fraudulent or illegal activities</li>
          </ul>
        </div>
      </div>
    </div>
    <!-- API
    <a href="javascript:location.href='https://t34.me/api/?web=1&u='+encodeURIComponent(location.href)">bookmark</a>
     -->
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
  </body>
</html>
