#!bin/bash
dir=/storage/jbod/nzaeh/2017-01-24
for i in $( ls $dir | grep crab); do
	crab status $dir/$i
done

