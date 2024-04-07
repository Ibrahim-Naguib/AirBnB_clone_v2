# script that sets up the web servers for the deployment of web_static
package { 'nginx':
  ensure  => installed,
}

exec { 'install_nginx':
  command => 'sudo apt-get update ; sudo apt-get -y install nginx',
  path    => '/usr/bin:/bin',
}

file { '/data/web_static/shared/':
  ensure => directory,
}

file { '/data/web_static/releases/test/':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

exec { 'sudo chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

exec { 'echo':
  path    => '/usr/bin:/bin',
  command => "echo 'server { listen 80; listen [::]:80 default_server; add_header X-Served-By ${HOSTNAME}; root /var/www/html; index index.html index.htm index.nginx-debian.html; server_name _; location /hbnb_static { alias /data/web_static/current; index index.html index.htm; } location /redirect_me { return 301  https://www.youtube.com/watch?v=QH2-TGUlwu4; } error_page 404 /404.html; location /404.html { root /var/www/html; internal; } }' | sudo tee /etc/nginx/sites-available/default"
}

service { 'nginx':
  ensure  => running,
}
