#### docker compose for nginx with self-signed certificate

1. Generate a keypair substitute {my-site.com}
`openssl req -newkey rsa:2048 -nodes -keyout nginx/my-site.com.key -x509 -days 365 -out nginx/my-site.com.crt`
2. Substitute {my-site.com} in the nginx.conf
3. Substitute {my-site.com} in the docker-compose.yml
4. Put web app files in ./site/ 
5. Run
`docker-compose up -d`