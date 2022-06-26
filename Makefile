clean:
	@rm -rf ./.pytest_cache
	@rm -rf ./dist
	@rm -rf ./src/*.egg-info
	@echo "OK"

install:
	pip uninstall -y filehole
	python -m build
	pip install --find-links dist filehole==0.0.3