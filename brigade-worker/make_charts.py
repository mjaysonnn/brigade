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
    mypdf.write("output.pdf")

def parse_arguments():
    args_parser = argparse.ArgumentParser(description="Analyze output logs")
    args_parser.add_argument('-i', "--input_csv", default='', action='store', dest='filename',help="Path of input CSV file with all container's information in CSV format")
    args = args_parser.parse_args()
    return args

total_read_rows = 0
total_complete_rows = 0
total_relevant_rows=0

def run_reader(csv_file):
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
    
    df['delta_c1.lastTransitionTime'] = (df['c1.lastTransitionTime'] - df['Minimum']).dt.total_seconds()
    df['delta_init_cs_state.startedAt'] = (df['init_cs_state.startedAt'] - df['Minimum']).dt.total_seconds()
    df['delta_init_cs_state.finishedAt'] = (df['init_cs_state.finishedAt'] - df['Minimum']).dt.total_seconds()
    df['delta_c0.lastTransitionTime'] = (df['c0.lastTransitionTime'] - df['Minimum']).dt.total_seconds()
    df['delta_c3.lastTransitionTime'] = (df['c3.lastTransitionTime'] - df['Minimum']).dt.total_seconds()
    df['delta_lastTransitionTime'] = (df['c3.lastTransitionTime'] - df['c0.lastTransitionTime']).dt.total_seconds()
    df['delta_cs_state.startedAt'] = (df['cs_state.startedAt'] - df['Minimum']).dt.total_seconds()
    df['delta_cs_state.finishedAt'] = (df['cs_state.finishedAt'] - df['Minimum']).dt.total_seconds()

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
                        'total_turnaround_lat',
                        'delta_c1.lastTransitionTime',
                        'delta_init_cs_state.startedAt',
                        'delta_init_cs_state.finishedAt',
                        'delta_c0.lastTransitionTime',
                        'delta_c3.lastTransitionTime',
                        'delta_cs_state.startedAt',
                        'delta_cs_state.finishedAt',
                        'delta_lastTransitionTime'
                        ]]

    # print (df)
    
    df["JobHash"] = df['meta.name'].str[-26:]
    df["AppID"] = df['meta.name'].str[:-27]
    df["Baseline_bool"] = df['AppID'].str.contains(pat = "-baseline$")
    booleanDictionary = {True: 'Baseline', False: 'SlackPrediction'}
    df["Expt"] = df["Baseline_bool"]
    df["Expt"] = df["Expt"].replace(booleanDictionary)
    df["AppName"] = df['AppID'].map(lambda x: x.rstrip('-b'))
    total_relevant_rows = df.shape[0]
    print (df)
    
    job_df = df.groupby(['JobHash', 'Expt']).agg(
        {'total_turnaround_lat': ['sum'], 
         'Minimum':['min'], 
         'Maximum':['max'], 
         'AppID': ['sum'],
         'delta_lastTransitionTime':['min']})
    job_df = job_df.reset_index()
    job_df.columns = job_df.columns.droplevel(1)
    print (job_df['delta_lastTransitionTime'])

    return df, job_df

def plot_data(func_df, job_df):
    merged_pdf = PdfFileMerger()
    for appname in func_df.AppName.unique():
        fig = plt.figure(figsize=(10,6))
        appdf = func_df[func_df['AppName'] == appname]
        baseline_df = appdf.loc[appdf['Expt'] == "Baseline"]
        slackpred_df = appdf.loc[appdf['Expt'] == "SlackPrediction"]
        sns.distplot(baseline_df['total_turnaround_lat'], label = "Baseline", norm_hist=False, kde=False, rug=False)
        sns.distplot(slackpred_df['total_turnaround_lat'], label = "SlackPrediction", hist=True, kde=False, rug=False)
        plt.title(appname)
        plt.legend()
        close_fig(merged_pdf)
    
    fig = plt.figure(figsize=(10,6))
    baseline_df = job_df.loc[job_df['Expt'] == "Baseline"]
    slackpred_df = job_df.loc[job_df['Expt'] == "SlackPrediction"]
    sns.distplot(baseline_df['total_turnaround_lat'], label = "Baseline", norm_hist=False, kde=True, rug=False).set(xlim=(0))
    sns.distplot(slackpred_df['total_turnaround_lat'], label = "SlackPrediction", norm_hist=False, kde=True, rug=False).set(xlim=(0))
    plt.title("All Jobs - Baseline vs SlackPrediction")
    plt.legend()
    close_fig(merged_pdf)

    fig, ax = plt.subplots(figsize=(10,6))
    job_df['start_time_int64'] = job_df.Minimum.astype(np.int64)
    job_df.plot(x='start_time_int64', y='total_turnaround_lat', kind='scatter', ax=ax)
    ## Need to fix why we see 00:00:00 after we convert back to time.
    # ax.set_xticklabels([dt.date.fromtimestamp(ts / 1e9).strftime('%H:%M:%S') for ts in ax.get_xticks()])
    # ax.set_yticklabels([dt.date.fromtimestamp(ts / 1e9).strftime('%H:%M:%S') for ts in ax.get_yticks()])
    close_fig(merged_pdf)
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(y=job_df['delta_lastTransitionTime'], x=job_df['Expt'],data=job_df)
    ax.set_ylim([0,50])
    close_fig(merged_pdf)
    baseline_df = func_df.loc[func_df['Expt'] == "Baseline"]
    baseline_df = baseline_df.reset_index()
    slackpred_df = func_df.loc[func_df['Expt'] == "SlackPrediction"]
    slackpred_df = slackpred_df.reset_index()

    for delta_plots_var in ['delta_c1.lastTransitionTime',
                        #'delta_init_cs_state.startedAt',
                        #'delta_init_cs_state.finishedAt',
                        #'delta_lastTransitionTime',
                        #'delta_c0.lastTransitionTime',
                        'delta_c3.lastTransitionTime',
                        #'delta_cs_state.startedAt',
                        'delta_cs_state.finishedAt'] :
        fig, ax = plt.subplots(figsize=(10,6))
        print ("Charts for .. ", delta_plots_var)
        #ax = sns.lineplot(x=baseline_df.index, y=delta_plots_var, label="Baseline", data=baseline_df)
        #ax = sns.lineplot(x=slackpred_df.index, y=delta_plots_var, label="SlackPredictions", data=slackpred_df)
        #ax = sns.scatterplot(x=baseline_df.index, y=delta_plots_var, label="Baseline", data=baseline_df)
        # ax = sns.scatterplot(x=slackpred_df.index, y=delta_plots_var, label="SlackPredictions", data=slackpred_df)
        # ax = sns.violinplot(x=func_df.index, y=delta_plots_var, hue='Expt', split=True, inner="quart", data=func_df)
        # sns.despine(left=True)
        sns.distplot(baseline_df[delta_plots_var], label = "Baseline", norm_hist=False, kde=False, rug=False)
        sns.distplot(slackpred_df[delta_plots_var], label = "SlackPrediction", norm_hist=False, kde=False, rug=False)
        #sns.boxplot(y=baseline_df[delta_plots_var], x=baseline_df.index,data=baseline_df,palette="Set3")
        plt.legend()
        close_fig(merged_pdf)
        print ("Done", delta_plots_var)
    
    #fig, ax = plt.subplots(figsize=(10,6))
    #ax = sns.lineplot(x=baseline_df.index, y='delta_init_cs_state.startedAt', data=baseline_df)
    #ax = sns.lineplot(x=slackpred_df.index, y='delta_init_cs_state.startedAt', data=slackpred_df)
    #close_fig(merged_pdf)
    
    print (slackpred_df['delta_c3.lastTransitionTime'])
    
    ## Write all charts to PDF here
    write_pdf(merged_pdf)

    return func_df, job_df

# def main():
args = parse_arguments()
viz_setup()
df = run_reader(args.filename)
df = clean_data(df)
func_df, job_df = process_data(df)
df = plot_data(func_df, job_df)

print ("Percentage of incomplete rows = {:.1f}".format((total_read_rows - total_complete_rows)*100/total_read_rows))
print ("Percentage of irrlevant rows = {:.1f}".format((total_read_rows - total_relevant_rows)*100/total_read_rows))

# %%
