import plotter
import numpy as np
import matplotlib.pyplot as plt
from analyzers.analyzer import Analyzer

class CurrentUsageAnalyzer(Analyzer):

    def analyze(self, records):
        self.out("Analyzing power consumption")

        low_voltage = np.where(records['voltage'] < 8)[0]
        if len(low_voltage) > 0:
            strings = ["Low voltage at %s" % r for r in records['time'][low_voltage]]
            self.out(strings)

        plotter.plot_voltage_current(records)
        #
        # 'pdp_0', 'pdp_1', 'pdp_2', 'pdp_3', 'pdp_4', 'pdp_5', 'pdp_6', 'pdp_7',
        # 'pdp_8', 'pdp_9', 'pdp_10', 'pdp_11', 'pdp_12', 'pdp_13', 'pdp_14', 'pdp_15',
        # 'pdp_total_current',
        # pdp_id
        # if len(high_can_usage) > 0:
        #

        self.out("Analysis complete")
