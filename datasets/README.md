## Datasets
Datasets are provided in 3 folders within `/datasets/`: `KB13`, `NL-RX-Synth`, `NL-RX-Turk`. Datasets are open source under MIT license.

* `KB13` is the data from [Kushman and Barzilay, 2013](http://people.csail.mit.edu/nkushman/papers/naacl2013.pdf). 
* `NL-RX-Synth` is data from `NL-RX`<sup>1</sup> with original synthetic descriptions.
* `NL-RX-Turk` is data from `NL-RX`<sup>1</sup> with Mechanical-Turk paraphrased descriptions.

<sup>1</sup> `NL-RX` is the dataset from our paper.

### Dataset Notes
The data is a parallel corpus, so the folder is split into 2 files: `src.txt` and `targ.txt`. `src.txt` is the natural language descriptions. `targ.text` is the corresponding regular expressions.

* Note - all models (ours and previous) that perform this task perform string replacement of any string in quotation marks. This means that "lines that contain 'blue'" and "lines that contain 'red'", will both be identical in some form "lines that contain <WORD>".
	* Our datasets have this already pre-computed - for each example, the words in quotations appear in the order 'dog', 'truck', 'ring', 'lake' to universally indicate their position.
