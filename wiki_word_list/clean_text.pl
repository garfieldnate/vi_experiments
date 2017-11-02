use strict;
use warnings;
use utf8;
# required for regex sets
use 5.018;
use feature qw(fc);
# allow piping unicode data to through STDIN
use open qw(:std :utf8);
no warnings "experimental::regex_sets";

while(my $line = <>) {
    $line =~ s/[\r\n]//g;
    # normalize case
    $line = fc($line);
    # remove punctuation, except _, which is used to join words
    $line =~ s/(?[ \p{Punct} + \p{Symbol} - [_] ])/ /g;
    # combined all numbers into a single token
    $line =~ s/\d+(\s+?\d+)*/ #NUM# /g;
    # Combine Chinese(y) words into one token
    $line =~ s/\p{Unified_Ideograph=yes}+/#HAN#/g;
    # combine adjacent whitespaces
    $line =~ s/\s{2,}/ /g;

    say $line if $line;
}
