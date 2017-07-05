#! /bin/bash

line=$1
f_links='links.data'
f_job='job.data'


src=$(awk '{FS="\t"}FNR=='$line'{print $2}' $f_links)
dest=$(awk '{FS="\t"}FNR=='$line'{print $3}' $f_links)
trans_type=$(awk '{FS="\t"}FNR=='$line'{print $4}' $f_links)
interval=$(awk '{FS="\t"}FNR=='$line'{print $5}' $f_links)
interval_persist=$interval

rclone -v $trans_type $src $dest &> $f_job
echo "$(date +"%T") Copying..."

i=0
while :; do
	minute=$(date +"%-M")
	hour=$(date +"%-H")
	total_mins=$((minute + (60 * hour)))

	if ((total_mins % interval == 0)); then
		rclone -v $trans_type $src $dest &> $f_job
		echo "$(date +"%T") Copying..."

		if grep -e ': Copied (new)' -e': Copied (replaced existing)' -e ': Deleted' "$f_job" --quiet;then
			echo "$(date +"%T") Change(s) detected..."
			echo "$(date +"%T") Entering heightened state!"
			echo "$(date +"%T") Checks occurring every minute."
			interval=1
			i=1
		elif ((i >= 13)); then
			echo "$(date +"%T") Leaving heightened state."
			echo "$(date +"%T") Checks occurring at normal intervals."
			interval=$(awk '{FS="\t"}FNR=='$line'{print $5}' $f_links)
			i=0
		elif ((i >= 10)) && ((interval_persist != 1)); then
			echo "$(date +"%T") Checks reduced to every other minute."
			interval=2
			((i++))
		elif ((i > 0)); then
			((i++))
		fi

	fi
	sleep 1m

done




