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

## API Setup

To launch api server (non-containerized)
```
uvicorn backend.main:app --port 8000
```