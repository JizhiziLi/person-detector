#!/bin/bash
source activate persondetector
cd person_detector/static/
cd batch_images/validate_result
open .
cd ../../
cd batch_images/validate_test
open .
cd ../../
cd single_image/original
open .
cd ../../
cd single_image/processed
open .
cd ../../../../
open /Applications/Postman.app
python run.py


