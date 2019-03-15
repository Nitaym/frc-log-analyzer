import utils
import glob
import os

#logs_folder = 'C:/Users/Sketch Bros 2/Documents/Programming/frc-log-analyzer/Logs/White night 20190308/'
logs_folder = 'f:/Users/Nitay/Dropbox/Work/First FRC/2019/Logs/District 4/Day 2/'
#logs_folder = 'Logs/White night 20190308/'
log_filename = '2019_03_08 03_34_49 Fri.dslog'
events_filename = log_filename.replace('dslog', 'dsevents')


if __name__ == "__main__":
    needed_files = []

    for file in glob.glob(logs_folder + '*.dsevents'):
        # print(file)
        s = utils.read_event_name(file)
        if 'FMS Connected:' in s:
            s = s[17:]
            needed_files += [(file, s)]
            print(s)


    for (file, event) in needed_files:
        (dir, filename) = os.path.split(file)
        if filename.startswith('Elimi') or filename.startswith('Qual'):
            continue
        s = event[:event.find('Field Time:') - 2].replace(':', '_').replace(' ', '')
        # print(dir + '/%s__%s' % (s, filename))
        os.rename(file, dir + '/%s__%s' % (s, filename))
        file = file.replace('dsevents', 'dslog')
        filename = filename.replace('dsevents', 'dslog')
        os.rename(file, dir + '/%s__%s' % (s, filename))