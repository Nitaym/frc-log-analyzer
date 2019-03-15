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
import utils
import os

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


def generate_graph(dslog, eventlog):
    print("Reading data...", end="", flush=True)
    start = time.time()
    parser = DSLogParser(dslog)
    records = parser.read_records()
    df = pd.DataFrame(records)
    elapsed = time.time() - start
    print("Done [Took %2.2f seconds]" % elapsed)

    print(utils.read_event_name(eventlog))
    plotter.plot_all(df, save=True, show=True, log_name=os.path.split(dslog)[1])



logs_folder = 'f:/Users/Nitay/Dropbox/Work/First FRC/2019/Logs/District 4/Day 2/'
#logs_folder = 'Logs/White night 20190308/'
logs_filenames = [
    'Elimination-19_1__2019_03_14 16_48_33 Thu.dslog',
    'Elimination-19_1__2019_03_14 17_12_07 Thu.dslog',
    'Elimination-20_1__2019_03_14 17_13_39 Thu.dslog',
    'Elimination-21_1__2019_03_14 17_23_35 Thu.dslog',
]
events_filenames = [s.replace('dslog', 'dsevents') for s in logs_filenames]

analyzers = []

if __name__ == "__main__":
    # s = [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    # print(find_starting_point(s))

    # Set this to false if you want to see disabled periods
    IGNORE_DISBALED = True

    for dslog, event_log in zip(logs_filenames, events_filenames):
        generate_graph(logs_folder + dslog, logs_folder + event_log)
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
