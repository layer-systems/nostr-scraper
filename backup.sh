docker exec -it postgres bash -c "pg_dump -U nostr nostr > /var/lib/postgresql/data/backup.sql"
docker cp postgres:/var/lib/postgresql/data/backup.sql backup.sql