.PHONY: serve build bundle new-mi new-prb new-journal

serve:
	python scripts/build_indexes.py
	mkdocs serve -a 0.0.0.0:8000

build:
	python scripts/build_indexes.py
	mkdocs build --strict --site-dir site

bundle:
	python scripts/build_indexes.py
	python scripts/build_bundles.py

new-mi:
	python scripts/new_page.py mi --id $(ID) --sev $(SEV) --service "$(SERVICE)"

new-prb:
	python scripts/new_page.py prb --id $(ID) --owner $(OWNER)

new-journal:
	python scripts/new_page.py journal --author $(AUTHOR)
