# Makefile

BINDIR = ~/bin
SRCDIR = treenote-v0.2
SRC = AppDef.py AppView.py AppFile.py main.py
BIN = treenote 

install:
	mkdir $(BINDIR)/$(SRCDIR)
	cp $(SRC) $(BINDIR)/$(SRCDIR)
	cp $(BIN) $(BINDIR)

uninstall:
	rm -f $(BINDIR)/$(BIN)
	rm -fr $(BINDIR)/$(SRCDIR)

clean:
	rm -f *.pyc

# end of file
