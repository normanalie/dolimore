```docker build -t dolimore:latest .```

```
SECRET_KEY=secretKey
DATABASE_URL=mysql+pymsql://dbuser:dbpassword@dbserver/dbname
DOLIBARR_API_KEY=apikey
DOLIBARR_URL=http://example.com/dolibarr
```

```docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=dbname -e MYSQL_USER=dbuser -e MYSQL_PASSWORD=dbpassword mysql/mysql-server:latest```

```docker run --name dolimore  -p 5000:5000 --rm --env-file .env -v /path/on/host:/home/dolimore/app/static/files --link mysql:dbserver dolimore:latest```