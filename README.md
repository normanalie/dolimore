# Dolimore

```docker build -t dolimore:latest .```

```
SECRET_KEY=secretKey
DATABASE_URL=mysql+pymysql://dbuser:dbpassword@dbserver/dbname
DOLIBARR_API_KEY=apikey
DOLIBARR_URL=http://example.com/dolibarr

MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=dbname
MYSQL_USER=dbuser
MYSQL_PASSWORD=dbpassword
```

```docker run --name mysql --restart always -d --env-file .env mysql/mysql-server:latest```

```docker run --name dolimore --restart always -d  -p 5000:5000 --env-file .env -v /path/on/host:/home/dolimore/app/static/files --link mysql:dbserver dolimore:latest```