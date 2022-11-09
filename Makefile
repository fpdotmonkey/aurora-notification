PACKAGE_NAME=aurora_notification

PROJECT_PATH=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: run
run: test
	python3 -m "${PACKAGE_NAME}"

.PHONY: test
test: lint
	python3 -m pytest "${PACKAGE_NAME}"

.PHONY: lint
lint: venv_activation
	python3 -m mypy "${PACKAGE_NAME}"
	python3 -m flake8 "${PACKAGE_NAME}"
	python3 -m pylint "${PACKAGE_NAME}"

.PHONY: venv_activation
venv_activation: venv
	@if [ -z "${VIRTUAL_ENV}" \
		  -o "${VIRTUAL_ENV}" != "${PROJECT_PATH}venv" \
		]; then \
		echo "Please manually activate the venv with \`. venv/bin/activate\`"; \
		exit 1; \
	fi

venv: requirements.txt
	# https://github.com/fpdotmonkey/env/blob/master/bin/venvgen
	venvgen

.PHONY: clean
clean:
	# https://github.com/fpdotmonkey/env/blob/master/bin/venvgen
	venvgen --delete force
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf $(shell find -name venv -prune -o -name __pycache__ -type d)
	@echo "Remember to manually deactivate the venv with \`deactivate\`"
