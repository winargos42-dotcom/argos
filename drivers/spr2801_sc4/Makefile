CC ?= cc
CFLAGS ?= -O2 -g -std=c11 -Wall -Wextra -Werror -Wconversion -Wshadow -pedantic
LDFLAGS ?=
BIN := bin/argos-sc4
LIB := bin/libargos_sc4.so
SRC := src/argos_sc4.c src/argos_sc4_cli.c
.PHONY: all clean test
all: $(BIN) $(LIB)

$(BIN): $(SRC) src/argos_sc4.h
	@mkdir -p bin
	$(CC) $(CFLAGS) -Isrc $(SRC) $(LDFLAGS) -o $(BIN)

$(LIB): src/argos_sc4.c src/argos_sc4.h
	@mkdir -p bin
	$(CC) $(CFLAGS) -fPIC -shared -Isrc src/argos_sc4.c $(LDFLAGS) -o $(LIB)

test: $(BIN) $(LIB)
	python3 -m unittest discover -s tests -p 'test_*.py' -v

clean:
	rm -f $(BIN)
