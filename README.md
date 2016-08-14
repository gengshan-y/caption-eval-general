# caption-eval-general

Caption evaluation code simplied from COCO dataset evaluation tool.

There are three pieces of codes here:

1. languageEval_sent_list.py taks in the prediction and reference text file and
   generate scores.

   e.g.: `python languageEval_sent_list.py -i data/pred.txt -r data/ref.txt`
 
2. languageEval_sent_list.ipynb is the ipython notebook version of 1.

3. languageEval_withID.ipynb can take the formatted data as follows:
   `id<TAB>sentences`
