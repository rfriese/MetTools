#!bin/bash
dir=/storage/jbod/nzaeh/2017-02-02
for i in $( ls $dir | grep crab); do
	crab resubmit --maxmemory=10000 --maxjobruntime=3000 $dir/$i
done

