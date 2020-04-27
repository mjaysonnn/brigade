#%%
#!/bin/env python3

import argparse
import ast
import csv
import glob
import io
import itertools
import math
import os
import pprint
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties
import humanize
from PyPDF2 import PdfFileMerger, PdfFileReader
import datetime as dt
import pytz

#%%
def viz_setup():
    sns.despine(offset=10, trim=True)
    custom_rc={
        "lines.linewidth" : 0.8
    }
    sns.set(
        context='notebook',
        style='darkgrid',
        palette='deep',
        font='sans-serif',
        font_scale=0.8,
        color_codes=True,
        rc=custom_rc
    )

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_colwidth', 27)
    pd.set_option('display.width', 400)

def close_fig(mypdf):
    buf=io.BytesIO()
    plt.savefig(buf, format='pdf', dpi=400)
    buf.seek(0)
    mypdf.append(PdfFileReader(buf))
    plt.cla()
    plt.clf()
    plt.close('all')

def write_pdf(mypdf):
    mypdf.write("/home/cc/go_projects/src/github.com/brigadecore/brigade/brigade-worker/output.pdf")

""" 
def parse_arguments():
    args_parser = argparse.ArgumentParser(description="Analyze output logs")
    args_parser.add_argument('-i', "--input_csv", default='', help="Path of input CSV file with all container's information in CSV format")
    args = args_parser.parse_args()
    return args
 """
total_read_rows = 0
total_complete_rows = 0
total_relevant_rows=0

def run_reader(csv_file=sys.argv[1]):
    global total_read_rows
    print ("Opening file: {}".format(csv_file))
    column_names = [
            "meta.name",
            "meta.uid",
            "meta.creationTimestamp",
            "c0.type",
            "c1.type",
            "c2.type",  
            "c3.type",
            "c0.lastTransitionTime",
            "c1.lastTransitionTime",
            "c2.lastTransitionTime",
            "c3.lastTransitionTime",
            "c0.status",
            "c1.status",
            "c2.status",
            "c3.status",
            "cs_state.startedAt",
            "cs_state.finishedAt",
            "init_cs_state.finishedAt",
            "init_cs_state.startedAt",
            "startTime"
    ]
    df = pd.read_csv(csv_file, header=None, sep=",", names=column_names, index_col=False)
    print(df,"\n***************************", total_complete_rows) 
    df = df.drop([
        'meta.uid',
        'c0.type',
        'c1.type',
        'c2.type',
        'c3.type'
         ], axis=1).reset_index(drop=True)
    # print(df['c1.status'].unique())
    # print(df['c2.status'].unique())
    for col in [
            "meta.creationTimestamp",
            "c0.lastTransitionTime",
            "c1.lastTransitionTime",
            "c2.lastTransitionTime",
            "c3.lastTransitionTime",
            "cs_state.startedAt",
            "cs_state.finishedAt",
            "init_cs_state.finishedAt",
            "init_cs_state.startedAt",
            "startTime"]:
        df[col] =  pd.to_datetime(df[col], format='%Y-%m-%dT%H:%M:%SZ')
    total_read_rows = df.shape[0]
    return df

def clean_data(df):
    global total_complete_rows
    global total_relevant_rows
    df = df[df['cs_state.startedAt'].notnull()]
    df = df[df['cs_state.finishedAt'].notnull()]
    df = df[df['init_cs_state.startedAt'].notnull()]
    df = df[df['init_cs_state.finishedAt'].notnull()]
    df = df[df['c2.lastTransitionTime'].notnull()]
    df = df[df['c3.lastTransitionTime'].notnull()]
    df = df[df['c1.lastTransitionTime'].notnull()]
    df = df[df['c0.lastTransitionTime'].notnull()]
    df = df[df['startTime'].notnull()]
    df = df[df.notna().any(axis=1)]
    total_complete_rows = df.shape[0]
    print(df['cs_state.finishedAt'],df['cs_state.startedAt'],"\n***************************", total_complete_rows) 
    df = df[df['meta.name'].str.match('asr|nlp|qa')]
    total_relevant_rows = df.shape[0]
    df = df.reset_index(drop=True)

    ## Applying checks to see if some columns are stricly greater than another column
    # print ("startTime > c1.lastTransitionTime : {}", format(df[df['startTime'] > df['c1.lastTransitionTime']]))
    # print ("c1.lastTransitionTime > init_cs_state.startedAt : {}", format(df[df['c1.lastTransitionTime'] > df['init_cs_state.startedAt']]))

    return df

def process_data(df):
    # We are assuming c1.lastTransitionTime == c2.lastTransitionTime always. If this is not the case, we need to modify code and check if our assumptions fail anywhere.
    assert (df['c1.lastTransitionTime'].equals(df['c2.lastTransitionTime']))
    
    df['cs_state_diff'] = (df['cs_state.finishedAt'] - df['cs_state.startedAt']).dt.total_seconds()
    df['start_to_c3lasttransition'] = (df['c3.lastTransitionTime'] - df['startTime']).dt.total_seconds()
    df['c3lasttransition_to_cs_finished'] = (df['cs_state.finishedAt'] - df['c3.lastTransitionTime']).dt.total_seconds()
    
    df['Minimum'] = df.loc[:, ['startTime', 'c3.lastTransitionTime', 'c0.lastTransitionTime', 'c1.lastTransitionTime', 'c2.lastTransitionTime', 'cs_state.startedAt', 'cs_state.finishedAt']].min(axis=1)
    df['Maximum'] = df.loc[:, ['startTime', 'c3.lastTransitionTime', 'c0.lastTransitionTime', 'c1.lastTransitionTime', 'c2.lastTransitionTime', 'cs_state.startedAt', 'cs_state.finishedAt']].max(axis=1)
    df['total_turnaround_lat'] = (df['Maximum'] - df['Minimum']).dt.total_seconds()

    """     print (df[["meta.name",
                    "startTime", 
                    # "c1.lastTransitionTime",
                    # "init_cs_state.startedAt", 
                    # "init_cs_state.finishedAt", 
                    # "c0.lastTransitionTime",
                    # "c3.lastTransitionTime",
                    # "cs_state.startedAt",
                    # "cs_state.finishedAt",
                    # 'cs_state_diff',
                    'start_to_c3lasttransition',
                    'c3lasttransition_to_cs_finished',
                    'total_turnaround_lat'
                    ]]) """

    df = df[["meta.name",
                        "startTime", 
                        # "c1.lastTransitionTime",
                        # "init_cs_state.startedAt", 
                        # "init_cs_state.finishedAt", 
                        # "c0.lastTransitionTime",
                        # "c3.lastTransitionTime",
                        # "cs_state.startedAt",
                        # "cs_state.finishedAt",
                        # 'cs_state_diff',
                        # 'start_to_c3lasttransition',
                        # 'c3lasttransition_to_cs_finished',
                        'Minimum',
                        'Maximum',
                        'total_turnaround_lat'
                        ]]

    # print (df)
    
    df["JobHash"] = df['meta.name'].str[-26:]
    df["AppID"] = df['meta.name'].str[:-27]
    df["Baseline_bool"] = df['AppID'].str.contains(pat = "-b$")
    booleanDictionary = {True: 'Baseline', False: 'SlackPrediction'}
    df["Expt"] = df["Baseline_bool"]
    df["Expt"] = df["Expt"].replace(booleanDictionary)
    df["AppName"] = df['AppID'].map(lambda x: x.rstrip('-b'))
    total_relevant_rows = df.shape[0]
    print (df)
    
    job_df = df.groupby(['JobHash', 'Expt']).agg({'total_turnaround_lat': ['sum'], 'Minimum':['min'], 'Maximum':['max'], 'AppID': ['sum']})
    job_df = job_df.reset_index()
    job_df.columns = job_df.columns.droplevel(1)
    print (job_df)

    return job_df

def plot_data(df):
    merged_pdf = PdfFileMerger()
<<<<<<< HEAD
    for appname in df.AppName.unique():
        fig = plt.figure(figsize=(10,6))
        appdf = df[df['AppName'] == appname]
        baseline_df = appdf.loc[appdf['Expt'] == "Baseline"]
        Slackpred_df = appdf.loc[appdf['Expt'] == "SlackPrediction"]
        sns.distplot(baseline_df['total_turnaround_lat'], label = "Baseline", hist=True, kde=False, rug=False)
        sns.distplot(slackpred_df['total_turnaround_lat'], label = "SlackPrediction", hist=True, kde=False, rug=False)
        plt.title(appname)
        plt.legend()
        close_fig(merged_pdf)
=======
    # for appname in df.AppName.unique():
    #     fig = plt.figure(figsize=(10,6))
    #     appdf = df[df['AppName'] == appname]
    #     baseline_df = appdf.loc[appdf['Expt'] == "Baseline"]
    #     slackpred_df = appdf.loc[appdf['Expt'] == "SlackPrediction"]
    #     sns.distplot(baseline_df['total_turnaround_lat'], label = "Baseline", hist=True, kde=False, rug=False)
    #     sns.distplot(slackpred_df['total_turnaround_lat'], label = "SlackPrediction", hist=True, kde=False, rug=False)
    #     plt.title(appname)
    #     plt.legend()
    #     close_fig(merged_pdf)
>>>>>>> 1eb37a69d3080be66a2e63a4cd7848e7365cf826
    
    fig = plt.figure(figsize=(10,6))
    baseline_df = df.loc[df['Expt'] == "Baseline"]
    slackpred_df = df.loc[df['Expt'] == "SlackPrediction"]
    sns.distplot(baseline_df['total_turnaround_lat'], label = "Baseline", hist=True, kde=True, rug=False).set(xlim=(0))
    sns.distplot(slackpred_df['total_turnaround_lat'], label = "SlackPrediction", hist=True, kde=True, rug=False).set(xlim=(0))
    plt.title("All Jobs - Baseline vs SlackPrediction")
    plt.legend()
    close_fig(merged_pdf)

    fig, ax = plt.subplots(figsize=(10,6))
    df['start_time_int64'] = df.Minimum.astype(np.int64)
    df.plot(x='start_time_int64', y='total_turnaround_lat', kind='scatter', ax=ax)
    ## Need to fix why we see 00:00:00 after we convert back to time.
    # ax.set_xticklabels([dt.date.fromtimestamp(ts / 1e9).strftime('%H:%M:%S') for ts in ax.get_xticks()])
    # ax.set_yticklabels([dt.date.fromtimestamp(ts / 1e9).strftime('%H:%M:%S') for ts in ax.get_yticks()])
    close_fig(merged_pdf)
    write_pdf(merged_pdf)

    return df

# def main():
# args = parse_arguments()
viz_setup()
df = run_reader()
df = clean_data(df)
df = process_data(df)
#df = plot_data(df)

print ("Percentage of incomplete rows = {:.1f}".format((total_read_rows - total_complete_rows)*100/total_read_rows))
print ("Percentage of irrlevant rows = {:.1f}".format((total_read_rows - total_relevant_rows)*100/total_read_rows))

# %%
