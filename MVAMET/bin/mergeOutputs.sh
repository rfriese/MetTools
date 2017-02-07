#!/bin/bash
gridname=/storage/jbod/nzaeh/2017-02-02/
names=$(find $gridname -name "slimmed.root" | grep mad)
	hadd -f $gridname/shrinkedDataTotMad.root $names
names=$(find $gridname -name "slimmed.root")
	hadd -f $gridname/shrinkedDataTotMad.root $names
