# Compilazione: `latexmk` dalla cartella del progetto. PDF in latex/build/main.pdf
$pdf_mode = 1;
$do_cd = 1;
$out_dir = 'build';
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
@default_files = ('latex/main.tex');
