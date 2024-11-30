#!/bin/bash

# Start time

## First test: ping 100 times
addrs=("10.0.0.1" "10.0.0.2")
wgetaddrs=("10.0.0.1" "10.0.0.2")
testname=$1
summaryFile="summary.txt"
for addr in "${addrs[@]}"
do
    start_time=$(date +%s)

    # Run the ping command 100 times and save the output
    newPingFile="log/$testname-ping100times$addr.txt"

    ping -c 100 $addr > "$newPingFile"

    # End time
    end_time=$(date +%s)

    # Calculate elapsed time
    elapsed_time=$((end_time - start_time))

    # Log the elapsed time
    echo "Ping test completed in $elapsed_time seconds." >> "$newPingFile"
    
    ## TODO: more realistic tasks, like downloading
    wgetfilename="testwget.html"
    newWgetFile="log/$testname-wget10times$addr.txt"
    wgetList=""
    for i in `seq 1 3`; do 
    wgetList="$wgetList $addr"
    done
    #echo "$wgetList" > testwgetlist.txt
    wget --timeout=30 -t 10 --limit-rate=0 -O $wgetfilename -o $newWgetFile $wgetList

    end_time=$(date +%s)
    elapsed_time=$((end_time - start_time))
    echo "All tests run for address $addr completed in $elapsed_time seconds." >> "$summaryFile"
    
    #python parseOutput.py ping "$newPingFile" "Culmulative time PING to $addr on network $testname" "Average PING time ping to $addr on network $testname"
    #python parseOutput.py wget "$newWgetFile" "Culmulative time WGET to $addr on network $testname" "Average WGET time ping to $addr on network $testname"
done
