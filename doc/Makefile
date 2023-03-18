all: clean build

build: main.tex
	mkdir -p build && \
	latexmk main.tex

clean:
	rm -rf build
