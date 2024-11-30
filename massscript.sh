#!/bin/bash

# Start time
start_time=$(date +%s)

# Run the ping command 100 times and save the output
ping -c 100 -i 0.000001 10.0.0.1 > h1toh1.txt

# End time
end_time=$(date +%s)

# Calculate elapsed time
elapsed_time=$((end_time - start_time))

# Log the elapsed time
echo "Ping test completed in $elapsed_time seconds." >> h1toh1.txt