# Configures a web server for deployment of web_static.

# Nginx configuration file
$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${HOSTNAME};
    root   /var/www/html;
    index  index.html index.htm;
    location /hbnb_static {
        alias /data/web_static/current/;
    }
    location /redirect_me {
        return 301 https://github.com/AhmadYousif89;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
}

-> file { '/data':
  ensure  => 'directory',
}

-> file { '/data/web_static':
  ensure => 'directory',
}

-> file { '/data/web_static/releases':
  ensure => 'directory',
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory',
}

-> file { '/data/web_static/shared':
  ensure => 'directory',
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => "Test page\n",
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

-> exec { 'chown -hR ubuntu:ubuntu /data/':
  path => '/bin/:/usr/bin/:/usr/local/bin/',
}

-> file { '/var/www/html/index.html':
  ensure  => 'file',
  content => "Welcome page 👋\n",
}

-> file { '/var/www/html/404.html':
  ensure  => 'file',
  content => "Page Not Found!\n",
}

-> file { '/etc/nginx/sites-enabled/default':
  ensure  => 'file',
  content => $nginx_conf,
}

-> exec { 'nginx restart':
  path => '/etc/init.d/',
}
