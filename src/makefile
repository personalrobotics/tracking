CC = g++
CFLAGS = -g -Wall -std=c++11 -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup `python -m pybind11 --includes` -I ./
SRCS = src/tracking_class.cpp 
PROG = src/lib/find_marker`python-config --extension-suffix`

$(PROG):$(SRCS)
	mkdir -p src/
	$(CC) $(CFLAGS) -o $(PROG) $(SRCS)

clean:
	rm src/find_marker
