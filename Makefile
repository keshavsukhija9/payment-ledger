.PHONY: dev test load-test duplicate-storm integrity-check logs clean

dev:
	docker compose up --build

test:
	docker compose -f docker-compose.test.yml run --rm backend

load-test:
	k6 run load_tests/concurrent_transfers.js \
		-e BASE_URL=http://localhost:8000 \
		-e HOTSPOT_ACCOUNT_ID=a0000000-0000-0000-0000-000000000004 \
		-e RECEIVER_ACCOUNT_ID=a0000000-0000-0000-0000-000000000002

duplicate-storm:
	k6 run load_tests/duplicate_storm.js \
		-e BASE_URL=http://localhost:8000 \
		-e HOTSPOT_ACCOUNT_ID=a0000000-0000-0000-0000-000000000004 \
		-e RECEIVER_ACCOUNT_ID=a0000000-0000-0000-0000-000000000002

integrity-check:
	docker compose exec postgres \
		psql -U ledger_user ledger -c \
		"SELECT entry_type, COUNT(*), SUM(amount) FROM ledger_entries GROUP BY entry_type;"

logs:
	docker compose logs -f backend

clean:
	docker compose down -v
	docker system prune -f
