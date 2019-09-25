sudo docker build -t serviceapi .
sudo docker run -dit --restart unless-stopped  -p 4443:4443 -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock -v $(sudo readlink -f /etc/letsencrypt/live/www.capnflint.com/privkey.pem):/app/certs/privkey.pem:ro -v $(sudo readlink -f /etc/letsencrypt/live/www.capnflint.com/fullchain.pem):/app/certs/fullchain.pem:ro --name serviceapi serviceapi