.INTERMEDIATE: .version
.PHONY: help update full-update

.version:
	@echo "$$(poetry version -s)" > $@

help:
	@echo AVAILABLE COMMANDS
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-23s\033[0m%s\n", $$1, $$2}'

update: ## Update catalog and app images in docker-compose.yml to specified version
ifndef VERSION
	$(error VERSION is not set)
endif

	@sed -Ei -e 's/(image: matatika\/(catalog|app)).*/\1:$(VERSION)/g' files_matatika_ext/docker-compose.yml

full-update: .version update ## Update, bump project version, commit changes and tag
	@poetry version minor
	@git commit -m 'Update image tags to `$(VERSION)`' files_matatika_ext/docker-compose.yml
	@git commit -m 'Bump version from `'"$$(cat $<)"'` to `'"$$(poetry version -s)"'`' pyproject.toml
	@git tag "v$$(poetry version -s)"
