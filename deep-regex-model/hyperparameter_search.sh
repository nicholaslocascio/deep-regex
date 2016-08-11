lr=$1
batch_sizes=(32 64)
dropouts=(0.1 0.25)
n_layers=(2 3)
data_dir="mturk_full_data_proper_hyper"

cp -rf $data_dir ${data_dir}_temp;

for batch_size in "${batch_sizes[@]}"; do
    for dropout in "${dropouts[@]}"; do
        for n_layer in "${n_layers[@]}"; do
            new_file_name=hyper_${lr}_${batch_size}_${dropout}_${n_layer}
            cp -rf ${data_dir}_temp $new_file_name; mv $new_file_name $data_dir;
        done;
    done;
done;

rm -rf ${data_dir}_temp

for batch_size in "${batch_sizes[@]}"; do
    for dropout in "${dropouts[@]}"; do
        for n_layer in "${n_layers[@]}"; do
            new_file_name=hyper_${lr}_${batch_size}_${dropout}_${n_layer}
            data_path=${data_dir}/$new_file_name
            python preprocess.py --srcfile $data_path/src-train.txt --targetfile $data_path/targ-train.txt --srcvalfile $data_path/src-val.txt --targetvalfile $data_path/targ-val.txt --outputfile $data_path/out_demo --batchsize $batch_size;
        done;
    done;
done;

for batch_size in "${batch_sizes[@]}"; do
    for dropout in "${dropouts[@]}"; do
        for n_layer in "${n_layers[@]}"; do
            new_file_name=hyper_${lr}_${batch_size}_${dropout}_${n_layer}
            echo $new_file_name
            data_path=${data_dir}/$new_file_name
            th train.lua -data_file $data_path/out_demo-train.hdf5 -val_data_file $data_path/out_demo-train.hdf5 -savefile $data_path/model -learning_rate $lr -num_layers $n_layer -dropout $dropout > $data_path/log_file.txt &
        done;
    done;
done;

