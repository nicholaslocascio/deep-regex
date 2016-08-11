data_dir=$1
model_name=$2

if [ ! -z $3 ]
then
    src_file=$3
else
    src_file=$data_dir/src-val.txt
fi

if [ ! -z $4 ]
then
    targ_file=$4
else
    targ_file=$data_dir/targ-val.txt
fi

th beam.lua -model $data_dir/$model_name -src_file $src_file -output_file $data_dir/pred.txt -src_dict $data_dir/out_demo.src.dict -targ_dict $data_dir/out_demo.targ.dict -targ_file $targ_file
