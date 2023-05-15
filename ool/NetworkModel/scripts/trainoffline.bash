#!/usr/bin/env bash

CONGESTION_TEST="python /App/mininettest/congestiontest.py --train";
WEIGHT_FILE="/App/offline_agent/blank_weights.h5f"

usage(){
    echo "train.bash <delta_rtt> <steps> [allowed_congestion]"
}

main(){
    echo "$1","$2","$3"
    if [ -z $3 ]
    then
    ALLOWED=0
    else
    ALLOWED=$3
    fi

    MAX_STEPS=$2
    STEPS=0
    rm -rf /App/output/train_$1/
    mkdir -p /App/output/train_$1/

    python /App/offline_agent/trainModel.py /App/output/50302640/aggregated_$1.csv
    WEIGHT_FILE=$(ls $PWD/weight*)
    
    mv $WEIGHT_FILE /App/output/train_$1/
}

if [ $# -ge 2 ]
then
    main $1 $2 $3
else
    usage
fi
