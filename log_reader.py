import numpy as np
import struct
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from dslog2csv import DSLogParser

def read_event_name(filename):
    with open(filename, 'rb') as f:
        # First is junk
        f.read(39)
        length = struct.unpack('<B', f.read(1))[0]
        s = struct.unpack('<%ds' % length, f.read(length))
        s = s[0].strip().decode('ascii')[17:]
    return s


logs_folder = 'f:/Users/Nitay/Dropbox/Work/First FRC/2019/Logs/District 1/Day 1/'
log_filename = '2019_03_04 14_43_21 Mon.dslog'
events_filename = log_filename.replace('dslog', 'dsevents')

if __name__ == "__main__":
    parser = DSLogParser(logs_folder + log_filename)
    records = parser.read_records()

    print(read_event_name(logs_folder + events_filename))

    #voltage = [[r['time'], r['voltage'], r['robot_disabled'], r['brownout']] for r in records]
    df = pd.DataFrame(records)
    plt.figure(1)

    x = df['time']
    y = df['rio_cpu']

    # Interesting logs:
    # 1. CPU
    # 2. PDP Usage
    # 3. Brownouts, disabled problems, states

    #Add coloring for robot disabled, robot browned out, watchdog, ds_disabled

    # Get the background color right - First create the target background color array
    disabled = np.asarray([1 if r else 0 for r in df['robot_disabled']], dtype=np.int)
    # That's pretty much the same as traspose
    disabled = np.vstack((disabled,))
    # Get the colors ordering right
    disabled = 1 - disabled
    # Paint
    plt.imshow(disabled, extent=(min(x),max(x), min(y),max(y)), cmap=plt.cm.RdYlGn, alpha=0.1, aspect='auto')

    ax = plt.plot(x, y, 'k-')
    plt.waitforbuttonpress()

    print(y)

