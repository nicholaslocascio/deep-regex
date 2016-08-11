#!/bin/bash
data_dir=$1

echo "Running for data directory named: '$data_dir'"

python preprocess.py --srcfile $data_dir/src-train.txt --targetfile $data_dir/targ-train.txt --srcvalfile $data_dir/src-val.txt --targetvalfile $data_dir/targ-val.txt --outputfile $data_dir/demo

# th train.lua -data_file $data_dir/demo-train.hdf5 \
#     -val_data_file $data_dir/demo-val.hdf5 \
#     -savefile $data_dir/model

th train.lua -data_file $data_dir/demo-train_1.0.hdf5 \
    -val_data_file $data_dir/demo-val.hdf5 \
    -savefile $data_dir/model

echo "bye:-)"