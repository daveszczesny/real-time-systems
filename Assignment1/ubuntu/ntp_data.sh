#!/bin/bash

sleep 5

# Define the NTP servers to query
NTP_SERVERS=("1.ie.pool.ntp.org" "0.uk.pool.ntp.org" "0.europe.pool.ntp.org" "1.europe.pool.ntp.org" "0.us.pool.ntp.org" "0.au.pool.ntp.org" "0.asia.pool.ntp.org")

# Output file
OUTPUT_FILE="./ntp/ntp_info.csv"

# Header for CSV file
echo "timestamp,server,offset,delay,jitter" > $OUTPUT_FILE

# Function to collect data
collect_ntp_data() {
    local server=$1
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    # Run ntpq -p and extract offset, delay, jitter
    ntpq -pn $server | awk -v time="$timestamp" -v srv="$server" \
        'NR>2 {print time "," srv "," $9 "," $8 "," $10}' >> $OUTPUT_FILE
}

# Run every 20 minutes for ~8-12 hours
END_TIME=$((SECONDS + 8 * 60 * 60))  # Change to 8 * 60 * 60 for 8 hours
while [ $SECONDS -lt $END_TIME ]; do
    for server in "${NTP_SERVERS[@]}"; do
        collect_ntp_data "$server"
    done
    sleep 1200  # 20 minutes
done

echo "Data collection complete. Results saved in $OUTPUT_FILE"