<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="tank@t34.me">
    <!-- CSS -->
    <link href="/media/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="/media/css/custom.css" rel="stylesheet">
  </head>

  <body>
    <div class="container-narrow">
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <li><a href="/about/">About</a></li>
          <!-- <li><a href="/api/">API</a></li>  -->
          <li><a href="https://github.com/z0rr0/t34.me">Sources on GitHub</a></li>
        </ul>
        <h3 class="muted"><a href="/">T-34</a></h3>
      </div>
      <hr>
      <div class="jumbotron">
        <h1>{{ header }}</h1>
        %include
      </div>
    </div>
  </body>
</html>
