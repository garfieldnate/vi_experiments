use strict;
use warnings;
use 5.010;
# allow piping unicode data to through STDIN
use open qw(:std :utf8);

my %index;
while(my $line = <>) {
    $line =~ s/[\r\n]//g;
    my @words = split /\s/, $line;
    for my $word(@words) {
        $index{$word}++;
    }
}

for my $word (sort {$index{$b} <=> $index{$a}} keys %index) {
    my $frequency = $index{$word};
    # JVnTextPro used _ to join words; fix that here
    $word =~ s/_/ /g;
    if(!$word) {
        next;
    }
    say "$word\t$frequency";
}
