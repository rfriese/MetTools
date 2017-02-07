#!bin/bash
dir=/storage/jbod/nzaeh/2017-02-02
for i in $( ls $dir | grep crab); do
	crab status $dir/$i
done

