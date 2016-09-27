images_dia := $(wildcard diagrams/*.dia)
images_png := $(images_dia:%.dia=%.png)

all: slides.html $(images_png)

%.png: %.dia 
	dia --filter=png-libart --export=$@ $< 

%.html: %.asciidoc 
	asciidoc -b slidy  $<

clean:
	rm *.html
	rm diagrams/*.png
