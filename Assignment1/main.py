import json
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

"""

====
timestamp
====
remote refid st t when poll reach delay offset jitter
====
values
values
values

====
timestamp
etc...

"""

def parse_ntpq_output(filename: str):
    with open(filename, 'r') as f:
        lines = f.readlines()

    entries = {}
    timestamp = None
    headings = []

    for line in lines:
        # if line is '=====' skip the line
        if line.startswith('====') or line == '\n':
            continue

        # if line contains 'Time' this marks the start of a new entry
        if line.startswith('Time'):
            timestamp = line.strip()
            entries[timestamp] = {}
            continue

        # headings line
        if 'remote' in line:
            # capture all the headings
            headings = line.strip().split()
            # assign them to entries[timestamp]
            if timestamp:
                for heading in headings:
                    entries[timestamp][heading] = []
            continue

        # values line
        values = line.strip().split()
        if timestamp:
            for i, heading in enumerate(headings):
                if i < len(values):
                    entries[timestamp][heading].append(values[i])
                else:
                    entries[timestamp][heading].append('')

    return entries

def get_attr_for_ip(entries, ip_address):
    ip_attrs = {}
    for timestamp, data in entries.items():
        if ip_address in data['remote']:
            index = data['remote'].index(ip_address)
            ip_attrs[timestamp] = {heading: data[heading][index] for heading in data}
    return ip_attrs

def caclulate_stats(values):
    values = np.array(values, dtype=float)
    return {
        'mean': np.mean(values),
        'std': np.std(values),
        'min': np.min(values),
        'max': np.max(values)
    }

def plot_ip_attributes(ip_attrs, ip_address):
    timestamps = []
    delays = []
    offsets = []
    jitters = []

    for timestamp, attrs in ip_attrs.items():
        timestamps.append(datetime.strptime(timestamp.split(": ")[1], '%d/%m/%Y %H:%M:%S.%f'))
        delays.append(float(attrs['delay']))
        offsets.append(float(attrs['offset']))
        jitters.append(float(attrs['jitter']))

    delay_stats = caclulate_stats(delays)
    offset_stats = caclulate_stats(offsets)
    jitter_stats = caclulate_stats(jitters)

    print(f"Delay stats for {ip_address}: {json.dumps(delay_stats, indent=4)}")
    print(f"Offset stats for {ip_address}: {json.dumps(offset_stats, indent=4)}")
    print(f"Jitter stats for {ip_address}: {json.dumps(jitter_stats, indent=4)}")
    
    plt.figure(figsize=(12, 6))


    plt.subplot(3,1,1)
    plt.plot(timestamps, delays, label='Delay')
    plt.xlabel('Timestamp')
    plt.ylabel('Delay')
    plt.title(f'Delay for {ip_address}')
    plt.legend()

    plt.subplot(3,1,2)
    plt.plot(timestamps, offsets, label='Offset')
    plt.xlabel('Timestamp')
    plt.ylabel('Offset')
    plt.title(f'Offset for {ip_address}')
    plt.legend()

    plt.subplot(3,1,3)
    plt.plot(timestamps, jitters, label='Jitter')
    plt.xlabel('Timestamp')
    plt.ylabel('Jitter')
    plt.title(f'Jitter for {ip_address}')
    plt.legend()

    plt.tight_layout()
    plt.show()





if __name__ == '__main__':
    filename = 'log.txt'
    entries = parse_ntpq_output(filename)
    # print(json.dumps(entries, indent=4))

    
    ip_addresses = [
        '123.123.123.123',
        '66.123.123.123'
    ]

    for ip in ip_addresses:
        ip_attrs = get_attr_for_ip(entries, ip)
        print(json.dumps(ip_attrs, indent=4))
        plot_ip_attributes(ip_attrs, ip)


    # to capture the properties from a single ip address, we can simply get its index in entries
