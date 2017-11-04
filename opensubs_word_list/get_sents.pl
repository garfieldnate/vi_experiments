use strict;
use warnings;
use 5.010;
use autodie;
use PerlIO::gzip;
use Path::Tiny;
use XML::Twig;

binmode(*STDOUT, 'utf8');

my $parser = XML::Twig->new();

my $sub_dir = path($ARGV[0]);

my $iter = $sub_dir->iterator( {
    recurse         => 1,
    follow_symlinks => 0,
});

while(my $path = $iter->()) {
    # find and read all of the gzipped files in the OpenSubtitle directory
    if ($path->basename !~ /\.gz$/){
        next;
    }
    open my $gz, '<:gzip', $path;
    my $twig = $parser->parse($gz);

    # extract sentences and output one per line
    # sentences seem to be correctly split in the file.
    # remove or fix some punctuation in case it helps the word tokenizer
    for my $sentence ($twig->get_xpath('//s')) {
        my @words = $sentence->get_xpath('./w');
        shift @words while (@words and $words[0]->text eq '-');
        next unless @words;
        my $words = join ' ', map {$_->text} @words;
        $words =~ s/^" (.*) "$/$1/;
        $words =~ s/\s([,.:;?!])/$1/g;
        say $words;
    }
}
