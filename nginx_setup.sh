#!/bin/bash
cat << 'EOF' > /etc/nginx/sites-available/goclaw-cham
server {
    listen 80;
    server_name agent.elsaphuong.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF
ln -sf /etc/nginx/sites-available/goclaw-cham /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
