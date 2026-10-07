## Note
make sure to always check the alembic migration to not drop the table

### Run Command
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Migration with alembic
- To save the updated migration into database
```bash
alembic upgrade head
```

- To do the migration
```bash
alembic revision --autogenerate -m "message"
```

- To check current alembic history
```bash
alembic history
```