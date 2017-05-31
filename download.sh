#!/bin/bash

wget -c -O train.zip "https://publicqn.saikr.com/3f96bef8dcbbf57605db3f5e79d5384e1495175270342.zip?attname=dsjtzs_txfz_training.txt.zip"
wget -c -O test.zip "https://publicqn.saikr.com/b4d50fbf55ed071e2bcdbf6448ee5caa1495681365947.zip?attname=dsjtzs_txfz_test1.txt.zip"
unzip train.zip
unzip test.zip
mv __MACOSX/dsjtzs_txfz_test1.txt mouse_test.txt
mv __MACOSX/dsjtzs_txfz_training.txt mouse_training.txt
rm -rf __MACOSX
rm -f train.zip test.zip
