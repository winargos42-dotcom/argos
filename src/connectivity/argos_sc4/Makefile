CC ?= cc
CFLAGS ?= -O2 -g -std=c11 -Wall -Wextra -Werror -Wconversion -Wshadow -pedantic
BIN = bin/argos-sc4
LIB = bin/libargos_sc4.so

.PHONY: all test clean
all: $(BIN) $(LIB)

$(BIN): argos_sc4.c argos_sc4_cli.c argos_sc4.h
	@mkdir -p bin
	$(CC) $(CFLAGS) -I. argos_sc4.c argos_sc4_cli.c -o $(BIN)

$(LIB): argos_sc4.c argos_sc4.h
	@mkdir -p bin
	$(CC) $(CFLAGS) -fPIC -shared -I. argos_sc4.c -o $(LIB)

test: all
	python3 -m unittest discover -s tests -p 'test_*.py' -v

clean:
	rm -f $(BIN) $(LIB)
