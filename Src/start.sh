sudo docker build -t serviceapi .
sudo docker run -dit --restart unless-stopped  -p 4443:4443 -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock serviceapi