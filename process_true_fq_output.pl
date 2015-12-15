#!/usr/bin/env perl

open IN, shift;
while (<IN>){
    ($len) = $_ =~ /((?<=\()\d+(?= bp\)))/;
    if($len<16){$lt16++;}
    elsif($len>2432){$gt2432++; printf $len."\n";}
}close IN;

printf "# reads < 16: $lt16\n";
printf "# reads > 2432: $gt2432\n";
