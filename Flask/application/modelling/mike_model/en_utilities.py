# #This module contains a bunch of utility functions for
# use in processing timeseries data, load profiles, etc.
# import utility_module as um

import pandas as pd
# import win32api
# import win32com.client
# import pythoncom
# # import io
# from pytz import UTC
# from pytz import timezone
import datetime as dt
import numpy as np
import logging
import os
import time
# import matplotlib as mpl
# import matplotlib.pyplot as plt
import subprocess
# import matplotlib.dates as mdates
# import pdb, traceback, sys
# import calendar
# import pytz
# import seaborn as sns
import sys
import shutil
import traceback
import warnings
import sys


def warn_with_traceback(message, category, filename, lineno, file=None, line=None):
    log = file if hasattr(file, 'write') else sys.stderr
    traceback.print_stack(file=log)
    log.write(warnings.formatwarning(message, category, filename, lineno, line))


def setup_logging(py_name, label=''):
    log_folder = "C:\\PYTHONprojects\\py_logfiles"
    py_root = os.path.splitext(py_name)[0]
    log_dir = os.path.join(log_folder, py_root)

    runtime = dt.datetime.now()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_name = "python_logfile_" + label + \
               "_" + str(runtime.year) + \
               "_" + str(runtime.month).zfill(2) + \
               "_" + str(runtime.day).zfill(2) + \
               "_" + str(runtime.hour).zfill(2) + \
               str(runtime.minute).zfill(2) + \
               str(runtime.second).zfill(2) + \
               ".txt"

    log_path = os.path.join(log_dir, log_name)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_path,
        filemode='w',
        format='%(asctime)s %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')

    logging.info('Python Script is: %s', py_name)


def setup_local_logging(root_path, py_name, label=''):
    # Set up logfile adjacent to script directory
    log_dir = os.path.join(root_path, 'py_logfiles')

    runtime = dt.datetime.now()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_name = "python_logfile_" + label + \
               "_" + str(runtime.year) + \
               "_" + str(runtime.month).zfill(2) + \
               "_" + str(runtime.day).zfill(2) + \
               "_" + str(runtime.hour).zfill(2) + \
               str(runtime.minute).zfill(2) + \
               str(runtime.second).zfill(2) + \
               ".txt"

    log_path = os.path.join(log_dir, log_name)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_path,
        filemode='w',
        format='%(asctime)s %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p')

    logging.info('Python Script is: %s', py_name)


def reshape_profile(df):
    # take an annual load profile organised as a single column df with column 'kW'
    # and returns a df with rows indexed by date, and columns by time (decimal hours)

    # so as to leave the original DataFrame intact
    df_copy = df.copy()
    df_copy.index = [df.index.date, df.index.hour + df.index.minute / 60]
    return df_copy['kW'].unstack()


def reshape_profile_gen(df, column):
    # More generalised version of reshape_profile that takes column name as well
    # takes an annual load profile organised as a single column df with column 'kW'
    # and returns a df with rows indexed by date, and columns by time (decimal hours)

    # so as to leave the original DataFrame intact
    df_copy = df.copy()
    df_copy.index = [df.index.time, df.index.date]
    return df_copy[column].unstack()


def shift_tz(df):
    # Acts on a reshaped df time series with time as index, dates as columns
    # and does a crude timezone shift including DST
    year = df.columns[0].year
    dst_start = pd.to_datetime(dt.datetime(year, 10, 1))
    dst_end = pd.to_datetime(dt.datetime(year, 4, 1))
    # ...... tbc


# TODO Work out if the complex version is helpful.
def df_to_csv(df, path):
    """Writes data frame to .csv, first closing the .csv if it's open elsewhere."""
    # tries to save a df to a csv file,
    # traps io error and if the file is open elsewhere, closes the file
    # Adapted from
    # http: // timgolden.me.uk / python / win32_how_do_i / see - if -an - excel - workbook - is -open.html

    df.to_csv(path)

    # try:
    #     df.to_csv(path)
    #     logging.info('saved to %s', path)
    #     pass
    #
    # except IOError:
    #     context = pythoncom.CreateBindCtx(0)
    #     for moniker in pythoncom.GetRunningObjectTable():
    #         name = moniker.GetDisplayName(context, None)
    #         if name == path:
    #             obj = win32com.client.GetObject(path)
    #             obj.Close(True)
    #     df.to_csv(path)


def find_between(s, first, last):
    # find string between 2 substrings
    # from https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def plot_tariffs(
        path='C:\\Users\\z5044992\\Documents\\MainDATA\\DATA_EN_3\\reference',
        filename='static_import_tariffs.csv',
        tariff_list=['all']):

    """Plot a chart of price vs time for weekday and weekend."""
    plot_path = os.path.join(path, 'tariff_plots')
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    # Use static import and export tariffs saved in en reference folder
    # -----------------------------------------------------------------
    file = os.path.join(path, filename)
    data = pd.read_csv(file, parse_dates=['timestamp'], index_col='timestamp')
    if tariff_list != ['all']:
        data = data[tariff_list]

    # Average over weekday or weekend
    df = {}
    data['time'] = data.index.hour + data.index.minute / 60
    df['weekday'] = data.loc[data.index.weekday.isin([0, 1, 2, 3, 4])]
    df['weekend'] = data.loc[data.index.weekday.isin([5, 6])]
    df['weekday'] = df['weekday'].groupby([df['weekday'].index.hour, df['weekday'].index.minute]).mean()
    df['weekend'] = df['weekend'].groupby([df['weekend'].index.hour, df['weekend'].index.minute]).mean()
    df['weekday'].set_index(['time'], inplace=True)
    df['weekend'].set_index(['time'], inplace=True)

    # Plot data frames
    colours = ['r', 'b', 'g', 'y', 'm', 'c'][0:len(df['weekday'].columns)]
    # NB: This uses pd.plot, not mpl.plot.
    # Note technique to plot 2 dfs on same axes
    ax = df['weekday'].plot(kind='line', linestyle='-', color=colours)
    df['weekend'].plot(kind='line', linestyle='--', color=colours, ax=ax)
    ax.xaxis.xmin = 0
    ax.xaxis.xmax = 24
    ax.set_xlabel("Hour", fontsize=20)
    ax.set_ylabel("tariff c/kWh", fontsize=20)
    ax.legend(df['weekday'].columns, fontsize=12, loc='best')
    ax.grid(True)

    plot_file = os.path.join(plot_path, ('-'.join(tariff_list) + '.png'))

    # fig = ax[0].get_figure()
    plt.savefig(plot_file, dpi=1000)
    plt.close()


def plot_battery(
        project,
        study_name,
        base_path='C:\\Users\\z5044992\\Documents\\MainDATA\\DATA_EN_4\\studies',
        start_day=0,
        include_string=''):

    """Plots time series data of pv, load, import, export and SOC."""

    path = os.path.join(base_path, project, 'outputs', study_name, 'timeseries')
    plot_path = os.path.join(path, 'plots')

    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    file_list = [f for f in os.listdir(path) if '.csv' in f and include_string in f]

    for name in file_list:  # [f for f in file_list if f == 'test_energy3_119_btm_s_c_test_2night.csv']:
        print(name)
        file = os.path.join(path, name)
        plot_file = os.path.join(plot_path, name[0:-4] + '_day' + str(start_day).zfill(3) + '.png')
        df = pd.read_csv(file)
        df = df.set_index('timestamp')

        # Slice for 2 days starting at start_day"
        period = df.index[start_day*48:(start_day+2)*48]
        df = df.loc[period]

        # remove irrelevant / unnecessary columns:
        if 'battery_charge_kWh' in df.columns:
            df = df.drop(['battery_charge_kWh'], axis=1)

        # if '_en_' in name:
        df = df.drop(['sum_of_customer_imports', 'sum_of_customer_exports'], axis=1)
        # if '_btm_' in name:
        #     df = df.drop(['grid_import', 'grid_export'], axis=1)
        max_kwh = df[[c for c in df.columns if 'SOC' not in c and 'SOH' not in c]].max().max()
        fig, ax = plt.subplots()
        df.index = pd.to_datetime(df.index)

        for c in [c for c in df.columns if 'SOC' not in c]:
            ax.plot(df.index, df[c], label=c)

        if 'battery_SOC' in df.columns:
            ax2 = ax.twinx()
            ax2.plot(df.index, df['battery_SOC'], linestyle='--')
            ax2.set_ylabel("Battery SOC %")
            ax2.set_ylim(0, 110)

        if 'ind_battery_SOC' in df.columns:
            ax2 = ax.twinx()
            ax2.plot(df.index, df['ind_battery_SOC'], linestyle='--')
            ax2.set_ylabel("Battery SOC %")
            ax2.set_ylim(0, 110)

        ax.set_xlabel("Time", fontsize=14)
        ax.set_ylabel("kWh", fontsize=14)
        ax.grid(True)
        ax.set_ylim(0, max_kwh)

        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        # set formatter
        h_fmt = mdates.DateFormatter('%H')
        ax.xaxis.set_major_formatter(h_fmt)
        # set font and rotation for date tick labels
        fig.autofmt_xdate(rotation=90)

        # legend
        # -------
        leg = ax.legend(fancybox=True)
        leg.get_frame().set_alpha(0.5)
        ax.set_title(name[:-4], fontsize=14)
        # box = ax.get_position()
        # ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

        # plt.show()
        plt.savefig(plot_file, dpi=1000)
        print(plot_file)
        plt.close('all')


def delete_target(target):
    # delete file or folder that is read only
    if os.path.exists(target):
        subprocess.check_call(('attrib -R ' + target + '\\* /S').split())
        shutil.rmtree(target)
