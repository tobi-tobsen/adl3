import os, sys
from optparse import OptionParser
from adl3 import *

class ADLError(Exception):
    pass

class atieyefinity(object):
    """description of class"""


def initialize():
    # check for unset DISPLAY, assume :0
    if "DISPLAY" not in os.environ:
        os.environ["DISPLAY"] = ":0"
    
    # the '1' means only retrieve info for active adapters
    if ADL_Main_Control_Create(ADL_Main_Memory_Alloc, 1) != ADL_OK:
        raise ADLError("Couldn't initialize ADL interface.")

def shutdown():
    if ADL_Main_Control_Destroy() != ADL_OK:
        raise ADLError("Couldn't destroy ADL interface global pointers.")

def getDisplayMapConfig(adapter):
    lpNumDisplayMap = c_int(-1)
    lpDisplayMap = LPADLDisplayMap()
    lpNumDisplayTarget = c_int(-1)
    lppDisplayTarget = LPADLDisplayTarget()
    retval =  ADL_Display_DisplayMapConfig_Get(adapter, byref(lpNumDisplayMap), 
                                            byref(lpDisplayMap), byref(lpNumDisplayTarget), 
                                            byref(lppDisplayTarget), ADL_DISPLAY_DISPLAYMAP_OPTION_GPUINFO)

    if retval == ADL_OK:
        print "Got %d items in display map"  % lpNumDisplayMap.value
        print "Got %d items display targets"  % lpNumDisplayTarget.value
        for num in range(0, lpNumDisplayMap.value):
            print lpDisplayMap[num].iDisplayMapMask
            #print lpDisplayMap[num]
        return 

    raise ADLError("Unable to retrieve the display map config.")

def printConfig():
    primaryAdapter = c_int(-1)
    if ADL_Adapter_Primary_Get(byref(primaryAdapter)) != ADL_OK:
        raise ADLError("Unable to retrieve the primary eyefinity adapter.")
    else:
        print "Primary adapter number %d" % primaryAdapter.value
        getDisplayMapConfig(primaryAdapter)
        
    return

if __name__ == "__main__":
    result = 0
    try:
        initialize()
        printConfig()
    
    except ADLError, err:
        result = 1
        print err
        
    finally:        
        shutdown()
        
    sys.exit(result)