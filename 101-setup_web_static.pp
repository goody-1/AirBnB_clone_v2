# Install Nginx if it doesn't exist
if ! package { 'nginx':
  ensure => installed,
}
{
  package { 'nginx':
    ensure => present,
  }
  # allow HTTP
  exec { 'allow HTTP':
    command => "ufw allow 'Nginx HTTP'",
    path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
    onlyif  => '! dpkg -l nginx | egrep \'îi.*nginx\' > /dev/null 2>&1',
  }

  # change folder rights
  exec { 'chmod www folder':
    command => 'chown -R "$USER":"$USER" /var/www/html',
    path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  }

  # create index file
  file { '/var/www/html/index.html':
    content => "Hello World!\n",
  }

  # create 404 error file
  file { '/var/www/html/404.html':
    content => "Ceci n'est pas une page\n",
  }
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Modify Nginx configuration
augeas { 'nginx_hbnb_static':
  context => '/files/etc/nginx/sites-available/default',
  changes => "set server/location[last()+1] /hbnb_static\nset server/location[last()]/alias /data/web_static/current/\nset server/location[last()]/index index.html",
  notify  => Service['nginx'],
}

file { '/etc/nginx/sites-enabled/default':
  ensure => 'link',
  target => '/etc/nginx/sites-available/default',
  owner  => 'root',
  group  => 'root',
  mode   => '0644',
  notify => Service['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
