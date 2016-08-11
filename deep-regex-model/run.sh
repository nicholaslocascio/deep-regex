data_dir=$1
fractions=(10 25 50 75 90 100 618)
fractionsstr="10 25 50 75 90 100"
python split_data_into_size_subfolders.py --data_dir $data_dir --splits $fractionsstr

for train_fraction in "${fractions[@]}"; do
    data_path=$data_dir/data_$train_fraction
    python preprocess.py --srcfile $data_path/src-train.txt --targetfile $data_path/targ-train.txt --srcvalfile $data_path/src-val.txt --targetvalfile $data_path/targ-val.txt --outputfile $data_path/out_demo;
done;

for train_fraction in "${fractions[@]}"; do
    data_path=$data_dir/data_$train_fraction
    th train.lua -data_file $data_path/out_demo-train.hdf5 -val_data_file $data_path/out_demo-train.hdf5 -savefile $data_path/model &
done;
