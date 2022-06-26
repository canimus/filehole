clean:
	@rm -rf ./.pytest_cache
	@rm -rf ./dist
	@rm -rf ./src/*.egg-info
	@find . | grep "__pycache__" | xargs rm -rf
	@echo "OK"

install:
	pip uninstall -y filehole
	python -m build
	pip install --find-links dist filehole==0.0.3