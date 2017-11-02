# Wikipedia Word List

A first attempt to create a Vietnamese high frequency word list, using the Vietnamese Wikipedia. I do NOT want a frequency list of syllables/syllabemes, which is what is commonly offered.

## Method

Utilized software:

* Python 2 or 3, Perl 5.18+
* [Wikiextractor]
* [jq](https://stedolan.github.io/jq/)
* [JVnTextPro](http://jvntextpro.sourceforge.net/)

Steps:

1. Download the latest Vietnamese Wikipedia article dump here: Downloading the VI Wikipedia dump here: http://dumps.wikimedia.org/viwiki/latest/viwiki-latest-pages-articles.xml.bz2.
2. Run the following command to extract the articles into ~100 .txt files (replace YOUR/TEXT/DIRECTORY with the desired file location):

    python WikiExtractor.py --json --no-templates --sections --output - --filter_disambig_pages viwiki-latest-pages-articles.xml.bz2 | jq --raw-output .text | sed  '/^$/d' | split -l 30000 - YOUR/TEXT/DIRECTORY

We remove template expansion because we do not want to bias word frequency with repeated template text. We add section headers (I figured they might be relevant). We also filter disambiguation pages. `jq` is used to extract just the text from WikiExtractor's JSON output, and then `sed` is used to remove empty lines. Finally, `split` pipes the output in 1-10M chunks to several files so that they are easier to inspect in a text editor. This is not strictly necessary.

3. Run sentence segmentation and word tokenization. Run `jvntextpro.JVnTextProTest` with the following arguments (replace the two directory names as appropriate; JVnTextPro comes with a models directory): `-senseg -wordseg -modeldir JVnTextPro/models -input YOUR/TEXT/DIRECTORY`. This will create one .txt.pro file for each of the original .txt files.

4. Normalize the words and count occurrences using the included scripts:

    cat YOUR/TEXT/DIRECTORY/viwikidump/jvntok_seg/*.txt.pro | perl clean_text.pl | perl count_words.pl > wikipedia_unigrams.txt

The resulting wikipedia_unigrams.txt has been added to this repository.

## Possible Improvments, Future Work

I ran tokenization with Roy_A's work [here](https://github.com/roy-a/Roy_VnTokenizer), but the result was unsatisfactory (proper nouns combined with their adjectives, periods combined with following words, etc.). I did some editing to the file to try to make it faster, so it is possible that I messed it up somehow, especially considering that Roy reports very high accuracy.

I was unable to get [VNtokenizer](mim.hus.vnu.edu.vn/phuonglh/softwares/vnTokenizer) to run at all.

Dinh et al's "Word segmentation of Vietnamese texts: a comparison of approaches" (LREC 2008) suggests that I might get better word tokenization accuracy with JVnSegmenter if I retrained it using their data. Seems like a great idea for further research. I cannot find a copy of PVnSeg, which is listed as having the best performance.

Of course, Wikipedia does not constitute a balanced corpus, and it would be better to use other corpora along with it, or even instead of it. The lowest hanging fruit is from [OpenSubtitles](http://opus.lingfil.uu.se/OpenSubtitles2016.php): These others got my hopes up but then dashed them (they may still be useful):

* https://catalog.ldc.upenn.edu/LDC2017S01 (phone convo transcripts; costs 25$; there are also plenty of other Vietnamese corpora from LDC. The LDC website is completely broken at the moment.)
* [VLSP NER Campaign Corpus](http://vlsp.org.vn/evaluation_campaign_NER)- the website is long dead. I wonder if any researcher could provide the corpus for me?
* https://the.sketchengine.co.uk/corpus/corp_info?corpname=preloaded/vietnamesewac2- not downloadable; however, they wrote a paper detailing its creation which could be interesting to duplicate: https://www.sketchengine.co.uk/wp-content/uploads/2015/05/Corpus_Factory_2010.pdf
* https://slhs.sdsu.edu/gtpham/vnspeech/Research/CVT/ResearchCVTWordList.html - 1M words from children's books and newspapers. Corpus cannot be downloaded, only word lists, and they only have syllables (grr!)
* http://sealang.net/vietnamese/corpus.htm- not downloadable.
* SUBTLEX-VIET- I see references to it online but I can't find where it actually is.

