import plotter
import numpy as np
import matplotlib.pyplot as plt

class RoborioPerformanceAnalyzer:

    def out(self, message):
        if isinstance(message, list):
            for s in message:
                self.out(s)
        else:
            print(message)

    def analyze(self, records):
        self.out("Analyzing roborio performance")

        high_cpu = np.where(records['rio_cpu'] > 0.5)[0]
        if len(high_cpu ) > 0:
            strings = ["High CPU detected at %s" % r for r in records['time'][high_cpu]]
            self.out(strings)

        watchdog = np.where(records['watchdog'] == True)[0]
        if len(watchdog) > 0:
            strings = ["Watchdog issue at %s" % r for r in records['time'][watchdog]]
            self.out(strings)

        brownouts = np.where(records['brownout'] == True)[0]
        if len(brownouts) > 0:
            strings = ["Brownout detected at %s" % r for r in records['time'][brownouts]]
            self.out(strings)
            plt.figure(1)
            # Plot the data
            voltage_color = 'red'
            brownout_color = 'brown'
            fig, ax1 = plt.subplots()
            # Plot the data
            ax1.plot(records['time'], records['voltage'], color=voltage_color)
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Voltage', color=voltage_color)
            ax1.tick_params(axis='y', labelcolor=voltage_color)
            ax2 = ax1.twinx()
            ax2.plot(records['time'], records['brownout'], color=brownout_color)
            ax2.set_ylabel('Brownout', color=brownout_color)
            ax2.tick_params(axis='y', labelcolor=brownout_color)

            plotter.make_frc_plot('Brownouts', records)
            plt.show()

        high_can_usage = np.where(records['can_usage'] > 0.9)[0]
        if len(high_can_usage) > 0:
            self.out(["High CAN usage detected at %s" % r for r in records['time'][high_can_usage]])
            plt.figure(1)
            # Plot the data
            plt.plot(records['time'], records['can_usage'], 'k-')
            plt.ylim((0, 1))

            plotter.make_frc_plot('CAN Usage', records)
            plt.show()

        # plotter.plot_frc_log('Roborio Performance', records, 'time', 'brownout')

        self.out("Analysis complete")
