<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="short urls">
    <meta name="author" content="tank@t34.me">
    <!-- CSS -->
    <link href="/media/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=PT+Sans+Caption:400,700' rel='stylesheet' type='text/css'>
    <link href="/media/css/custom.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <!-- <li><a href="/api/">API</a></li>  -->
          <li><a href="https://github.com/z0rr0/t34.me">Sources on GitHub</a></li>
        </ul>
        <h3 class="text-muted"><a href="/">T-34</a></h3>
      </div>
      <hr>
      <div class="jumbotron">
        <h1>{{ header }}</h1>
        {{ !base }}
      </div>
    </div>
  </body>
</html>
