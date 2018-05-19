use strict;
use warnings;
use 5.010;
# allow piping unicode data to through STDIN
use open qw(:std :utf8);

sub  trim { my $s = shift; $s =~ s/^\s+|\s+$//g; return $s };

my %index;
while(my $line = <>) {
    $line =~ s/[\r\n]//g;
    my @words = split /\s+/, $line;
    for my $word(@words) {
        $word = trim $word;
        $index{$word}++ if $word;
    }
}

my $total = 0;
for my $word (sort {$index{$b} <=> $index{$a}} keys %index) {
    my $frequency = $index{$word};
    # JVnTextPro used _ to join words; fix that here
    $word =~ s/_/ /g;
    $word = trim $word;
    if(!$word) {
        next;
    }
    $total += $frequency;
    say "$word\t$frequency";
}

print STDERR "Total words: $total";
