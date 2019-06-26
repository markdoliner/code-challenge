.PHONY: check
check:
	pycodestyle find_store find_store_test.py
	pylint find_store find_store_test.py
	./find_store_test.py
