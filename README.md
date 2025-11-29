## DB Setup
To launch the db use
```
docker compose up -d
```

After the db is started use
```
alembic upgrade head
```
to perform migrations