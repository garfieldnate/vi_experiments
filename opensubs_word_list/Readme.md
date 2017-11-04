# OpenSubtitles-based Vietnamese Frequency Dictionary

This directory contains a frequency dictionary created from a Vietnamese subtitle corpus. Props to http://www.opensubtitles.org/ for sharing this data.

## Method

This requires perl and JVnTokenizer.

1. Download the Open Subtitles data for Vietnamese from here: http://opus.lingfil.uu.se/download.php?f=OpenSubtitles2016/vi.tar.gz and extract the archive.
2. Extract the text save in files of 30K lines each :

    perl get_sents.pl PATH/TO/OpenSubtitles2016 | split -l 30000 - subtitles_

The files will total about 127MB.

3. Tokenize with JVnTokenizer. Run `jvntextpro.JVnTextProTest` with the following arguments (replace the two directory names as appropriate; JVnTextPro comes with a models directory): `-wordseg -modeldir JVnTextPro/models -input PATH/TO/FILES`. This will create one .txt.pro file for each .txt file in the directory.
4. Normalize the words and count occurrences using the scripts from the Wikipedia folder:

    cat PATH/TO/FILES/*.txt.pro | perl wiki_word_list/clean_text.pl | perl wiki_word_list/count_words.pl > opensubs_unigrams.txt

The resulting file has been added to this repository.

Total tokens: 18,503,218
Total types:  146,797

## Comments

The subtitles corpus is arguably more useful than Wikipedia in making a general purpose frequency dictionary; you don't have to filter out mathematical symbols or worry about repetitive Wikipedia text, the covered subject matter might actually be wider (terms for insects were among the highest in the Wikipedia corpus).

I did notice that ý is a high frequency word in this dictionary, but I couldn't find a definition for it by itself. This makes me suspicious that JVnTextPro might not perform as well on colloquial input.

Note: how many different authors are represented in the OpenSubtitles corpus?

