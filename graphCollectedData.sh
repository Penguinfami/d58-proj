#!/bin/bash

# Start time

## First test: ping 100 times
addrs=("10.0.0.1" "10.0.0.2")
wgetaddrs=("10.0.0.1" "10.0.0.2")

overallName=""
# ensure it is formatted
while getopts ":t:n:" opt; do
    case $opt in
        t)
            #shift $((OPTIND-1))
            overallName=$OPTARG
        ;;
        n)
            #shift $((OPTIND-1))
            numTests=$OPTARG
            echo "Number of files $numTests"
            ;;
        *)
            echo "Invalid option"
            shift $((OPTIND-1))
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

echo $overallName
testname=""
for addr in "${addrs[@]}"
do
    combinedPingFile="log/combinedPing_$overallName-$addr.txt"
    echo "" > $combinedPingFile

    combinedWGETFile="log/combinedWGET_$overallName-$addr.txt"
    echo "" > $combinedWGETFile
done

for i in `seq 1 $numTests`; do 
    testname=$1
    echo "Test:"
    echo $testname
    for addr in "${addrs[@]}"
    do
        echo $overallName

        # Run the ping command 100 times and save the output
        newPingFile="log/$testname-ping100times$addr.txt"

        newWgetFile="log/$testname-wget10times$addr.txt"

        python parseOutput.py ping "$newPingFile" "Culmulative time PING to $addr on network $testname" "Avg PING time ping to $addr on network $testname"
        python parseOutput.py wget "$newWgetFile" "Culmulative time WGET to $addr on network $testname"  "Avg WGET download speed from $addr on network $testname" "WGET times per 50KB from $addr on network $testname"
            
        combinedPingFile="log/combinedPing_$overallName-$addr.txt"
        combinedWGETFile="log/combinedWGET_$overallName-$addr.txt"

        cat $newPingFile >> $combinedPingFile 

        cat $newWgetFile >> $combinedWGETFile 
        echo "@@@@@@@@@@@@@@@@@@@@@@@" >> $combinedPingFile
        echo "@@@@@@@@@@@@@@@@@@@@@@@" >> $combinedWGETFile
    done
    shift
done

testname=""
for addr in "${addrs[@]}"
do
    combinedPingFile="log/combinedPing_$overallName-$addr.txt"
    combinedWGETFile="log/combinedWGET_$overallName-$addr.txt"
    echo $overallName

    python parseOutput.py comparePing "$combinedPingFile" "COMP Culm time PING to $addr on network $overallName" "COMP Avg PING time ping to $addr on network $overallName" 
    python parseOutput.py compareWget "$combinedWGETFile" "COMP Culm time WGET to $addr on network $overallName"  "COMP Avg WGET download speed from $addr for $overallName" "COMP WGET times per 50KB from $addr for $overallName"
done


