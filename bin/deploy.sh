#!/bin/sh

# usage: ./bin/deploy.sh example.com '443 ssl'

set -e
set -x

project_name=flask_healthcheck
deployment_server=${1:-localhost}
port=${2:-8000}

deployment_dir=/var/${project_name}

sudo mkdir -p $deployment_dir
sudo chown -R www-data:www-data $deployment_dir

sudo -u www-data rsync -ra \
  --exclude .git/ \
  --filter=':- .gitignore' \
  . \
  $deployment_dir

sudo -u www-data rsync -ra \
  .venv \
  --exclude=__pycache__/ \
  $deployment_dir


cat <<EOT | sudo tee /etc/systemd/system/${project_name}.socket
[Unit]
Description=wti-avatar socket

[Socket]
ListenStream=/run/${project_name}/socket

[Install]
WantedBy=sockets.target
EOT

cat <<EOT | sudo tee /etc/systemd/system/${project_name}.service
[Unit]
Description=Flask Service
Requires=${project_name}.socket
After=network.target

[Service]
PIDFile=/run/${project_name}/pid
User=www-data
Group=www-data
RuntimeDirectory=${project_name}
WorkingDirectory=${deployment_dir}
Environment=FLASK_ENV=staging
ExecStart=/bin/sh -c "${deployment_dir}/.venv/current/bin/gunicorn \\
	-w 2 \\
	--bind unix:/run/${project_name}/socket \\
	--pid /run/${project_name}/pid \\
	api.app:app"
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOT

cat <<EOT | sudo tee /etc/tmpfiles.d/${project_name}.conf
d /run/${project_name} 0755 www-data www-data - -
EOT
  
# Reload and restart services
sudo systemctl daemon-reload

# Enable the socket
sudo systemctl enable $project_name.socket

# Create /run/$flask_project_name with correct permissions before starting the socket
# sudo systemd-tmpfiles --create

# Start the socket 
sudo systemctl start $project_name.socket
sudo service $project_name start

# Use nginx to handle outside world communications.
cat <<EOT | sudo tee /etc/nginx/sites-available/$project_name
server {
    listen ${port};
    server_name ${deployment_server};

    location / {
        include proxy_params;  # This will allow flask url_for to function properly

        if (!-f \$request_filename) {
            proxy_pass http://unix:/run/${project_name}/socket;
            break;
        }
    }
}
EOT

sudo ln -fs /etc/nginx/sites-available/$project_name /etc/nginx/sites-enabled/
sudo service nginx reload
