#!/usr/bin/env perl

open $fq, "<", shift or die "could not open file\n";

while (<$fq>){
    if($_ =~ /([ACTG]+)/){
        $seq_len = length($1);
        if($seq_len<16){$lt16++;}
        elsif($seq_len>2432){$gt2432++;}
    }
}
close $fq;
printf "less than 16: $lt16\n";
printf "greater than 2432: $gt2432\n"; 
