all: readme.html

%.html: %.txt
	asciidoc  $< 

clean:
	rm -f *~
	rm -f *.html
