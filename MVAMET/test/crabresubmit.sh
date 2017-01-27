#!bin/bash
dir=/storage/jbod/nzaeh/2017-01-24
for i in $( ls $dir | grep crab); do
	crab resubmit --maxmemory=7000 --maxjobruntime=3000 $dir/$i
done

