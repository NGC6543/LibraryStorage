dev:
	python init_db.py
	uvicorn main:app --reload