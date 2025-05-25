#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:09:01 2025

@author: Hassan
"""


# Packages for App
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import wfdb
import tempfile
import os

# Packages for Processing
#import physiomarkerNoDependency as ph
import time
import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt

    
uploaded_file = st.file_uploader("Upload a .csv file", type='csv', key="file_uploader")

if uploaded_file is not None:
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(uploaded_file)
        st.info("***Data successfully loaded!***")
        st.dataframe(df)  # Show a preview of the data
        st.markdown("---")
        tab2_fs = st.number_input("**Enter Sampling Frequency**", placeholder="Type a int number...",min_value=125 )

# --- Signal Info ---                
        st.subheader("**Signal Info**")
        
        fileName = os.path.splitext(uploaded_file.name)[0]
        st.write(f"- File Name: {fileName}")
        st.write(f"- Sampling Frequency: {tab2_fs}")
        
        colomnList = df.columns.tolist()[1:]
        st.write(f"- Signal Names: {colomnList}")
        
        totalSamples = len(df)
        st.write(f"- Number of Samples: {totalSamples}")
        
        totalDuration = int(np.round(len(df)/tab2_fs))
        st.write(f"- Total Duration: {totalDuration} Seconds")
        
        st.markdown("---")

# --- Signal Channel Selection ---
        st.info("**Select Signal Index**")
        
        # Single-selection dropdown using st.selectbox
        
        columnName = df.columns.tolist()
        
        #Select ECG
        options_t2 = np.array((columnName))
        options_t2 = np.append(options_t2, "Not Exist")
        #st.write(columnName)
        
        ecgIdx_t2 = st.selectbox("**Select ECG Index**", options_t2, index=(len(options_t2)-1), key="tab2_1se")
        st.write(f"You selected: '{ecgIdx_t2}' for ECG signal")
        
        #Select PPG
        ppgIdx_t2 = st.selectbox("**Select PPG Index**", options_t2, index=(len(options_t2)-1), key="tab2_2se")
        st.write(f"You selected: '{ppgIdx_t2}' for PPG signal")
        
        #Select RESP
        respIdx_t2 = st.selectbox("**Select RESP Index**", options_t2, index=(len(options_t2)-1), key="tab2_3se")
        st.write(f"You selected: '{respIdx_t2}' for RESP signal")
        
        #Select ABP
        abpIdx_t2 = st.selectbox("**Select ABP Index**", options_t2, index=(len(options_t2)-1), key="tab2_4se")
        st.write(f"You selected: '{abpIdx_t2}' for ABP signal")

# --- Getting Signals                             
        
        existing_channels_t2 =[]
        channelIndex_t2 = []   
        
        existSignalsTab2 = []
        
        st.subheader("Available Signals")
        # Extract Signals
        try:
            ecgIdx2 = columnName.index(ecgIdx_t2)
            ecg = df.iloc[:, ecgIdx2].to_numpy()
            st.write('- ECG is present!')
            existing_channels_t2.append("ECG")
            channelIndex_t2.append(ecgIdx_t2)
            existSignalsTab2.append(1)
        except ValueError:
            ecg = []
            existSignalsTab2.append(0)
            st.write('- ECG is unavailable!')
    
        try:
            ppgIdx2 = columnName.index(ppgIdx_t2)
            ppg = df.iloc[:, ppgIdx2].to_numpy()
            st.write('- PPG is present!')
            existing_channels_t2.append("PPG")
            channelIndex_t2.append(ppgIdx_t2)
            existSignalsTab2.append(1)
        except ValueError:
            ppg = []
            existSignalsTab2.append(0)
            st.write('- PPG is unavailable!')
    
        try:
            respIdx2 = columnName.index(respIdx_t2)
            resp = df.iloc[:, respIdx2].to_numpy()
            st.write('- RESP is present!')
            existing_channels_t2.append("RESP")
            channelIndex_t2.append(respIdx_t2)
            existSignalsTab2.append(1)
        except ValueError:
            resp = []
            existSignalsTab2.append(0)
            st.write('- RESP is unavailable!')
    
        try:
            abpIdx2 = columnName.index(abpIdx_t2)
            abp = df.iloc[:, abpIdx2].to_numpy()
            st.write('- ABP is present!')
            existing_channels_t2.append("ABP")
            channelIndex_t2.append(abpIdx_t2)
            existSignalsTab2.append(1)
        except ValueError:
            abp = []
            existSignalsTab2.append(0)
            st.write('- ABP is unavailable!')
            
        st.markdown("---")
        
#--- Plot the available signals ---
        tabPlotT2,tabLabelT2 = st.tabs(["**Plot Signals**","**Label Signals**"])
        with tabPlotT2:
            st.info("***Plot Signals***", icon="ℹ️")
        with tabLabelT2:
    #--- Segment Information ---
            st.info("***Label Signals***", icon="ℹ️")

    except Exception as e:
        st.error(f"Error loading file: {e}")
