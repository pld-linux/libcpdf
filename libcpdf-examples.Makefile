#
# just a makefile to generate the examples directory
# written by Matt Warner <mwarner1@ix.netcom.com>, 25 Nov 1998.

OBJECTS=arc/Arcs.o dash/dashtest.o text/textalign.o marker/MarkerTest.o \
	weather/weather.o cover/cover.o timeaxis/timeaxis.o \
	filltest/filltest.o minimal/Minimal.o domain/DomainDemo.o \
	bezier/beziertest.o outline/outline.o fontlist/fontlist.o \
	linkpdfpage/linkpdfpage.o pdfclock/pdfclock.o textbox/textbox.o 

RUNOBJS=arc/Arcs dash/dashtest text/textalign marker/MarkerTest \
	cover/cover timeaxis/timeaxis \
	filltest/filltest domain/DomainDemo outline/outline fontlist/fontlist \
	linkpdfpage/linkpdfpage pdfclock/pdfclock textbox/textbox
	 
	

.SUFFIXES: .o .c

all: $(OBJECTS) run

.c.o:
	gcc -O3 -c $*.c -o $*.o
	echo $*
	gcc -o $* $*.o -lz -lc -lm -lcpdf

clean:
	rm -f $(OBJECTS)
	rm -f $(RUNOBJS)

realclean:
	rm -f $(OBJECTS)
	rm -f *.pdf
	rm -f $(RUNOBJS)
	find . -name "*.pdf" exec rm -f \{\} 
	find . -name core exec rm -f \{\} 

run:
	ln -s ../cpdfman110.pdf cpdfman110.pdf
	-for app in $(RUNOBJS); do \
apath=`echo $$app | sed -e 's;/.*;;'`; \
cd $$apath; \
aprog=`echo $$app | sed -e 's;.*/;;'`; \
(./$$aprog); \
cd ..; \
done
	weather/weather weather/OAK.wdat
	cp -f arctest.pdf minimal.pdf
	minimal/Minimal minimal.pdf


