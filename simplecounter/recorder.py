#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ctypes import *
from numpy import *
from dwfconstants import *
import math
import sys
import matplotlib.pyplot as plt
import pdb
import os 


if __name__=="__main__": 
    total_pulse = 0
    f = open("record.csv", "w")
    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    hdwf = c_int()
    sts = c_byte()
    #declare ctype variables
    
    #print DWF version
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    print ("DWF Version: "+version.value)
    
    #open device
    print ("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
    
    if hdwf.value == hdwfNone.value:
        print ("failed to open device")
        quit()
    
    print ("Configuring Digital Out / In...")
    
    # set number of sample to acquire
    # nSamples = 100000
    nSamples = 50000
    # nSamples = 10000
    # nSamples = 1000
    rgwSamples = (c_uint16*nSamples)()
    cAvailable = c_int()
    cLost = c_int()
    cCorrupted = c_int()
    cSamples = 0
    fLost = 0
    fCorrupted = 0
    
    # in record mode samples after trigger are acquired only
    dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeRecord)
    # dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeScanScreen)
    
    # sample rate = system frequency / divider, 100MHz/1000 = 100kHz
    # dwf.FDwfDigitalInDividerSet(hdwf, c_int(1*1000)) #100kHz drop
    # dwf.FDwfDigitalInDividerSet(hdwf, c_int(1*1000*5)) #20kHz drop
    dwf.FDwfDigitalInDividerSet(hdwf, c_int(1*1000*10)) #10kHz
    # 16bit per sample format
    dwf.FDwfDigitalInSampleFormatSet(hdwf, c_int(16))
    # number of samples after trigger
    dwf.FDwfDigitalInTriggerPositionSet(hdwf, c_int(nSamples))
    # trigger when all digital pins are low
    dwf.FDwfDigitalInTriggerSourceSet(hdwf, trigsrcDetectorDigitalIn)
    # trigger detector mask:                  low &   hight & ( rising | falling )
    # dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0xFFFF), c_int(0), c_int(0), c_int(0))
    # 16個のピン全てでローボルテージトリガをかける
    # dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0xFFFF), c_int(0), c_int(0), c_int(0))
    dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0xFFFF), c_int(0), c_int(0), c_int(0))
    
    # begin acquisition
    dwf.FDwfDigitalInConfigure(hdwf, c_bool(0), c_bool(1))
    
    print ("Starting record")
    
    # axes.set_autoscale_on(True) # enable autoscale
    # axes.autoscale_view(True,True,True)
    
    # total_pulse = 0
    current_range = 0
    # rgwSamples = (c_uint16*nSamples)()
    # cSamples = 0
    while cSamples < nSamples:
        dwf.FDwfDigitalInStatus(hdwf, c_int(1), byref(sts))
        if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
            # acquisition not yet started.
            continue
    
        dwf.FDwfDigitalInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
    
        cSamples += cLost.value
        
        if cLost.value:
            fLost = 1
            print ("Samples were lost! Reduce sample rate")
    
        if cCorrupted.value:
            print ("Samples could be corrupted! Reduce sample rate")
            fCorrupted = 1
    
        if cAvailable.value==0 :
            continue
    
        if cSamples+cAvailable.value > nSamples :
            cAvailable = c_int(nSamples-cSamples)
        
        dwf.FDwfDigitalInStatusData(hdwf, byref(rgwSamples, 2*cSamples), c_int(2*cAvailable.value))
        # print cAvailable.value
        cSamples += cAvailable.value
        total_pulse += len((nonzero(rgwSamples))[0])
        print(cSamples)

    for v in rgwSamples:
        f.write("%s\n" % v)
    print("total_pulse: "+str(total_pulse))
    dwf.FDwfDeviceClose(hdwf)
    f.close()
    os.system("Rscript showSum.R")



