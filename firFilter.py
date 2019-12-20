#!/usr/bin/env python
# coding: utf-8

# In[6]:


from scipy import signal
from scipy.signal import lfilter,firwin
# import numpy as np

# In[7]:



#####################################################################
# function firFilter

# Usage: 
# filtered_audio = firFilter(sample_data,fs)

# Input arguments:
# audio_data = sampled audio data of 10 seconds (can be more)
# fs = sampling frequency
# cutoff_frequency = frequency above which filter cutoff noise
#filter_order = no. of iteration filter makes, higher the order, more precise filter is

# Return:
# returns filtered audio data

####################################################################
def firFilter(audio_data,fs,cutoff_frequency = 4000,filter_order = 50):
    
    #Min-Max Normalization
    audio_data = audio_data/max(audio_data)
    min_data = min(audio_data)
    max_data = max(audio_data)
    audio_data = (audio_data - min_data)/(max_data - min_data)
    #Normalization complete
    
    nyquist_rate = fs/2.0
    normalized_cutoff_frequency = cutoff_frequency/nyquist_rate
    
    filter_coefficent = firwin(filter_order,cutoff=normalized_cutoff_frequency,window = "hamming")
    filtered_signal = lfilter(filter_coefficent,1.0,audio_data)
    return filtered_signal

