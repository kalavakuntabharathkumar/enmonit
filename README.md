# Real-Time Industrial Energy Monitoring Dashboard

Portfolio-ready simulation of an industrial energy monitoring stack.

## Stack
Python, FastAPI, PostgreSQL + TimescaleDB, Grafana, Docker Compose, Git

## Architecture
Sensor simulator -> FastAPI -> TimescaleDB -> Grafana

## Quick start
```bash
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Grafana: http://localhost:3000
- DB: localhost:5432
- Grafana login: admin / admin

Generate one hour of 1-second data:
```bash
docker compose exec api python /app/simulator/generate_data.py --seconds 3600
```

Run tests locally:
```bash
pip install -r backend/requirements.txt
pytest
```

The project uses synthetic data. Resume metrics should be described as simulated benchmarks unless independently measured.
