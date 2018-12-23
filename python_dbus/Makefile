TOPDIR = ../

images_dia = $(wildcard figures/*.dia)
images_png = $(images_dia:.dia=.png)

all: slides.html


slides.html: $(images_png)

EXPORT_WIDTH=800

clean:
	rm -f $(images_png)
	rm -f *~

include $(TOPDIR)/stylesheets/Makefile.rules
