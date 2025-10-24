.PHONY: serve build bundle new-mi new-prb new-journal

serve:
	python3 scripts/build_indexes.py
	mkdocs serve -a 0.0.0.0:8000

build:
	python3 scripts/build_indexes.py
	mkdocs build --strict --site-dir site

bundle:
	python3 scripts/build_indexes.py
	python3 scripts/build_bundles.py

new-mi:
	python3 scripts/new_page.py mi --id $(ID) --sev $(SEV) --service "$(SERVICE)"

new-prb:
	python3 scripts/new_page.py prb --id $(ID) --owner $(OWNER)

new-journal:
	python3 scripts/new_page.py journal --author $(AUTHOR)

# GitFlow Operations
.PHONY: feature-start feature-finish release-start release-finish hotfix-start hotfix-finish

feature-start:
	git checkout develop
	git checkout -b feature/$(FEATURE_NAME)

feature-finish:
	git checkout develop
	git merge feature/$(FEATURE_NAME)
	git branch -d feature/$(FEATURE_NAME)
	git push origin develop

release-start:
	git checkout develop
	git checkout -b release/$(RELEASE_NAME)

release-finish:
	git checkout main
	git merge release/$(RELEASE_NAME)
	git tag -a v$(RELEASE_NAME) -m "Release $(RELEASE_NAME)"
	git push origin main --tags
	git checkout develop
	git merge release/$(RELEASE_NAME)
	git branch -d release/$(RELEASE_NAME)

hotfix-start:
	git checkout main
	git checkout -b hotfix/$(HOTFIX_NAME)

hotfix-finish:
	git checkout main
	git merge hotfix/$(HOTFIX_NAME)
	git branch -d hotfix/$(HOTFIX_NAME)
	git push origin main
