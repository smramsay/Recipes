#!/usr/bin/env bash

pandoc -o /tmp/recipe.pdf \
	--pdf-engine xelatex \
	-H ${HOME}/documents/recipes/custom-preamble.tex \
	-V geometry:a4paper \
	-V geometry:margin=0.75in \
	-V fontsize=12pt \
	-V mainfont="Droid Sans Mono" \
	-V mainfontoptions:BoldFont="Droid Serif Bold" \
	"$1"
