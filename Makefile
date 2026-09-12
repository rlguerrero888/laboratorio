.PHONY: install seed run-bronze run-silver run-gold docker-up docker-down

install:
	pip install -e ".[dev]"

# --- data lake seed ---
seed:
	python jobs/seed.py

# --- local jobs ---
run-bronze:
	python jobs/bronze_ingest.py

run-silver:
	python jobs/silver_pipeline.py

run-gold:
	python jobs/gold_analytics.py

# --- docker ---
docker-up:
	docker compose up --build -d

docker-down:
	docker compose down -v
