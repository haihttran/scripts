time_start=`date "+%Y-%m-%d %H:%M:%S"`
start=$(date +%s)
echo $time_start

num_threads=24
v_path=/home/ubuntu/data/s3/04nov2022/5fps
s_path=/home/ubuntu/data/frames

mkdir $s_path


# parallel -j $num_threads "ffmpeg -i ${v_path}/{}.avi -strict -2 ${s_path}/{}.mp4" ::: `ls ${v_path} |cut -d. -f1`


# parallel -j $num_threads "ffmpeg -i ${v_path}/{}.mp4 \
# -q:v 4 -vf \"scale=trunc(((iw*256)/'min(iw,ih)')/2)*2:trunc(((ih*256)/'min(iw,ih)')/2)*2\" \
# -an -threads 1 -y -loglevel panic ${s_path}/{}/'img_%06d.jpg'" ::: `ls ${v_path} |cut -d. -f1`


# parallel -j $num_threads "mkdir ${s_path}/{};ffmpeg -i ${v_path}/{}.mpeg \
# -q:v 4 -vf \"scale=trunc(((iw*512)/'max(iw,ih)')/2)*2:trunc(((ih*5=12)/'max(iw,ih)')/2)*2\" \
# -an -threads 1 -y -loglevel panic ${s_path}/{}/'img_%05d.jpg'" ::: `ls ${v_path} |cut -d. -f1`

# parallel -j $num_threads "ffmpeg -i ${v_path}/{}.mpeg \
# -q:v 4 -vf \"scale=trunc(((iw*512)/'max(iw,ih)')/2)*2:trunc(((ih*512)/'max(iw,ih)')/2)*2\" \
# -an -threads 1 -y -loglevel panic ${s_path}/{}/'img_%06d.jpg'" ::: `ls ${v_path} |cut -d. -f1`


# parallel -j $num_threads "mkdir ${s_path}/${folder}/{};
# ffmpeg -i ${v_path}/${folder}/{}.mp4 -q:v 4  -an -threads 1 -y -loglevel panic 
# ${s_path}/${folder}/{}/'img_%05d.jpg'" ::: `ls ${v_path}/${folder} |cut -d. -f1`

# parallel -j $num_threads "mkdir ${s_path}/{};ffmpeg -i ${v_path}/{}.mp4 -q:v 4  -an -threads 1 -y -loglevel panic ${s_path}/{}/'img_%06d.jpg'" ::: `ls ${v_path} |cut -d. -f1`

parallel -j $num_threads "mkdir ${s_path}/{};ffmpeg -i ${v_path}/{}.mp4 -ss 1 -vf select='gte(n\, 0),fps=5' ${s_path}/{}/'image_%06d.jpg'" ::: `ls ${v_path} |cut -d. -f1`

time_end=`date "+%Y-%m-%d %H:%M:%S"`
end=$(date +%s)
echo $time_end
echo $(($end - $start))
