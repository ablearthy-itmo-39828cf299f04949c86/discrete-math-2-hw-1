all: clean build

build: main.tex
	mkdir -p build && \
	latexmk -shell-escape -xelatex main.tex -outdir=build

clean:
	rm -rf build
