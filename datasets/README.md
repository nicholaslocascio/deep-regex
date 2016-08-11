Data is provided in 3 folders: KB13, NL-RX-Synth, NL-RX-Turk. KB13 is the data from (Kushman and Barzilay, 2013). NL-RX-Synth is data from NL-RX with original synthetic descriptions. NL-RX-Turk is data from NL-RX with paraphrased descriptions.

The data is a parallel corpus, so the folder is split into 2 files: src.txt and targ.txt. src.txt is the natural language descriptions. targ.text is the corresponding regular expressions.

* Note - all models (ours and previous) that perform this task perform string replacement of any string in quotation marks. This means that "lines that contain 'blue'" and "lines that contain 'red'", will both be identical in some form "lines that contain <WORD>".

Our datasets have this already pre-computed - for each example the 1st word in an quotations is 'dog', the 2nd: 'lake', 3rd: '', 4th: ''.

 