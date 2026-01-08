test:
	python3 -m unittest test_shunting_yard.py -v

trim:
	@find . -name "*.py" -type f -exec sed -i '' 's/[[:space:]]*$$//' {} \;
