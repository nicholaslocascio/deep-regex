## Neural Generation of Regular Expressions from Natural Language with Minimal Domain Knowledge

Code for the paper [Neural Generation of Regular Expressions from Natural Language
with Minimal Domain Knowledge](http://arxiv.org/abs/1608.03000) (EMNLP 2016).

---
![Model Diagram](https://raw.githubusercontent.com/nicholaslocascio/deep-regex/master/model5.png)
---

#### Summary
Our neural model translates natural language queries into regular expressions which embody their meaning. We model the problem as a sequence-to-sequence mapping task using attention-based LSTM's. Our model achieves a performance gain of 19.6% over previous state-of-the-art models.

We also present a methodology for collecting a large corpus of regular expression, natural language pairs using Mechanical Turk and grammar generation. We utilize this methology to create the `NL-RX` dataset.

This dataset is open and available in this repo.

## Installation

### Requirements
#### Python
`pip install -r requirements.txt`
#### Lua
1. Install torch (<http://torch.ch/docs/getting-started.html>)
2. Install packages:

```
luarocks install nn
luarocks install nngraph
luarocks install hdf5
```

## Usage
#### Training DeepRegex model
 * From `/deep-regex-model/`, run `bash train_single.sh $full_data_directory`

#### Evaluating DeepRegex model:
* From `/deep-regex-model/`, run `bash eval_single.sh $data_directory $model_file_name`

	* There are 3 valid `$full_data_directory` strings: 
		1. `data_kushman_eval_kushman`
		2. `data_turk_eval_turk`
		3. `data_synth_eval_synth`
	* There are 3 valid `$data_directory` strings (after training): 
		1. `data_kushman_eval_kushman/data_100`
		2. `data_turk_eval_turk/data_100`
		3. `data_synth_eval_synth/data_100`

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

## Data Generation
Code used to generate new data (Regexes and Synthetic Descriptions) is in `/data_gen/` folder.

#### To generate new data:
From `/data_gen/`, run `python generate_regex_data.py` to run the generation process described in the paper.


### Acknowledgments
*  Yoon Kim's [seq2seq-attn](https://github.com/harvardnlp/seq2seq-attn)
* Facebook's [torch](https://github.com/torch/torch7)

### Licence
MIT
