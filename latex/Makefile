
default:
	# latexmk -pdfdvi thesis.tex
#	latexmk thesis.tex
#	dvipdfmx thesis
	 pdflatex thesis.tex
	 bibtex thesis.aux
	 pdflatex thesis.tex
	 pdflatex thesis.tex
thI:
	pdflatex thesis-I.tex
	bibtex thesis-I.aux
	pdflatex thesis-I.tex
	pdflatex thesis-I.tex
thII:
	pdflatex thesis-II.tex
	bibtex thesis-II.aux
	pdflatex thesis-II.tex
	pdflatex thesis-II.tex
	
	
cont:
	#latexmk -pvc -view=dvi thesis.tex
#	latexmk -pdfdvi -pvc -view=pdf thesis.tex

clean:
	@latexmk -C
	@rm -f *.brf
	@rm -f *.lol
	@rm -f *.out
	
