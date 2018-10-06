clean:
	rm -f test/*_out.xml
	rm -f test/*_diff.xml
	
test:
	./test.sh
release:
	git rm --cached test/*
	git rm --cached test.sh
	rm -Rf test
	rm -f test.sh
