OBJS= fmasgn.o fmif.o fmnote.o\
	fmpart.o fmtone.o fmvoice.o fmsd1_raspi.o\
	

server: $(OBJS) server.o
	gcc -o server server.o $(OBJS) -l bcm2835

ymf825srv: $(OBJS) server.o
	gcc -o ymf825srv server.o $(OBJS) -l bcm2835



fmasgn.o:   fmasgn.c fmasgn.h fmtype.h
fmif.o:     fmif.c fmif.h 
fmnote.o:   fmnote.c fmnote.h fmtype.h
fmpart.o:   fmpart.c fmpart.h fmtype.h
fmtone.o:   fmtone.c fmtone.h fmtype.h
fmvoice.o:  fmvoice.c fmvoice.h fmtype.h
fmsd1_raspi.o:  fmsd1_raspi.c
fm825test.o:    fm825test.c fmif.h fmsd1.h  
settone.o: settone.c fmif.h fmsd1.h  
sendmidi.o: sendmidi.c fmif.h fmsd1.h  
server.o: server.c fmif.h fmsd1.h  
init.o: init.c fmif.h fmsd1.h  
.c.o:
	gcc -c $<
