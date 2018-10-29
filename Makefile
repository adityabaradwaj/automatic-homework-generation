# TARGETS

hw:
	make render cat=hw n=${n}
	mv src/hw/hw${n}-raw.tex rendered/hw${n}/
	# open rendered/hw${n}/hw${n}.pdf
	# open rendered/hw${n}/hw${n}-sol.pdf

dis:
	make render cat=dis n=${n}
	# open rendered/dis${n}/dis${n}.pdf
	# open rendered/dis${n}/dis${n}-sol.pdf

practice:
	make render cat=practice n=${n}
	# open rendered/practice${n}/practice${n}.pdf
	# open rendered/practice${n}/practice${n}-sol.pdf

img:
	bash generate-img ${n}

publish:
	python3.6 publish.py ${n} ${test}

render:
	python3 generate.py ${cat} ${n}
	mkdir -p rendered/${cat}${n}
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n} src/${cat}/${cat}${n}.tex
	pdflatex -jobname=rendered/${cat}${n}/${cat}${n}-sol src/${cat}/${cat}${n}-sol.tex
