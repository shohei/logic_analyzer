#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ctypes import *
from numpy import *
from dwfconstants import *
import math
import sys
import matplotlib.pyplot as plt
import pdb


class SimpleCounter:
    def __init__(self):
        self.total_pulse = 0
        self.f = open("record.csv", "w")
        if sys.platform.startswith("win"):
            dwf = cdll.dwf
        elif sys.platform.startswith("darwin"):
            dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            dwf = cdll.LoadLibrary("libdwf.so")
        self.dwf = dwf
        self.hdwf = c_int()
        self.sts = c_byte()

    def main(self):
        dwf = self.dwf 
        hdwf = self.hdwf
        sts = self.sts

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
        nSamples = 10000
        # nSamples = 1000
        rgwSamples = (c_uint16*nSamples)()
        cAvailable = c_int()
        cLost = c_int()
        cCorrupted = c_int()
        cSamples = 0
        fLost = 0
        fCorrupted = 0
        
        # in record mode samples after trigger are acquired only
        # dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeRecord)
        dwf.FDwfDigitalInAcquisitionModeSet(hdwf, acqmodeScanScreen)
        
        # sample rate = system frequency / divider, 100MHz/1000 = 100kHz
        dwf.FDwfDigitalInDividerSet(hdwf, c_int(1*1000*10)) #10kHz
        # 16bit per sample format
        dwf.FDwfDigitalInSampleFormatSet(hdwf, c_int(16))
        # number of samples after trigger
        # dwf.FDwfDigitalInTriggerPositionSet(hdwf, c_int(nSamples))
        # trigger when all digital pins are low
        # dwf.FDwfDigitalInTriggerSourceSet(hdwf, trigsrcDetectorDigitalIn)
        # trigger detector mask:                  low &   hight & ( rising | falling )
        # dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0xFFFF), c_int(0), c_int(0), c_int(0))
        # 16個のピン全てでローボルテージトリガをかける
        # dwf.FDwfDigitalInTriggerSet(hdwf, c_int(0xFFFF), c_int(0), c_int(0), c_int(0))
        
        # begin acquisition
        dwf.FDwfDigitalInConfigure(hdwf, c_bool(0), c_bool(1))
        
        print ("Starting record")
        plt.ion()
        fig = plt.figure()  # Create figure
        axes = fig.add_subplot(111) # Add subplot (dont worry only one plot appears)
        
        # axes.set_autoscale_on(True) # enable autoscale
        # axes.autoscale_view(True,True,True)
        
        hl, = plt.plot([], [])
        hl.set_xdata(range(0,len(rgwSamples)))
        
        # total_pulse = 0
        current_range = 0
        while True:
            if(cSamples == nSamples):
                current_range += len(rgwSamples)
                hl.set_xdata(range(current_range,current_range+nSamples))
                axes.relim()        # Recalculate limits
                axes.autoscale_view(True,True,True) #Autoscale
                plt.draw()
                plt.pause(0.01)
                rgwSamples = (c_uint16*nSamples)()
                cSamples = 0
        
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
            self.total_pulse += len((nonzero(rgwSamples))[0])
        
            hl.set_ydata(rgwSamples)
            axes.relim()        # Recalculate limits
            axes.autoscale_view(True,True,True) #Autoscale
            plt.draw()
            plt.pause(0.01)
    
if __name__=="__main__":
    s = SimpleCounter()
    try:
        s.main()
    except KeyboardInterrupt:
        print("total_pulse: "+str(s.total_pulse))
        s.dwf.FDwfDeviceClose(s.hdwf)
        s.f.close()



