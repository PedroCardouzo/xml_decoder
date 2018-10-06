clean:
	rm -f test/*_out.xml
	rm -f test/*_diff.xml
	
test:
	./test.sh
release:
	rm -Rf test
	rm -f test.sh
