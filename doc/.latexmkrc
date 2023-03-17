$hash_calc_ignore_pattern{'pdf'} = '^/(CreationDate|ModDate|ID)';
# Also apply the same idea to eps files, so that this code works with latex
$hash_calc_ignore_pattern{'eps'} =  '^(%%CreationDate: |%DVIPSSource: )';
$pdf_mode = 5;
$dvi_mode = 0;
$postscript_mode = 0;
$out_dir = 'build';
$pdflatex = "xelatex -shell-escape -interaction=nonstopmode %O %S";
