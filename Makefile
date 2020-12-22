all:
	python3 main.py http.txt res.txt && cat res.txt

clean:
	rm res.txt