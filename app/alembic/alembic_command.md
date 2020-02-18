
alembic init alembic
alembic current
alembic revision --autogenerate -m 'Added last_updated'
alembic upgrade head