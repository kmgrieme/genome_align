#!/usr/bin/env perl

open $fq, "<", shift or die "could not open file\n";
open $fq_out, ">", shift or die "could not open write file\n";

while (<$fq>){
    push @block, $_;
    if(scalar(@block) == 4){
        ($seq) = $block[1] =~ /([ACTG]+)/;
        if(length($seq)>2432){
            @block = ();
            printf "long read found, skipping\n";
            next;
        }else{
            foreach $line (@block){
                printf $fq_out $line;
            }@block = ();
        }
    }
}
close $fq;
close $fq_out;
