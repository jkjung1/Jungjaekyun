import os
import sys
import argparse

CRName = sys.argv[1]

auto_log_dir = 'E:/03.project/tc_manager/RegressionTest_LOG_AUTO'
manual_log_dir = 'E:/03.project/tc_manager/REgressionTest_LOG' + CRName

try:
    if not os.path.exists(manual_log_dir):
        os.makedirs(manual_log_dir)
except OSError:
    print('Error: Creating LOG directory. ' + manual_log_dir)
    
    # if CSV files exist, remove the CSV files in MANUAL LOG DIR
    filelist = os.listdir(manual_log_dir)
    for file in filelist:
        if os.path.isfile(manual_log_dir + '/' + file):
            if 'csv' in file or 'CSV' in file:
                os.remove(manual_log_dir + '/' + file)
                
# create new CSV file by using TXT files in AUTO LOG DIR
for (path, dir, files) in os.walk(auto_log_dir + CRName):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.txt':
            if '\\' in path:
                new_csv_file = open(manual_log_dir + '/' + path.split('\\')[1] + '.CSV', 'a')
                new_csv_file.writelines(filename + '\n')
                new_csv_file.close()