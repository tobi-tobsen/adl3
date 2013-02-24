import os, sys
from optparse import OptionParser
from adl3 import *
import string

class ADLError(Exception):
    pass

class atieyefinity(object):
    """This class captures all relevant eyefintity settings for the adapters of a system"""
    ADLDisplayMap = struct_ADLDisplayMap()

    def __str__(self):
        retval = self.getTypeInfo(self.ADLDisplayMap)
        return retval

    def getTypeInfo(self, type): 
        typeInfo = ""
        for index, slotItem in type._fields_:
            if (hasattr(slotItem, "_fields_")):
                typeInfo += self.getTypeInfo(getattr(type, index))
            else:
                typeInfo += "%s " % index
                typeInfo += str(getattr(type, index))
                typeInfo += "\r\n"
        return typeInfo


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

#def getCurrentDisplayModesForAllDisplays(adapter):
#    iAdapterIndex = c_int(-1)
#	iDisplayIndex = c_int(-1)
#	lpNumModes = LPDisplay
#		ADLMode ** 	lppModes	 
#    if ADL_Display_Modes_Get() != ADL_OK:
#        raise ADLError("Unable to get current display modes.")

def getDisplayMapConfigs(adapter):
    lpNumDisplayMap = c_int(-1)
    lpDisplayMap = LPADLDisplayMap()
    lpNumDisplayTarget = c_int(-1)
    lppDisplayTarget = LPADLDisplayTarget()
    retval =  ADL_Display_DisplayMapConfig_Get(adapter, byref(lpNumDisplayMap), 
                                            byref(lpDisplayMap), byref(lpNumDisplayTarget), 
                                            byref(lppDisplayTarget), ADL_DISPLAY_DISPLAYMAP_OPTION_GPUINFO)
    if retval == ADL_OK:
        print "Got %d items in display map"  % lpNumDisplayMap.value
        print "Got %d display targets"  % lpNumDisplayTarget.value
        eyefinityconfigs = []
        for num in range(0, lpNumDisplayMap.value):
            config = atieyefinity()
            config.ADLDisplayMap = lpDisplayMap[num]
            eyefinityconfigs.append(config)
        return eyefinityconfigs
    else:
        raise ADLError("Unable to retrieve the display map config.")

def printConfig():
    primaryAdapter = c_int(-1)
    if ADL_Adapter_Primary_Get(byref(primaryAdapter)) != ADL_OK:
        raise ADLError("Unable to retrieve the primary eyefinity adapter.")
    else:
        print "Primary adapter number %d" % primaryAdapter.value
        configs = getDisplayMapConfigs(primaryAdapter)
        for config in configs:
            print "%s" % config
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