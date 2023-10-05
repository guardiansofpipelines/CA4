install:
	echo "Installing dependencies..."
	pip install --upgrade pip 
	pip install -r requirements.txt
	echo "Done Installing."

lint:
	echo "Linting..."
	pylint --disable=R,C src/*.py
	echo "Done Linting."

test:
	@echo "Running tests..."
	pytest src/test*.py
	@echo "Done running tests."

run:
	@echo "Running..."
	python src/UserAuthentication.py
	@echo "Done running."