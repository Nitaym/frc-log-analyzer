import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


global_event_name = ''

def set_event_name(event_name):
    global global_event_name
    global_event_name = event_name

def plot_voltage_current(records):
    voltage_color = 'red'
    current_color = 'blue'
    fig, ax1 = plt.subplots()
    # Plot the data
    ax1.plot(records['time'], records['voltage'], color=voltage_color)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage', color=voltage_color)
    ax1.tick_params(axis='y', labelcolor=voltage_color)
    ax2 = ax1.twinx()
    ax2.plot(records['time'], records['pdp_total_current'], color=current_color)
    ax2.set_ylabel('PDP Total Current', color=current_color)
    ax2.tick_params(axis='y', labelcolor=current_color)

    make_frc_plot('Voltage vs Current', records)
    plt.show()


def plot_all(records):
    names = ['0 ',
             '1 Drive',
             '2 Drive',
             '3 Drive',
             '4 Climb Leg',
             '5 Arm',
             '6 ?',
             '7 --Arm--',
             '8 ?',
             '9 Elevator',
             '10 Collector',
             '11 Climb Leg',
             '12 Drive',
             '13 Drive',
             '14 Drive',
             '15 Spare']
    for i in range(16):
        voltage_color = 'red'
        current_color = 'blue'
        ax1 = plt.subplot(4, 4, i+1)
        # Plot the data
        ax1.plot(records['time'], records['voltage'], color=voltage_color)
        # ax1.set_xlabel('Time')
        # ax1.set_ylabel('Voltage', color=voltage_color)
        ax1.tick_params(axis='y', labelcolor=voltage_color)
        ax2 = ax1.twinx()

        currents = records['pdp_currents']
        current = [c[i] for c in currents]
        ax2.plot(records['time'], current, color=current_color)
        ax2.set_ylabel(names[i], color=current_color)
        ax2.tick_params(axis='y', labelcolor=current_color)

        # make_frc_plot('Voltage vs Current', records)

    plt.show()


def plot_voltage_current_specific(records, pdp_number, pdp_name):
    voltage_color = 'red'
    current_color = 'blue'
    fig, ax1 = plt.subplots()
    # Plot the data
    ax1.plot(records['time'], records['voltage'], color=voltage_color)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Voltage', color=voltage_color)
    ax1.tick_params(axis='y', labelcolor=voltage_color)
    ax2 = ax1.twinx()

    currents = records['pdp_currents']
    current = [c[5] for c in currents]
    ax2.plot(records['time'], current, color=current_color)
    ax2.set_ylabel(pdp_name + '(%d)' % pdp_number, color=current_color)
    ax2.tick_params(axis='y', labelcolor=current_color)

    make_frc_plot('Voltage vs Current', records)
    #plt.show()


def make_frc_plot(plot_title, records):
    plt.title(global_event_name + ' - ' + plot_title)

    # Add coloring for robot disabled, robot browned out, watchdog, ds_disabled
    # Get the background color right - First create the target background color array
    disabled = np.asarray([1 if r else 0 for r in records['robot_disabled']], dtype=np.int)
    # That's pretty much the same as transpose
    disabled = np.vstack((disabled,))
    # Get the colors ordering right
    disabled = 1 - disabled
    # Paint
    plt.imshow(disabled, extent=(plt.xlim()[0],plt.xlim()[1], plt.ylim()[0],plt.ylim()[1]), cmap=plt.cm.RdYlGn, alpha=0.1, aspect='auto')
