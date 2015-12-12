#!/usr/bin/env perl

open IN, shift;

while (<IN>){
    my ($warn, $len) = $_ =~ /\d+/;
    printf "$len ";
    if($len<16){$lt16++;}
    elsif($len>1024){$gt1024++;}
    elsif($len==16){$len16++;}
    elsif($len==1024){$len1024++;}
}

close IN;

printf "\n";

printf "# reads < 16: $lt16\n";
printf "# reads > 1024: $gt1024\n";
printf "# reads == 16: $len16\n";
printf "# reads == 1024: $len1024\n";
