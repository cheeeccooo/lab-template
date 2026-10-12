# Compilazione: `latexmk` dalla cartella del progetto.
# PDF in latex/build/<nome>.pdf, dove <nome> è la riga `pdf` di setup.txt (default: main).
$pdf_mode = 1;
$do_cd = 1;
$out_dir = 'build';
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
@default_files = ('latex/main.tex');

if (open(my $fh, '<', 'setup.txt')) {
    while (<$fh>) {
        if (/^\s*pdf\s+([\w.\-]+)/) { ($jobname = $1) =~ s/\.pdf$//; }
    }
    close $fh;
}
