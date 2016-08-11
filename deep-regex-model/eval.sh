data_dir=$1
fractions=(10 25 50 75 100 618)

for train_fraction in "${fractions[@]}"; do
    data_path=$data_dir/data_$train_fraction
    th beam.lua -model $data_path/model_final.t7 -src_file $data_path/src-val.txt -output_file $data_path/pred.txt -src_dict $data_path/out_demo.src.dict -targ_dict $data_path/demo.targ.dict -targ_file $data_path/targ-val.txt > $data_path/output_log.txt
done;
