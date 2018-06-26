import numpy
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
from collections import defaultdict
from io import StringIO
from ..config import *

# following code used to resolve the problem as
# UserWarning: This call to matplotlib.use() has no effect 
# because the backend has already been chosen; 
# matplotlib.use() must be called *before* pylab, 
# matplotlib.pyplot, or matplotlib.backends is imported for the first time.
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
# sys.path.append("..")
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


class extract_frame:
    def __init__(self, **kwargs):
        if tf.__version__ < '1.4.0':
            raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
        params = dict(kwargs)
        self.image_name = params['image_name']
        self.model_name = params['model_name']
    
    def loadmodel(self):
        
        # model_file = self.model_name+'.tar.gz'
        model_file = os.path.join(MODEL_FOLDER, self.model_name+'.tar.gz')
        print(f'the model file is {model_file}')
        image_file = os.path.join(UPLOAD_FOLDER, self.image_name)
        print(f'the image file is {image_file}')
        tar_file = tarfile.open(model_file)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pbr3' in file_name:
                tar_file.extract(file, os.getcwd())
        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        PATH_TO_CKPT = self.model_name + '/frozen_inference_graph.pb'
        # List of the strings that is used to add correct label for each box.
        PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
        NUM_CLASSES = 90
        print('1')
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        print('1')
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        print(label_map)
