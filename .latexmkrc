# Compilazione: `latexmk` dalla cartella del progetto.
# PDF in latex/build/<nome>.pdf, dove <nome> è la voce `pdf` di setup.yaml (default: main).
$pdf_mode = 1;
$do_cd = 1;
$out_dir = 'build';
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
@default_files = ('latex/main.tex');

if (open(my $fh, '<', 'setup.yaml')) {
    while (<$fh>) {
        if (/^\s*pdf:\s*([\w.\-]+)/) { ($jobname = $1) =~ s/\.pdf$//; }
    }
    close $fh;
}
