<p class="lead">You can copy this short link.</p>
<h3>
  <a href="{{ var }}" target="_blank" class="shorturl">{{ var }}</a>
</h3>
<p>
  <a href="/" class="btn btn-success">Add new link</a>
</p>
<p>
	<img src="/qrcode/{{ dirty }}" alt="QR Code">
</p>
% rebase('layout.tpl', title='T-34')
