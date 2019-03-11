import glob
import time
import struct
from datetime import datetime
import pandas as pd
from dslog2csv.dslog2csv import DSLogParser
from analyzers.roborio_performance import RoborioPerformanceAnalyzer
from analyzers.current_usage import CurrentUsageAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import plotter

def read_event_name(filename):
    with open(filename, 'rb') as f:
        # First is junk
        f.read(39)
        length = struct.unpack('<B', f.read(1))[0]
        s = struct.unpack('<%ds' % length, f.read(length))
        s = s[0].strip().decode('ascii')[17:]
    return s


def load_analyzers():
    global analyzers
    #analyzers += [CurrentUsageAnalyzer()]
    analyzers += [RoborioPerformanceAnalyzer()]

def analyze(records):
    for analyzer in analyzers:
        analyzer.analyze(records)


def find_relevant_time(records):
    def find_consequtive_enabled(sequence):
        # Create an array that is 1 where a is 0, and pad each end with an extra 0.
        isone = np.concatenate(([0], np.equal(sequence, 1).view(np.int8), [0]))
        absdiff = np.abs(np.diff(isone))
        # Runs start and end where absdiff is 1.
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)

        ranges_size = np.asarray([r[1] - r[0] for r in ranges], dtype=np.int)
        
        # sometimes we see short disabled samples - I've only seen one disabled in a row for now, but ' \
        # the enabled contiues after that. I need to take that into account'

        return ranges[np.argmax(ranges_size)]

    # first lock on the first time voltage is measured
    irrelevant_voltage = np.where(records['voltage'] < 200)[0]
    start_index = irrelevant_voltage[0]
    # Then find 5 consequtive enabled period
    enabled = np.asarray([0 if r else 1 for r in records['robot_disabled']], dtype=np.int)
    enabled_period = find_consequtive_enabled(enabled[start_index:])
    enabled_period = [e + start_index for e in enabled_period]

    irrelevant_voltage = np.where(records['voltage'][enabled_period[0]:enabled_period[1]] > 200)[0]
    if irrelevant_voltage.size == 0:
        return enabled_period
    else:
        stop_index = irrelevant_voltage[0]
        return [enabled_period[0], stop_index]


def save_graph(filename):
    print("Reading data...", end="", flush=True)
    start = time.time()
    parser = DSLogParser(filename)
    records = parser.read_records()
    df = pd.DataFrame(records)
    elapsed = time.time() - start
    print("Done [Took %2.2f seconds]" % elapsed)

    print(read_event_name(logs_folder + events_filename))
    plotter.plot_all(df, save=True, show=True, log_name=filename)



logs_folder = 'C:/Users/Sketch Bros 2/Documents/Programming/frc-log-analyzer/Logs/White night 20190308/'
#logs_folder = 'Logs/White night 20190308/'
log_filename = '2019_03_08 03_34_49 Fri.dslog'
events_filename = log_filename.replace('dslog', 'dsevents')

analyzers = []

if __name__ == "__main__":
    # s = [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    # print(find_starting_point(s))

    # Set this to false if you want to see disabled periods
    IGNORE_DISBALED = True

    file = logs_folder + log_filename
    save_graph(file)
    # for file in glob.glob(logs_folder + '*.dslog'):
    #     print(file)
    #     save_graph(file)
    # print("Reading data...", end="", flush=True)
    # start = time.time()
    # parser = DSLogParser(logs_folder + log_filename)
    # records = parser.read_records()
    # df = pd.DataFrame(records)
    # elapsed = time.time() - start
    # print("Done [Took %2.2f seconds]" % elapsed)
    #
    # print(read_event_name(logs_folder + events_filename))
    # plotter.plot_all(df, logs_folder + log_filename)
    # relevant_period = find_relevant_time(df)
    #
    # load_analyzers()
    #
    # analyze(df)
