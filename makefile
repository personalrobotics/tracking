CC = g++
SRCS = src/tracking_class.cpp

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    CFLAGS = -g -Wall -std=c++11 -O3 -Wall -fPIC -shared -std=c++11 `python -m pybind11 --includes` -I /usr/include/python2.7 -I ./
    PROG = src/find_marker.so
endif

ifeq ($(UNAME_S),Darwin)
    CFLAGS = -g -Wall -std=c++11 -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup `python -m pybind11 --includes` -I ./
    PROG = src/find_marker`python-config --extension-suffix`
endif

$(PROG):$(SRCS)
	mkdir -p src/
	$(CC) $(CFLAGS) -o $(PROG) $(SRCS)

clean:
	rm -rf src/find_marker
