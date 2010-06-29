CXX = g++
CFLAGS = `pkg-config --cflags opencv`
LDFLAGS = `pkg-config --libs opencv`

image_rotate: image_rotate.cpp
	$(CXX) -o $@ $^ $(CFLAGS) $(LDFLAGS)
clean:
	rm -f image_rotate