# Wikipedia Keyword Extraction

Following the method described [here](https://www.sketchengine.co.uk/wp-content/uploads/2015/05/Corpus_Factory_2010.pdf), the first step to gathering a large web corpus is to generate search strings. We do this by first building a Wikipedia-based corpus.

##Required software:

* Python 2 or 3, Perl 5.18+
* [Wikiextractor](https://github.com/attardi/wikiextractor)
* [jq](https://stedolan.github.io/jq/)
* [JVnTextPro](http://jvntextpro.sourceforge.net/)
* [Corpus Catcher](https://github.com/translate/corpuscatcher)
* [BodyTextExtractor](https://github.com/aidanf/BTE)

## Method

1. Download the latest Vietnamese Wikipedia article dump here: Downloading the VI Wikipedia dump here: http://dumps.wikimedia.org/viwiki/latest/viwiki-latest-pages-articles.xml.bz2.

2. Extract suitable text files

The paper says that Wiki files were considered to have connected text if that had at least 500 words, but I think they meant syllables for Vietnamese since no tokenization process is indicated. `jq` lets you filter by character length; as estimate, I will multiply 500 by the number of letters in an average word (as measured by the previous Wikipedia corpus I made). 

I got the statistics from the previous corpus using word_size_estimator.py, which gave an answer of 5.17. Times 500 words = 2585.

So, run the following command to extract the articles into ~100 .txt files (replace YOUR/TEXT/DIRECTORY/ with the desired file location):

    python WikiExtractor.py --json --no-templates --filter_disambig_pages --min_text_length 2585 --output - viwiki-latest-pages-articles.xml.bz2 | jq --raw-output .text | sed  '/^$/d' | split -l 30000 - YOUR/TEXT/DIRECTORY/

The trailing slash on `YOUR/TEXT/DIRECTORY/` is important! We remove template expansion, section headers, and disambiguation pages because we do not want to bias word frequency with repeated template text. We set a length minimum to try to avoid articles without real text. `jq` is used to extract just the text from WikiExtractor's JSON output, and then `sed` is used to remove empty lines. Finally, `split` pipes the output in 1-10M chunks to several files so that they are easier to inspect in a text editor. This is not strictly necessary.

Hmm, looking at the output, it seems like section headers still snuck in there somehow...

3. Rename files to have the `.txt` extension, which is necessary for JVnTextPro in the next step.

    rename 's/$/.txt/' YOUR/TEXT/DIRECTORY/*

4. Run sentence segmentation and word tokenization. Run `jvntextpro.JVnTextProTest` with the following arguments (replace the two directory names as appropriate; JVnTextPro comes with a models directory): `-senseg -wordseg -modeldir JVnTextPro/models -input YOUR/TEXT/DIRECTORY`. This will create one .txt.pro file for each of the original .txt files. (I had to run this in IntelliJ; they don't have a Gradle build or anything to run it standalone quickly)

5. Normalize the words and count occurrences using the included scripts:

    cat YOUR/TEXT/DIRECTORY/*.txt.pro | perl ../../wiki_word_list/clean_text.pl | perl ../../wiki_word_list/count_words.pl > wikipedia_unigrams.txt

The resulting wikipedia_unigrams.txt has been added to this repository. The file is not perfectly clean, and there are still some junk entries, especially mathematical symbols like a superscript 2, etc.

Total tokens: 88,883,030
Total types:  1,145,157

6. Get the list of 500 most frequent words:

    cat wikipedia_unigrams.txt | cut -f1 | head -n500 > wikipedia_top_500.txt

7. Get the list of mid-frequency words (used for querying). There is some cleaning in there, too, as 1-byte words and ² are all garbage:

    cat wikipedia_unigrams.txt | cut -f1 | awk '{ if (length($0) >= 2 && $0 != "²") print }' | head -n6000 | tail -n 5000 > wikipedia_mid_5000.txt

8. Generate search queries:

    python gen_queries.py wikipedia_mid_5000.txt 4 30000 > queries_30000.txt

9. Run crawler using these search queries:
