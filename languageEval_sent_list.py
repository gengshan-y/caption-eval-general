# encoding: utf-8

import matplotlib 
matplotlib.use('Agg')  # to solve the backend problem when there's no GUI
import sys 
import argparse
sys.path.append('./coco-caption/') 
from pycocotools.coco import COCO 
from pycocoevalcap.eval import COCOEvalCap 
from captionLoader import *  # loading sentences to coco-json

''' Parsing arguments '''
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile", type=str, required=True,
                    help='File containing generated/hypothesis sentences.')
parser.add_argument("-r", "--references", type=str, required=True,
                    help='File containing references/groundtruth sentences.')
args = parser.parse_args()
reference_file = args.references
prediction_file = args.inputfile

''' Assigning output json path '''
reference_json = '{0}.json'.format(reference_file)
prediction_json = '{0}.json'.format(prediction_file)

''' load reference and predicts '''
ref = CocoAnnotations()
ref.read_file(reference_file)
ref.dump_json(reference_json)

pred = CocoResFormat()
pred.read_file(prediction_file)
pred.dump_json(prediction_json)

''' create coco object and cocoRes object '''
coco = COCO(reference_json)
cocoRes = coco.loadRes(prediction_json)

''' create cocoEval object '''
cocoEval = COCOEvalCap(coco, cocoRes)

''' evaluate results '''
cocoEval.evaluate()

''' print output evaluation scores '''
for metric, score in cocoEval.eval.items():
    print '%s: %.3f'%(metric, score)
