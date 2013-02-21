# Copyright (C) 2011 by Mark Visser <mjmvisser@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# This code is based on the AMD Display Library 3.0 and 5.0 SDK

import platform
from ctypes import *

from .adl_defines import *
from .adl_structures import *

_platform = platform.system()
_os = platform.os.name
_release = platform.release()

if _platform == "Linux" or _os == "posix" or _platform == "Windows" or _os == "nt":
    from ctypes import CDLL, CFUNCTYPE

    if _platform == "Linux" or _os == "posix":
        from ctypes import RTLD_GLOBAL

        # pre-load libXext (required by libatiadlxx.so in 11.12)
        CDLL("libXext.so.6", mode=RTLD_GLOBAL)

        # load the ADL 3.0 dso/dll
        _libadl = CDLL("libatiadlxx.so", mode=RTLD_GLOBAL)
    
        # ADL requires we pass an allocation function and handle freeing it ourselves
        _libc = CDLL("libc.so.6")
    else:
        from ctypes.util import find_msvcrt
        try:
            # first try to load the 64-bit library
            _libadl = CDLL("atiadlxx.dll")
        except OSError:
            # fall back on the 32-bit library
            _libadl = CDLL("atiadlxy.dll")

        _libc = CDLL(find_msvcrt());
    
    
    _malloc = _libc.malloc
    _malloc.argtypes = [c_size_t]
    _malloc.restype = c_void_p
    _free = _libc.free
    _free.argtypes = [c_void_p]

    ADL_MAIN_MALLOC_CALLBACK = CFUNCTYPE(c_void_p, c_int)
    ADL_MAIN_FREE_CALLBACK = CFUNCTYPE(None, POINTER(c_void_p))
    
    @ADL_MAIN_MALLOC_CALLBACK
    def ADL_Main_Memory_Alloc(iSize):
        return _malloc(iSize)

    @ADL_MAIN_FREE_CALLBACK
    def ADL_Main_Memory_Free(lpBuffer):
        if lpBuffer[0] is not None:
            _free(lpBuffer[0])
            lpBuffer[0] = None

else:
    raise RuntimeError("Platform '%s' or OS '%s' is not Supported." % (_platform, _os))

ADL_Main_Control_Create = _libadl.ADL_Main_Control_Create
ADL_Main_Control_Create.restype = c_int
ADL_Main_Control_Create.argtypes = [ADL_MAIN_MALLOC_CALLBACK, c_int]

ADL_Main_Control_Refresh = _libadl.ADL_Main_Control_Refresh
ADL_Main_Control_Refresh.restype = c_int
ADL_Main_Control_Refresh.argtypes = []

ADL_Main_Control_Destroy = _libadl.ADL_Main_Control_Destroy
ADL_Main_Control_Destroy.restype = c_int
ADL_Main_Control_Destroy.argtypes = []

ADL_Graphics_Platform_Get = _libadl.ADL_Graphics_Platform_Get
ADL_Graphics_Platform_Get.restype = c_int
ADL_Graphics_Platform_Get.argtypes = [POINTER(c_int)]

ADL_Adapter_Active_Get = _libadl.ADL_Adapter_Active_Get
ADL_Adapter_Active_Get.restype = c_int
ADL_Adapter_Active_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Adapter_NumberOfAdapters_Get = _libadl.ADL_Adapter_NumberOfAdapters_Get
ADL_Adapter_NumberOfAdapters_Get.restype = c_int
ADL_Adapter_NumberOfAdapters_Get.argtypes = [POINTER(c_int)]

ADL_Adapter_AdapterInfo_Get = _libadl.ADL_Adapter_AdapterInfo_Get
ADL_Adapter_AdapterInfo_Get.restype = c_int
ADL_Adapter_AdapterInfo_Get.argtypes = [LPAdapterInfo, c_int]

ADL_Adapter_AdapterInfoX2_Get = _libadl.ADL_Adapter_AdapterInfoX2_Get
ADL_Adapter_AdapterInfoX2_Get.restype = c_int
ADL_Adapter_AdapterInfoX2_Get.argtypes = [POINTER(POINTER(AdapterInfo))]

#int 	ADL_Adapter_AdapterInfoX2_Get (AdapterInfo **lppAdapterInfo)
# TODO:  Test ADL_Adapter_AdapterInfoX2_Get

ADL_Adapter_ASICFamilyType_Get = _libadl.ADL_Adapter_ASICFamilyType_Get
ADL_Adapter_ASICFamilyType_Get.restype = c_int
ADL_Adapter_ASICFamilyType_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Adapter_Speed_Caps = _libadl.ADL_Adapter_Speed_Caps
ADL_Adapter_Speed_Caps.restype = c_int
ADL_Adapter_Speed_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Adapter_Speed_Get = _libadl.ADL_Adapter_Speed_Get
ADL_Adapter_Speed_Get.restype = c_int
ADL_Adapter_Speed_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Adapter_Speed_Set = _libadl.ADL_Adapter_Speed_Set
ADL_Adapter_Speed_Set.restype = c_int
ADL_Adapter_Speed_Set.argtypes = [c_int, c_int]

ADL_Adapter_Accessibility_Get = _libadl.ADL_Adapter_Accessibility_Get
ADL_Adapter_Accessibility_Get.restype = c_int
ADL_Adapter_Accessibility_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Adapter_VideoBiosInfo_Get = _libadl.ADL_Adapter_VideoBiosInfo_Get
ADL_Adapter_VideoBiosInfo_Get.restype = c_int
ADL_Adapter_VideoBiosInfo_Get.argtypes = [c_int, POINTER(ADLBiosInfo)]

ADL_Adapter_ID_Get = _libadl.ADL_Adapter_ID_Get
ADL_Adapter_ID_Get.restype = c_int
ADL_Adapter_ID_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Adapter_CrossdisplayAdapterRole_Caps = _libadl.ADL_Adapter_CrossdisplayAdapterRole_Caps
ADL_Adapter_CrossdisplayAdapterRole_Caps.restype = c_int
ADL_Adapter_CrossdisplayAdapterRole_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(POINTER(c_int)), POINTER(c_int), POINTER(POINTER(c_int)), POINTER(c_int)]

ADL_Adapter_CrossdisplayInfo_Get = _libadl.ADL_Adapter_CrossdisplayInfo_Get
ADL_Adapter_CrossdisplayInfo_Get.restype = c_int
ADL_Adapter_CrossdisplayInfo_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(POINTER(c_int)), POINTER(c_int), POINTER(POINTER(c_int)), POINTER(c_int)]

ADL_Adapter_CrossdisplayInfo_Set = _libadl.ADL_Adapter_CrossdisplayInfo_Set
ADL_Adapter_CrossdisplayInfo_Set.restype = c_int
ADL_Adapter_CrossdisplayInfo_Set.argtypes = [c_int, c_int, c_int, c_int, POINTER(c_int)]

ADL_Adapter_CrossDisplayPlatformInfo_Get = _libadl.ADL_Adapter_CrossDisplayPlatformInfo_Get
ADL_Adapter_CrossDisplayPlatformInfo_Get.restype = c_int
ADL_Adapter_CrossDisplayPlatformInfo_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]
#TODO: Test ADL_Adapter_CrossDisplayPlatformInfo_Get

ADL_Adapter_CrossdisplayInfoX2_Set = _libadl.ADL_Adapter_CrossdisplayInfoX2_Set
ADL_Adapter_CrossdisplayInfoX2_Set.restype = c_int
ADL_Adapter_CrossdisplayInfoX2_Set.argtypes = [c_int, c_int, c_int, c_int, c_int, POINTER(c_int)]
# Todo: Test ADL_Adapter_CrossdisplayInfoX2_Set

ADL_Adapter_Crossfire_Caps = _libadl.ADL_Adapter_Crossfire_Caps
ADL_Adapter_Crossfire_Caps.restype = c_int
ADL_Adapter_Crossfire_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(POINTER(ADLCrossfireComb))]

ADL_Adapter_Crossfire_Get = _libadl.ADL_Adapter_Crossfire_Get
ADL_Adapter_Crossfire_Get.restype = c_int
ADL_Adapter_Crossfire_Get.argtypes = [c_int, POINTER(ADLCrossfireComb), POINTER(ADLCrossfireInfo)]

ADL_Adapter_Crossfire_Set = _libadl.ADL_Adapter_Crossfire_Set
ADL_Adapter_Crossfire_Set.restype = c_int
ADL_Adapter_Crossfire_Set.argtypes = [c_int, POINTER(ADLCrossfireComb)]

ADL_Display_DisplayInfo_Get = _libadl.ADL_Display_DisplayInfo_Get
ADL_Display_DisplayInfo_Get.restype = c_int
ADL_Display_DisplayInfo_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLDisplayInfo)), c_int]

ADL_Display_DpMstInfo_Get = _libadl.ADL_Display_DisplayInfo_Get
ADL_Display_DpMstInfo_Get.restype = c_int
ADL_Display_DpMstInfo_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLDisplayDPMSTInfo)), c_int]
#TODO: Test ADL_Display_DpMstInfo_Get

ADL_Display_NumberOfDisplays_Get = _libadl.ADL_Display_NumberOfDisplays_Get
ADL_Display_NumberOfDisplays_Get.restype = c_int
ADL_Display_NumberOfDisplays_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Display_PreservedAspectRatio_Get = _libadl.ADL_Display_PreservedAspectRatio_Get
ADL_Display_PreservedAspectRatio_Get.restype = c_int
ADL_Display_PreservedAspectRatio_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_PreservedAspectRatio_Set = _libadl.ADL_Display_PreservedAspectRatio_Set
ADL_Display_PreservedAspectRatio_Set.restype = c_int
ADL_Display_PreservedAspectRatio_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_ImageExpansion_Get = _libadl.ADL_Display_ImageExpansion_Get
ADL_Display_ImageExpansion_Get.restype = c_int
ADL_Display_ImageExpansion_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_ImageExpansion_Set = _libadl.ADL_Display_ImageExpansion_Set
ADL_Display_ImageExpansion_Set.restype = c_int
ADL_Display_ImageExpansion_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_Position_Get = _libadl.ADL_Display_Position_Get
ADL_Display_Position_Get.restype = c_int
ADL_Display_Position_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_Position_Set = _libadl.ADL_Display_Position_Set
ADL_Display_Position_Set.restype = c_int
ADL_Display_Position_Set.argtypes = [c_int, c_int, c_int, c_int]

ADL_Display_Size_Get = _libadl.ADL_Display_Size_Get
ADL_Display_Size_Get.restype = c_int
ADL_Display_Size_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_Size_Set = _libadl.ADL_Display_Size_Set
ADL_Display_Size_Set.restype = c_int
ADL_Display_Size_Set.argtypes = [c_int, c_int, c_int, c_int]

ADL_Display_AdjustCaps_Get = _libadl.ADL_Display_AdjustCaps_Get
ADL_Display_AdjustCaps_Get.restype = c_int
ADL_Display_AdjustCaps_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_Capabilities_Get = _libadl.ADL_Display_Capabilities_Get
ADL_Display_Capabilities_Get.restype = c_int
ADL_Display_Capabilities_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_ConnectedDisplays_Get = _libadl.ADL_Display_ConnectedDisplays_Get
ADL_Display_ConnectedDisplays_Get.restype = c_int
ADL_Display_ConnectedDisplays_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Display_DeviceConfig_Get = _libadl.ADL_Display_DeviceConfig_Get
ADL_Display_DeviceConfig_Get.restype = c_int
ADL_Display_DeviceConfig_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayConfig)]

ADL_Display_Property_Get = _libadl.ADL_Display_Property_Get
ADL_Display_Property_Get.restype = c_int
ADL_Display_Property_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayProperty)]

ADL_Display_Property_Set = _libadl.ADL_Display_Property_Set
ADL_Display_Property_Set.restype = c_int
ADL_Display_Property_Set.argtypes = [c_int, c_int, POINTER(ADLDisplayProperty)]

ADL_Display_SwitchingCapability_Get = _libadl.ADL_Display_SwitchingCapability_Get
ADL_Display_SwitchingCapability_Get.restype = c_int
ADL_Display_SwitchingCapability_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Display_DitherState_Get = _libadl.ADL_Display_DitherState_Get
ADL_Display_DitherState_Get.restype = c_int
ADL_Display_DitherState_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_DitherState_Set = _libadl.ADL_Display_DitherState_Set
ADL_Display_DitherState_Set.restype = c_int
ADL_Display_DitherState_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_SupportedPixelFormat_Get = _libadl.ADL_Display_SupportedPixelFormat_Get
ADL_Display_SupportedPixelFormat_Get.restype = c_int
ADL_Display_SupportedPixelFormat_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_PixelFormat_Get = _libadl.ADL_Display_PixelFormat_Get
ADL_Display_PixelFormat_Get.restype = c_int
ADL_Display_PixelFormat_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_PixelFormat_Set = _libadl.ADL_Display_PixelFormat_Set
ADL_Display_PixelFormat_Set.restype = c_int
ADL_Display_PixelFormat_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_ODClockInfo_Get = _libadl.ADL_Display_ODClockInfo_Get
ADL_Display_ODClockInfo_Get.restype = c_int
ADL_Display_ODClockInfo_Get.argtypes = [c_int, POINTER(ADLAdapterODClockInfo)]

ADL_Display_ODClockConfig_Set = _libadl.ADL_Display_ODClockConfig_Set
ADL_Display_ODClockConfig_Set.restype = c_int
ADL_Display_ODClockConfig_Set.argtypes = [c_int, POINTER(ADLAdapterODClockConfig)]

ADL_Display_AdjustmentCoherent_Get = _libadl.ADL_Display_AdjustmentCoherent_Get
ADL_Display_AdjustmentCoherent_Get.restype = c_int
ADL_Display_AdjustmentCoherent_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_AdjustmentCoherent_Set = _libadl.ADL_Display_AdjustmentCoherent_Set
ADL_Display_AdjustmentCoherent_Set.restype = c_int
ADL_Display_AdjustmentCoherent_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_ReducedBlanking_Get = _libadl.ADL_Display_ReducedBlanking_Get
ADL_Display_ReducedBlanking_Get.restype = c_int
ADL_Display_ReducedBlanking_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_ReducedBlanking_Set = _libadl.ADL_Display_ReducedBlanking_Set
ADL_Display_ReducedBlanking_Set.restype = c_int
ADL_Display_ReducedBlanking_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_FormatsOverride_Get = _libadl.ADL_Display_FormatsOverride_Get
ADL_Display_FormatsOverride_Get.restype = c_int
ADL_Display_FormatsOverride_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_FormatsOverride_Set = _libadl.ADL_Display_FormatsOverride_Set
ADL_Display_FormatsOverride_Set.restype = c_int
ADL_Display_FormatsOverride_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_MVPUCaps_Get = _libadl.ADL_Display_MVPUCaps_Get
ADL_Display_MVPUCaps_Get.restype = c_int
ADL_Display_MVPUCaps_Get.argtypes = [c_int, POINTER(ADLMVPUCaps)]

ADL_Display_MVPUStatus_Get = _libadl.ADL_Display_MVPUStatus_Get
ADL_Display_MVPUStatus_Get.restype = c_int
ADL_Display_MVPUStatus_Get.argtypes = [c_int, POINTER(ADLMVPUStatus)]

ADL_Adapter_Active_Set = _libadl.ADL_Adapter_Active_Set
ADL_Adapter_Active_Set.restype = c_int
ADL_Adapter_Active_Set.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Adapter_Active_SetPrefer = _libadl.ADL_Adapter_Active_SetPrefer
ADL_Adapter_Active_SetPrefer.restype = c_int
ADL_Adapter_Active_SetPrefer.argtypes = [c_int, c_int, c_int, POINTER(ADLDisplayTarget), POINTER(c_int)]

ADL_Adapter_Primary_Get = _libadl.ADL_Adapter_Primary_Get
ADL_Adapter_Primary_Get.restype = c_int
ADL_Adapter_Primary_Get.argtypes = [POINTER(c_int)]

ADL_Adapter_Primary_Set = _libadl.ADL_Adapter_Primary_Set
ADL_Adapter_Primary_Set.restype = c_int
ADL_Adapter_Primary_Set.argtypes = [c_int]

ADL_Adapter_ModeSwitch = _libadl.ADL_Adapter_ModeSwitch
ADL_Adapter_ModeSwitch.restype = c_int
ADL_Adapter_ModeSwitch.argtypes = [c_int]

ADL_Display_Modes_Get = _libadl.ADL_Display_Modes_Get
ADL_Display_Modes_Get.restype = c_int
ADL_Display_Modes_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(POINTER(ADLMode))]

ADL_Display_Modes_Set = _libadl.ADL_Display_Modes_Set
ADL_Display_Modes_Set.restype = c_int
ADL_Display_Modes_Set.argtypes = [c_int, c_int, c_int, POINTER(ADLMode)]

ADL_Display_PossibleMode_Get = _libadl.ADL_Display_PossibleMode_Get
ADL_Display_PossibleMode_Get.restype = c_int
ADL_Display_PossibleMode_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLMode))]

ADL_Display_ForcibleDisplay_Get = _libadl.ADL_Display_ForcibleDisplay_Get
ADL_Display_ForcibleDisplay_Get.restype = c_int
ADL_Display_ForcibleDisplay_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_ForcibleDisplay_Set = _libadl.ADL_Display_ForcibleDisplay_Set
ADL_Display_ForcibleDisplay_Set.restype = c_int
ADL_Display_ForcibleDisplay_Set.argtypes = [c_int, c_int, c_int]

ADL_Adapter_NumberOfActivatableSources_Get = _libadl.ADL_Adapter_NumberOfActivatableSources_Get
ADL_Adapter_NumberOfActivatableSources_Get.restype = c_int
ADL_Adapter_NumberOfActivatableSources_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLActivatableSource))]

ADL_Adapter_Display_Caps = _libadl.ADL_Adapter_Display_Caps
ADL_Adapter_Display_Caps.restype = c_int
ADL_Adapter_Display_Caps.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLAdapterDisplayCap))]

ADL_Display_DisplayMapConfig_Get = _libadl.ADL_Display_DisplayMapConfig_Get
ADL_Display_DisplayMapConfig_Get.restype = c_int
ADL_Display_DisplayMapConfig_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLDisplayMap)), POINTER(c_int), POINTER(POINTER(ADLDisplayTarget)), c_int]

ADL_Display_DisplayMapConfig_Set = _libadl.ADL_Display_DisplayMapConfig_Set
ADL_Display_DisplayMapConfig_Set.restype = c_int
ADL_Display_DisplayMapConfig_Set.argtypes = [c_int, c_int, POINTER(ADLDisplayMap), c_int, POINTER(ADLDisplayTarget)]

ADL_Display_PossibleMapping_Get = _libadl.ADL_Display_PossibleMapping_Get
ADL_Display_PossibleMapping_Get.restype = c_int
ADL_Display_PossibleMapping_Get.argtypes = [c_int, c_int, POINTER(ADLPossibleMapping), c_int, POINTER(c_int), POINTER(POINTER(ADLPossibleMapping))]

ADL_Display_DisplayMapConfig_Validate = _libadl.ADL_Display_DisplayMapConfig_Validate
ADL_Display_DisplayMapConfig_Validate.restype = c_int
ADL_Display_DisplayMapConfig_Validate.argtypes = [c_int, c_int, POINTER(ADLPossibleMap), POINTER(c_int), POINTER(POINTER(ADLPossibleMapResult))]

ADL_Display_DisplayMapConfig_PossibleAddAndRemove = _libadl.ADL_Display_DisplayMapConfig_PossibleAddAndRemove
ADL_Display_DisplayMapConfig_PossibleAddAndRemove.restype = c_int
ADL_Display_DisplayMapConfig_PossibleAddAndRemove.argtypes = [c_int, c_int, POINTER(ADLDisplayMap), c_int, POINTER(ADLDisplayTarget), POINTER(c_int), POINTER(POINTER(ADLDisplayTarget)), POINTER(c_int), POINTER(POINTER(ADLDisplayTarget))]

ADL_Display_SLSGrid_Caps = _libadl.ADL_Display_SLSGrid_Caps
ADL_Display_SLSGrid_Caps.restype = c_int
ADL_Display_SLSGrid_Caps.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLSLSGrid)), c_int]

ADL_Display_SLSMapIndexList_Get = _libadl.ADL_Display_SLSMapIndexList_Get
ADL_Display_SLSMapIndexList_Get.restype = c_int
ADL_Display_SLSMapIndexList_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(c_int)), c_int]

ADL_Display_SLSMapIndex_Get = _libadl.ADL_Display_SLSMapIndex_Get
ADL_Display_SLSMapIndex_Get.restype = c_int
ADL_Display_SLSMapIndex_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayTarget), POINTER(c_int)]

ADL_Display_SLSMapConfig_Get = _libadl.ADL_Display_SLSMapConfig_Get
ADL_Display_SLSMapConfig_Get.restype = c_int
ADL_Display_SLSMapConfig_Get.argtypes = [c_int, c_int, POINTER(ADLSLSMap), POINTER(c_int), POINTER(POINTER(ADLSLSTarget)), POINTER(c_int), POINTER(POINTER(ADLSLSMode)), POINTER(c_int), POINTER(POINTER(ADLBezelTransientMode)), POINTER(c_int), POINTER(POINTER(ADLBezelTransientMode)), POINTER(c_int), POINTER(POINTER(ADLSLSOffset)), c_int]

#int 	ADL_Display_SLSMapConfigX2_Get (int iAdapterIndex, int iSLSMapIndex, ADLSLSMap *lpSLSMap, int *lpNumSLSTarget, ADLSLSTarget **lppSLSTarget, int *lpNumNativeMode, ADLSLSMode **lppNativeMode, int *lpNumNativeModeOffsets, ADLSLSOffset **lppNativeModeOffsets, int *lpNumBezelMode, ADLBezelTransientMode **lppBezelMode, int *lpNumTransientMode, ADLBezelTransientMode **lppTransientMode, int *lpNumSLSOffset, ADLSLSOffset **lppSLSOffset, int iOption)
# 	Function to retrieve an SLS configuration.
#TODO: implement and test ADL_Display_SLSMapConfigX2_Get

ADL_Display_SLSMapConfig_Create = _libadl.ADL_Display_SLSMapConfig_Create
ADL_Display_SLSMapConfig_Create.restype = c_int
ADL_Display_SLSMapConfig_Create.argtypes = [c_int, ADLSLSMap, c_int, POINTER(ADLSLSTarget), c_int, POINTER(c_int), c_int]

ADL_Display_SLSMapConfig_Delete = _libadl.ADL_Display_SLSMapConfig_Delete
ADL_Display_SLSMapConfig_Delete.restype = c_int
ADL_Display_SLSMapConfig_Delete.argtypes = [c_int, c_int]

ADL_Display_SLSMapConfig_SetState = _libadl.ADL_Display_SLSMapConfig_SetState
ADL_Display_SLSMapConfig_SetState.restype = c_int
ADL_Display_SLSMapConfig_SetState.argtypes = [c_int, c_int, c_int]

ADL_Display_SLSMapConfig_Rearrange = _libadl.ADL_Display_SLSMapConfig_Rearrange
ADL_Display_SLSMapConfig_Rearrange.restype = c_int
ADL_Display_SLSMapConfig_Rearrange.argtypes = [c_int, c_int, c_int, POINTER(ADLSLSTarget), ADLSLSMap, c_int]

if (_platform == "Windows" or _os == "nt") and _release == "XP":
    ADL_Display_PossibleMode_WinXP_Get = _libadl.ADL_Display_PossibleMode_WinXP_Get
    ADL_Display_PossibleMode_WinXP_Get.restype = c_int
    ADL_Display_PossibleMode_WinXP_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayTarget), c_int, c_int, POINTER(c_int), POINTER(POINTER(ADLMode))]

ADL_Display_BezelOffsetSteppingSize_Get = _libadl.ADL_Display_BezelOffsetSteppingSize_Get
ADL_Display_BezelOffsetSteppingSize_Get.restype = c_int
ADL_Display_BezelOffsetSteppingSize_Get.argtypes = [c_int, POINTER(c_int), POINTER(POINTER(ADLBezelOffsetSteppingSize))]

ADL_Display_BezelOffset_Set = _libadl.ADL_Display_BezelOffset_Set
ADL_Display_BezelOffset_Set.restype = c_int
ADL_Display_BezelOffset_Set.argtypes = [c_int, c_int, c_int, LPADLSLSOffset, ADLSLSMap, c_int]

ADL_Display_BezelSupported_Validate = _libadl.ADL_Display_BezelSupported_Validate
ADL_Display_BezelSupported_Validate.restype = c_int
ADL_Display_BezelSupported_Validate.argtypes = [c_int, c_int, LPADLPossibleSLSMap, POINTER(c_int), POINTER(LPADLPossibleMapResult)]

ADL_Workstation_EnableUnsupportedDisplayModes = _libadl.ADL_Workstation_EnableUnsupportedDisplayModes
ADL_Workstation_EnableUnsupportedDisplayModes.restype = c_int
ADL_Workstation_EnableUnsupportedDisplayModes.argtypes = [c_int]
#TODO: Test ADL_Workstation_EnableUnsupportedDisplayModes

ADL_Display_ColorCaps_Get = _libadl.ADL_Display_ColorCaps_Get
ADL_Display_ColorCaps_Get.restype = c_int
ADL_Display_ColorCaps_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_Color_Set = _libadl.ADL_Display_Color_Set
ADL_Display_Color_Set.restype = c_int
ADL_Display_Color_Set.argtypes = [c_int, c_int, c_int, c_int]

ADL_Display_Color_Get = _libadl.ADL_Display_Color_Get
ADL_Display_Color_Get.restype = c_int
ADL_Display_Color_Get.argtypes = [c_int, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_ColorTemperatureSource_Get = _libadl.ADL_Display_ColorTemperatureSource_Get
ADL_Display_ColorTemperatureSource_Get.restype = c_int
ADL_Display_ColorTemperatureSource_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_ColorTemperatureSource_Set = _libadl.ADL_Display_ColorTemperatureSource_Set
ADL_Display_ColorTemperatureSource_Set.restype = c_int
ADL_Display_ColorTemperatureSource_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_ModeTimingOverride_Get = _libadl.ADL_Display_ModeTimingOverride_Get
ADL_Display_ModeTimingOverride_Get.restype = c_int
ADL_Display_ModeTimingOverride_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayMode), POINTER(ADLDisplayModeInfo)]

ADL_Display_ModeTimingOverride_Set = _libadl.ADL_Display_ModeTimingOverride_Set
ADL_Display_ModeTimingOverride_Set.restype = c_int
ADL_Display_ModeTimingOverride_Set.argtypes = [c_int, c_int, POINTER(ADLDisplayModeInfo), c_int]

ADL_Display_ModeTimingOverrideList_Get = _libadl.ADL_Display_ModeTimingOverrideList_Get
ADL_Display_ModeTimingOverrideList_Get.restype = c_int
ADL_Display_ModeTimingOverrideList_Get.argtypes = [c_int, c_int, c_int, POINTER(ADLDisplayModeInfo), POINTER(c_int)]

ADL_Display_CustomizedModeListNum_Get = _libadl.ADL_Display_CustomizedModeListNum_Get
ADL_Display_CustomizedModeListNum_Get.restype = c_int
ADL_Display_CustomizedModeListNum_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_CustomizedModeList_Get = _libadl.ADL_Display_CustomizedModeList_Get
ADL_Display_CustomizedModeList_Get.restype = c_int
ADL_Display_CustomizedModeList_Get.argtypes = [c_int, c_int, POINTER(ADLCustomMode), c_int]

ADL_Display_CustomizedMode_Add = _libadl.ADL_Display_CustomizedMode_Add
ADL_Display_CustomizedMode_Add.restype = c_int
ADL_Display_CustomizedMode_Add.argtypes = [c_int, c_int, ADLCustomMode]

ADL_Display_CustomizedMode_Delete = _libadl.ADL_Display_CustomizedMode_Delete
ADL_Display_CustomizedMode_Delete.restype = c_int
ADL_Display_CustomizedMode_Delete.argtypes = [c_int, c_int, c_int]

ADL_Display_CustomizedMode_Validate = _libadl.ADL_Display_CustomizedMode_Validate
ADL_Display_CustomizedMode_Validate.restype = c_int
ADL_Display_CustomizedMode_Validate.argtypes = [c_int, c_int, ADLCustomMode, POINTER(c_int)]

ADL_Display_Underscan_Set = _libadl.ADL_Display_Underscan_Set
ADL_Display_Underscan_Set.restype = c_int
ADL_Display_Underscan_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_Underscan_Get = _libadl.ADL_Display_Underscan_Get
ADL_Display_Underscan_Get.restype = c_int
ADL_Display_Underscan_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_Overscan_Set = _libadl.ADL_Display_Overscan_Set
ADL_Display_Overscan_Set.restype = c_int
ADL_Display_Overscan_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_Overscan_Get = _libadl.ADL_Display_Overscan_Get
ADL_Display_Overscan_Get.restype = c_int
ADL_Display_Overscan_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Display_ControllerOverlayAdjustmentCaps_Get = _libadl.ADL_Display_ControllerOverlayAdjustmentCaps_Get
ADL_Display_ControllerOverlayAdjustmentCaps_Get.restype = c_int
ADL_Display_ControllerOverlayAdjustmentCaps_Get.argtypes = [c_int, POINTER(ADLControllerOverlayInput), POINTER(ADLControllerOverlayInfo)]

ADL_Display_ControllerOverlayAdjustmentData_Get = _libadl.ADL_Display_ControllerOverlayAdjustmentData_Get
ADL_Display_ControllerOverlayAdjustmentData_Get.restype = c_int
ADL_Display_ControllerOverlayAdjustmentData_Get.argtypes = [c_int, POINTER(ADLControllerOverlayInput)]

ADL_Display_ControllerOverlayAdjustmentData_Set = _libadl.ADL_Display_ControllerOverlayAdjustmentData_Set
ADL_Display_ControllerOverlayAdjustmentData_Set.restype = c_int
ADL_Display_ControllerOverlayAdjustmentData_Set.argtypes = [c_int, POINTER(ADLControllerOverlayInput)]

ADL_Display_PowerXpressVersion_Get = _libadl.ADL_Display_PowerXpressVersion_Get
ADL_Display_PowerXpressVersion_Get.restype = c_int
ADL_Display_PowerXpressVersion_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Display_PowerXpressActiveGPU_Get = _libadl.ADL_Display_PowerXpressActiveGPU_Get
ADL_Display_PowerXpressActiveGPU_Get.restype = c_int
ADL_Display_PowerXpressActiveGPU_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Display_PowerXpressActiveGPU_Set = _libadl.ADL_Display_PowerXpressActiveGPU_Set
ADL_Display_PowerXpressActiveGPU_Set.restype = c_int
ADL_Display_PowerXpressActiveGPU_Set.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Display_PowerXpress_AutoSwitchConfig_Get = _libadl.ADL_Display_PowerXpress_AutoSwitchConfig_Get
ADL_Display_PowerXpress_AutoSwitchConfig_Get.restype = c_int
ADL_Display_PowerXpress_AutoSwitchConfig_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_PowerXpress_AutoSwitchConfig_Set = _libadl.ADL_Display_PowerXpress_AutoSwitchConfig_Set
ADL_Display_PowerXpress_AutoSwitchConfig_Set.restype = c_int
ADL_Display_PowerXpress_AutoSwitchConfig_Set.argtypes = [c_int, c_int, c_int]

# TODO: implement and test these
#int 	ADL_PowerXpress_Config_Caps (int iAdapterIndex, ADLPXConfigCaps *lpPXConfigCaps)
# 	This function gets the PowerXpress configuration Caps. 
#int 	ADL_PowerXpress_Scheme_Get (int iAdapterIndex, ADLPXScheme *lpPXSchemeRange, ADLPXScheme *lpPXSchemeCurrentState, ADLPXScheme *lpPXSchemeDefaultState)
# 	This function gets the PowerXpress scheme. 
#int 	ADL_PowerXpress_Scheme_Set (int iAdapterIndex, ADLPXScheme scheme)
# 	This function sets the PowerXpress scheme. 
#int 	ADL_PowerXpress_AncillaryDevices_Get (int iAdapterIndex, int *lpNumberOfAncillaryDevices, ADLBdf **lppAncillaryDevices)
# 	This function gets ancillary GPUs.

# TODO: implement and test these
#int 	ADL_Display_ViewPort_Set (int iAdapterIndex, int iDisplayIndex, ADLControllerMode *lpControllerMode)
# 	Function to change the view position, view size or view pan lock of a selected display. 
#int 	ADL_Display_ViewPort_Get (int iAdapterIndex, int iDisplayIndex, ADLControllerMode *lpControllerMode)
# 	Function to get the view position, view size or view pan lock of a selected display. 
#int 	ADL_Display_ViewPort_Cap (int iAdapterIndex, int *lpSupported)
# 	Function to check if the selected adapter supports the view port control.

ADL_DFP_BaseAudioSupport_Get = _libadl.ADL_DFP_BaseAudioSupport_Get
ADL_DFP_BaseAudioSupport_Get.restype = c_int
ADL_DFP_BaseAudioSupport_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_DFP_HDMISupport_Get = _libadl.ADL_DFP_HDMISupport_Get
ADL_DFP_HDMISupport_Get.restype = c_int
ADL_DFP_HDMISupport_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_DFP_MVPUAnalogSupport_Get = _libadl.ADL_DFP_MVPUAnalogSupport_Get
ADL_DFP_MVPUAnalogSupport_Get.restype = c_int
ADL_DFP_MVPUAnalogSupport_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_DFP_PixelFormat_Caps = _libadl.ADL_DFP_PixelFormat_Caps
ADL_DFP_PixelFormat_Caps.restype = c_int
ADL_DFP_PixelFormat_Caps.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]

ADL_DFP_PixelFormat_Get = _libadl.ADL_DFP_PixelFormat_Get
ADL_DFP_PixelFormat_Get.restype = c_int
ADL_DFP_PixelFormat_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int)]

ADL_DFP_PixelFormat_Set = _libadl.ADL_DFP_PixelFormat_Set
ADL_DFP_PixelFormat_Set.restype = c_int
ADL_DFP_PixelFormat_Set.argtypes = [c_int, c_int, c_int]

ADL_DFP_GPUScalingEnable_Get = _libadl.ADL_DFP_GPUScalingEnable_Get
ADL_DFP_GPUScalingEnable_Get.restype = c_int
ADL_DFP_GPUScalingEnable_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_DFP_GPUScalingEnable_Set = _libadl.ADL_DFP_GPUScalingEnable_Set
ADL_DFP_GPUScalingEnable_Set.restype = c_int
ADL_DFP_GPUScalingEnable_Set.argtypes = [c_int, c_int, c_int]

ADL_DFP_AllowOnlyCETimings_Get = _libadl.ADL_DFP_AllowOnlyCETimings_Get
ADL_DFP_AllowOnlyCETimings_Get.restype = c_int
ADL_DFP_AllowOnlyCETimings_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_DFP_AllowOnlyCETimings_Set = _libadl.ADL_DFP_AllowOnlyCETimings_Set
ADL_DFP_AllowOnlyCETimings_Set.restype = c_int
ADL_DFP_AllowOnlyCETimings_Set.argtypes = [c_int, c_int, c_int]

ADL_Display_TVCaps_Get = _libadl.ADL_Display_TVCaps_Get
ADL_Display_TVCaps_Get.restype = c_int
ADL_Display_TVCaps_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_TV_Standard_Set = _libadl.ADL_TV_Standard_Set
ADL_TV_Standard_Set.restype = c_int
ADL_TV_Standard_Set.argtypes = [c_int, c_int, c_int]

ADL_TV_Standard_Get = _libadl.ADL_TV_Standard_Get
ADL_TV_Standard_Get.restype = c_int
ADL_TV_Standard_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_CV_DongleSettings_Get = _libadl.ADL_CV_DongleSettings_Get
ADL_CV_DongleSettings_Get.restype = c_int
ADL_CV_DongleSettings_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_CV_DongleSettings_Set = _libadl.ADL_CV_DongleSettings_Set
ADL_CV_DongleSettings_Set.restype = c_int
ADL_CV_DongleSettings_Set.argtypes = [c_int, c_int, c_int]

ADL_CV_DongleSettings_Reset = _libadl.ADL_CV_DongleSettings_Reset
ADL_CV_DongleSettings_Reset.restype = c_int
ADL_CV_DongleSettings_Reset.argtypes = [c_int, c_int]

ADL_Overdrive5_CurrentActivity_Get = _libadl.ADL_Overdrive5_CurrentActivity_Get
ADL_Overdrive5_CurrentActivity_Get.restype = c_int
ADL_Overdrive5_CurrentActivity_Get.argtypes = [c_int, POINTER(ADLPMActivity)]

ADL_Overdrive5_ThermalDevices_Enum = _libadl.ADL_Overdrive5_ThermalDevices_Enum
ADL_Overdrive5_ThermalDevices_Enum.restype = c_int
ADL_Overdrive5_ThermalDevices_Enum.argtypes = [c_int, c_int, POINTER(ADLThermalControllerInfo)]

ADL_Overdrive5_Temperature_Get = _libadl.ADL_Overdrive5_Temperature_Get
ADL_Overdrive5_Temperature_Get.restype = c_int
ADL_Overdrive5_Temperature_Get.argtypes = [c_int, c_int, POINTER(ADLTemperature)]

ADL_Overdrive5_FanSpeedInfo_Get = _libadl.ADL_Overdrive5_FanSpeedInfo_Get
ADL_Overdrive5_FanSpeedInfo_Get.restype = c_int
ADL_Overdrive5_FanSpeedInfo_Get.argtypes = [c_int, c_int, POINTER(ADLFanSpeedInfo)]

ADL_Overdrive5_FanSpeed_Get = _libadl.ADL_Overdrive5_FanSpeed_Get
ADL_Overdrive5_FanSpeed_Get.restype = c_int
ADL_Overdrive5_FanSpeed_Get.argtypes = [c_int, c_int, POINTER(ADLFanSpeedValue)]

ADL_Overdrive5_FanSpeed_Set = _libadl.ADL_Overdrive5_FanSpeed_Set
ADL_Overdrive5_FanSpeed_Set.restype = c_int
ADL_Overdrive5_FanSpeed_Set.argtypes = [c_int, c_int, POINTER(ADLFanSpeedValue)]

ADL_Overdrive5_FanSpeedToDefault_Set = _libadl.ADL_Overdrive5_FanSpeedToDefault_Set
ADL_Overdrive5_FanSpeedToDefault_Set.restype = c_int
ADL_Overdrive5_FanSpeedToDefault_Set.argtypes = [c_int, c_int]

ADL_Overdrive5_ODParameters_Get = _libadl.ADL_Overdrive5_ODParameters_Get
ADL_Overdrive5_ODParameters_Get.restype = c_int
ADL_Overdrive5_ODParameters_Get.argtypes = [c_int, POINTER(ADLODParameters)]

ADL_Overdrive5_ODPerformanceLevels_Get = _libadl.ADL_Overdrive5_ODPerformanceLevels_Get
ADL_Overdrive5_ODPerformanceLevels_Get.restype = c_int
ADL_Overdrive5_ODPerformanceLevels_Get.argtypes = [c_int, c_int, POINTER(ADLODPerformanceLevels)]

ADL_Overdrive5_ODPerformanceLevels_Set = _libadl.ADL_Overdrive5_ODPerformanceLevels_Set
ADL_Overdrive5_ODPerformanceLevels_Set.restype = c_int
ADL_Overdrive5_ODPerformanceLevels_Set.argtypes = [c_int, POINTER(ADLODPerformanceLevels)]

# PowerControl APIs were undocumented in ADL3, but discovered via the AMDOverdriveCtrl project
# http://phoronix.com/forums/showthread.php?55589-undocumented-feature-powertune
# These are now documented in ADL5

ADL_Overdrive5_PowerControl_Caps = _libadl.ADL_Overdrive5_PowerControl_Caps
ADL_Overdrive5_PowerControl_Caps.restype = c_int
ADL_Overdrive5_PowerControl_Caps.argtypes = [c_int, POINTER(c_int)]

ADL_Overdrive5_PowerControlInfo_Get = _libadl.ADL_Overdrive5_PowerControlInfo_Get
ADL_Overdrive5_PowerControlInfo_Get.restype = c_int
ADL_Overdrive5_PowerControlInfo_Get.argtypes = [c_int, POINTER(ADLPowerControlInfo)]

ADL_Overdrive5_PowerControl_Get = _libadl.ADL_Overdrive5_PowerControl_Get
ADL_Overdrive5_PowerControl_Get.restype = c_int
ADL_Overdrive5_PowerControl_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Overdrive5_PowerControl_Set = _libadl.ADL_Overdrive5_PowerControl_Set
ADL_Overdrive5_PowerControl_Set.restype = c_int
ADL_Overdrive5_PowerControl_Set.argtypes = [c_int, c_int]

ADL_Overdrive_Caps = _libadl.ADL_Overdrive_Caps
ADL_Overdrive_Caps.restype = c_int
ADL_Overdrive_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
#TODO: test the ADL_Overdrive5 PowerControl methods
#TODO: test the ADL_Overdrive_Caps

#TODO implement and test Overdrive6 APIS:
#Overdrive6 APIs

#Functions
#int 	ADL_Overdrive6_Capabilities_Get (int iAdapterIndex, ADLOD6Capabilities *lpODCapabilities)
# 	Function to retrieve the current Overdrive capabilities. 
#int 	ADL_Overdrive6_StateInfo_Get (int iAdapterIndex, int iStateType, ADLOD6StateInfo *lpStateInfo)
# 	Function to retrieve the current or default Overdrive clock ranges. 
#int 	ADL_Overdrive6_State_Set (int iAdapterIndex, int iStateType, ADLOD6StateInfo *lpStateInfo)
# 	Function to set the current Overdrive clock ranges. 
#int 	ADL_Overdrive6_State_Reset (int iAdapterIndex, int iStateType)
# 	Function to reset the Overdrive clock ranges to default. 
#int 	ADL_Overdrive6_CurrentStatus_Get (int iAdapterIndex, ADLOD6CurrentStatus *lpCurrentStatus)
# 	Function to retrieve current Overdrive and performance-related activity. 
##int 	ADL_Overdrive6_ThermalController_Caps (int iAdapterIndex, ADLOD6ThermalControllerCaps *lpThermalControllerCaps)
# 	Function to retrieve capabilities of the GPU thermal controller. 
#int 	ADL_Overdrive6_Temperature_Get (int iAdapterIndex, int *lpTemperature)
# 	Function to retrieve GPU temperature from the thermal controller. 
#int 	ADL_Overdrive6_FanSpeed_Get (int iAdapterIndex, ADLOD6FanSpeedInfo *lpFanSpeedInfo)
# 	Function to retrieve the fan speed reported by the thermal controller. 
#int 	ADL_Overdrive6_FanSpeed_Set (int iAdapterIndex, ADLOD6FanSpeedValue *lpFanSpeedValue)
# 	Function to set the fan speed. 
#int 	ADL_Overdrive6_FanSpeed_Reset (int iAdapterIndex)
# 	Function to reset the fan speed to the default. 
#int 	ADL_Overdrive6_PowerControl_Caps (int iAdapterIndex, int *lpSupported)
# 	Function to check for PowerControl capabilities. 
#int 	ADL_Overdrive6_PowerControlInfo_Get (int iAdapterIndex, ADLOD6PowerControlInfo *lpPowerControlInfo)
# 	Function to get the PowerControl adjustment range. 
#int 	ADL_Overdrive6_PowerControl_Get (int iAdapterIndex, int *lpCurrentValue, int *lpDefaultValue)
# 	Function to get the current and default PowerControl adjustment values. 
#int 	ADL_Overdrive6_PowerControl_Set (int iAdapterIndex, int iValue)
# 	Function to set the current PowerControl adjustment value.

ADL_Display_WriteAndReadI2CRev_Get = _libadl.ADL_Display_WriteAndReadI2CRev_Get
ADL_Display_WriteAndReadI2CRev_Get.restype = c_int
ADL_Display_WriteAndReadI2CRev_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Display_WriteAndReadI2C = _libadl.ADL_Display_WriteAndReadI2C
ADL_Display_WriteAndReadI2C.restype = c_int
ADL_Display_WriteAndReadI2C.argtypes = [c_int, POINTER(ADLI2C)]

ADL_Display_DDCBlockAccess_Get = _libadl.ADL_Display_DDCBlockAccess_Get
ADL_Display_DDCBlockAccess_Get.restype = c_int
ADL_Display_DDCBlockAccess_Get.argtypes = [c_int, c_int, c_int, c_int, c_int, c_char_p, POINTER(c_int), c_char_p]

ADL_Display_DDCInfo_Get = _libadl.ADL_Display_DDCInfo_Get
ADL_Display_DDCInfo_Get.restype = c_int
ADL_Display_DDCInfo_Get.argtypes = [c_int, c_int, POINTER(ADLDDCInfo)]

#TODO: Implement and test ADL_Display_DDCInfo2_Get
#int 	ADL_Display_DDCInfo2_Get (int iAdapterIndex, int iDisplayIndex, ADLDDCInfo2 *lpInfo)
# 	Function to get the DDC info.

ADL_Display_EdidData_Get = _libadl.ADL_Display_EdidData_Get
ADL_Display_EdidData_Get.restype = c_int
ADL_Display_EdidData_Get.argtypes = [c_int, c_int, POINTER(ADLDisplayEDIDData)]

ADL_Workstation_Caps = _libadl.ADL_Workstation_Caps
ADL_Workstation_Caps.restype = c_int
ADL_Workstation_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Workstation_Stereo_Get = _libadl.ADL_Workstation_Stereo_Get
ADL_Workstation_Stereo_Get.restype = c_int
ADL_Workstation_Stereo_Get.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

ADL_Workstation_Stereo_Set = _libadl.ADL_Workstation_Stereo_Set
ADL_Workstation_Stereo_Set.restype = c_int
ADL_Workstation_Stereo_Set.argtypes = [c_int, c_int]

ADL_Workstation_AdapterNumOfGLSyncConnectors_Get = _libadl.ADL_Workstation_AdapterNumOfGLSyncConnectors_Get
ADL_Workstation_AdapterNumOfGLSyncConnectors_Get.restype = c_int
ADL_Workstation_AdapterNumOfGLSyncConnectors_Get.argtypes = [c_int, POINTER(c_int)]

ADL_Workstation_DisplayGenlockCapable_Get = _libadl.ADL_Workstation_DisplayGenlockCapable_Get
ADL_Workstation_DisplayGenlockCapable_Get.restype = c_int
ADL_Workstation_DisplayGenlockCapable_Get.argtypes = [c_int, c_int, POINTER(c_int)]

ADL_Workstation_GLSyncModuleDetect_Get = _libadl.ADL_Workstation_GLSyncModuleDetect_Get
ADL_Workstation_GLSyncModuleDetect_Get.restype = c_int
ADL_Workstation_GLSyncModuleDetect_Get.argtypes = [c_int, c_int, POINTER(ADLGLSyncModuleID)]

ADL_Workstation_GLSyncModuleInfo_Get = _libadl.ADL_Workstation_GLSyncModuleInfo_Get
ADL_Workstation_GLSyncModuleInfo_Get.restype = c_int
ADL_Workstation_GLSyncModuleInfo_Get.argtypes = [c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(POINTER(ADLGLSyncPortCaps))]

ADL_Workstation_GLSyncGenlockConfiguration_Get = _libadl.ADL_Workstation_GLSyncGenlockConfiguration_Get
ADL_Workstation_GLSyncGenlockConfiguration_Get.restype = c_int
ADL_Workstation_GLSyncGenlockConfiguration_Get.argtypes = [c_int, c_int, c_int, POINTER(ADLGLSyncGenlockConfig)]

ADL_Workstation_GLSyncGenlockConfiguration_Set = _libadl.ADL_Workstation_GLSyncGenlockConfiguration_Set
ADL_Workstation_GLSyncGenlockConfiguration_Set.restype = c_int
ADL_Workstation_GLSyncGenlockConfiguration_Set.argtypes = [c_int, c_int, ADLGLSyncGenlockConfig]

ADL_Workstation_GLSyncPortState_Get = _libadl.ADL_Workstation_GLSyncPortState_Get
ADL_Workstation_GLSyncPortState_Get.restype = c_int
ADL_Workstation_GLSyncPortState_Get.argtypes = [c_int, c_int, c_int, c_int, POINTER(ADLGlSyncPortInfo), POINTER(POINTER(c_int))]

ADL_Workstation_GLSyncPortState_Set = _libadl.ADL_Workstation_GLSyncPortState_Set
ADL_Workstation_GLSyncPortState_Set.restype = c_int
ADL_Workstation_GLSyncPortState_Set.argtypes = [c_int, c_int, ADLGlSyncPortControl]

ADL_Workstation_DisplayGLSyncMode_Get = _libadl.ADL_Workstation_DisplayGLSyncMode_Get
ADL_Workstation_DisplayGLSyncMode_Get.restype = c_int
ADL_Workstation_DisplayGLSyncMode_Get.argtypes = [c_int, c_int, POINTER(ADLGlSyncMode)]

ADL_Workstation_DisplayGLSyncMode_Set = _libadl.ADL_Workstation_DisplayGLSyncMode_Set
ADL_Workstation_DisplayGLSyncMode_Set.restype = c_int
ADL_Workstation_DisplayGLSyncMode_Set.argtypes = [c_int, c_int, ADLGlSyncMode]

ADL_Workstation_GLSyncSupportedTopology_Get = _libadl.ADL_Workstation_GLSyncSupportedTopology_Get
ADL_Workstation_GLSyncSupportedTopology_Get.restype = c_int
ADL_Workstation_GLSyncSupportedTopology_Get.argtypes = [c_int, c_int, POINTER(ADLGlSyncMode2), POINTER(c_int), POINTER(POINTER(ADLGlSyncMode2))]

ADL_Workstation_LoadBalancing_Get = _libadl.ADL_Workstation_LoadBalancing_Get
ADL_Workstation_LoadBalancing_Get.restype = c_int
ADL_Workstation_LoadBalancing_Get.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]

ADL_Workstation_LoadBalancing_Set = _libadl.ADL_Workstation_LoadBalancing_Set
ADL_Workstation_LoadBalancing_Set.restype = c_int
ADL_Workstation_LoadBalancing_Set.argtypes = [c_int]

ADL_Workstation_LoadBalancing_Caps = _libadl.ADL_Workstation_LoadBalancing_Caps
ADL_Workstation_LoadBalancing_Caps.restype = c_int
ADL_Workstation_LoadBalancing_Caps.argtypes = [c_int, POINTER(c_int), POINTER(c_int)]

#TODO: IMplement and test following Workstation APIs
#int 	ADL_Workstation_DeepBitDepth_Get (int *lpCurDBDState, int *lpDefDBDState, int *lpCurGrayscale, int *lpDefGrayscale, int *lpCurBypass, int *lpDefBypass)
# 	Function to get current requested state of Deep Bit Depth and related settings. 
#int 	ADL_Workstation_DeepBitDepth_Set (int iDBDState, int iGrayscale, int iBypassGamma)
# 	Function to set requested state of Deep Bit Depth and related settings. 
#int 	ADL_Workstation_ECC_Caps (int iAdapterIndex, int *lpSupported)
# 	Function to get ECC (Error Correction Code) Capabilities on the specified adapter. This function implements the CI call to get ECC (Error Correction Code) Capabilities on the specified adapter. 
#int 	ADL_Workstation_ECC_Get (int iAdapterIndex, int *lpDefaultMode, int *lpCurrentMode, int *lpDesiredMode)
# 	Function to get ECC (Error Correction Code) current and desired states on the specified adapter. This function implements the CI call to get ECC (Error Correction Code) current mode(driver applied mode) and the desired mode (user requested mode) on the specified adapter. 
#int 	ADL_Workstation_ECCData_Get (int iAdapterIndex, ADLECCData *lpAdlEccData)
# 	Function to get ECC statistics on the specified adapter. This function implements the CI call to get SEC(Single Error Correct) and DED(Double Error Detect) Counts on the specified adapter. 
#int 	ADL_Workstation_ECC_Set (int iAdapterIndex, int iDesiredMode)
# 	Function to set ECC Mode on the specified adapter This function implements the CI call to set ECC (Error Correction Code) to turn on and off this feature on the specified adapter.

#TODO Implement and test following Application Profiles APIs
#int 	ADL_ApplicationProfiles_System_Reload ()
# 	Function to Reload System appprofiles. 
#int 	ADL_ApplicationProfiles_User_Load ()
# 	Function to Load User appprofiles. 
#int 	ADL_ApplicationProfiles_User_Unload ()
# 	Function to Unload User appprofiles. 
#int 	ADL_ApplicationProfiles_ProfileOfAnApplication_Search (const char *FileName, const char *Path, const char *Version, const char *AppProfileArea, ADLApplicationProfile **lppProfile)
# 	Function to retrieve the profile of an application defined in driver. 
#int 	ADL_ApplicationProfiles_HitLists_Get (int iListType, int *lpNumApps, ADLApplicationData **lppAppList)
# 	Function to retrieve the recent application list from registry.


if _platform == "Linux" or _os == "posix":
    ADL_Adapter_MemoryInfo_Get = _libadl.ADL_Adapter_MemoryInfo_Get
    ADL_Adapter_MemoryInfo_Get.restype = c_int
    ADL_Adapter_MemoryInfo_Get.argtypes = [c_int, POINTER(ADLMemoryInfo)]
    
    # missing in linux dso, but listed in the API docs
    #ADL_Controller_Color_Set = _libadl.ADL_Controller_Color_Set
    #ADL_Controller_Color_Set.restype = c_int
    #ADL_Controller_Color_Set.argtypes = [c_int, c_int, ADLGamma]
    
    #ADL_Controller_Color_Get = _libadl.ADL_Controller_Color_Get
    #ADL_Controller_Color_Get.restype = c_int
    #ADL_Controller_Color_Get.argtypes = [c_int, c_int, POINTER(ADLGamma), POINTER(ADLGamma), POINTER(ADLGamma), POINTER(ADLGamma)]
    
    ADL_DesktopConfig_Get = _libadl.ADL_DesktopConfig_Get
    ADL_DesktopConfig_Get.restype = c_int
    ADL_DesktopConfig_Get.argtypes = [c_int, POINTER(c_int)]
    
    ADL_DesktopConfig_Set = _libadl.ADL_DesktopConfig_Set
    ADL_DesktopConfig_Set.restype = c_int
    ADL_DesktopConfig_Set.argtypes = [c_int, c_int]
    
    ADL_NumberOfDisplayEnable_Get = _libadl.ADL_NumberOfDisplayEnable_Get
    ADL_NumberOfDisplayEnable_Get.restype = c_int
    ADL_NumberOfDisplayEnable_Get.argtypes = [c_int, POINTER(c_int)]
    
    ADL_DisplayEnable_Set = _libadl.ADL_DisplayEnable_Set
    ADL_DisplayEnable_Set.restype = c_int
    ADL_DisplayEnable_Set.argtypes = [c_int, POINTER(c_int), c_int, c_int]
    
    ADL_Display_IdentifyDisplay = _libadl.ADL_Display_IdentifyDisplay
    ADL_Display_IdentifyDisplay.restype = c_int
    ADL_Display_IdentifyDisplay.argtypes = [c_int, c_int, c_int, c_int, c_int, c_int, c_int]
    
    ADL_Display_LUTColor_Set = _libadl.ADL_Display_LUTColor_Set
    ADL_Display_LUTColor_Set.restype = c_int
    ADL_Display_LUTColor_Set.argtypes = [c_int, c_int, ADLGamma]
    
    ADL_Display_LUTColor_Get = _libadl.ADL_Display_LUTColor_Get
    ADL_Display_LUTColor_Get.restype = c_int
    ADL_Display_LUTColor_Get.argtypes = [c_int, c_int, POINTER(ADLGamma), POINTER(ADLGamma), POINTER(ADLGamma), POINTER(ADLGamma)]
    
    ADL_Adapter_XScreenInfo_Get = _libadl.ADL_Adapter_XScreenInfo_Get
    ADL_Adapter_XScreenInfo_Get.restype = c_int
    ADL_Adapter_XScreenInfo_Get.argtypes = [LPXScreenInfo, c_int]
    
    ADL_Display_XrandrDisplayName_Get = _libadl.ADL_Display_XrandrDisplayName_Get
    ADL_Display_XrandrDisplayName_Get.restype = c_int
    ADL_Display_XrandrDisplayName_Get.argtypes = [c_int, c_int, c_char_p, c_int]

    # TODO: implement the following linux apis: 
#    Linux Specific APIs

#Functions
#int 	ADL_Adapter_MemoryInfo_Get (int iAdapterIndex, ADLMemoryInfo *lpMemoryInfo)
# 	Function to retrieve memory information from the adapter. 
#int 	ADL_Adapter_ConfigMemory_Get (int iADLAdapter, int iScreenWidth, int iScreenHeight, int displayFeatureMask, int numDisplays, ADLMemoryDisplayFeatures *displayFeatureList, int *iNumMemTypes, ADLMemoryRequired **lppMemRequired)
# 	Function to get the memory configuration of an adapter. 
#int 	ADL_Adapter_ObservedClockInfo_Get (int iAdapterIndex, int *lpCoreClock, int *lpMemoryClock)
# 	Function to get the core and memory clock info of an adapter.  This is the clock displayed on CCC information center.          Specific logic is used to select appropriate clock for display in current configuration. 
#int 	ADL_Controller_Color_Set (int iAdapterIndex, int iControllerIndex, ADLGamma adlGamma)
# 	Function to set the current gamma value for a controller. 
#int 	ADL_Controller_Color_Get (int iAdapterIndex, int iControllerIndex, ADLGamma *lpGammaCurrent, ADLGamma *lpGammaDefault, ADLGamma *lpGammaMin, ADLGamma *lpGammaMax)
# 	Function to get the current value of gamma for a controller. 
#int 	ADL_DesktopConfig_Get (int iAdapterIndex, int *lpDesktopConfig)
# 	Function to get the Desktop Configuration. 
#int 	ADL_DesktopConfig_Set (int iAdapterIndex, int iDesktopConfig)
# 	Function to set the Desktop Configuration. 
#int 	ADL_NumberOfDisplayEnable_Get (int iAdapterIndex, int *lpNumberOfDisplays)
# 	Function to retrieve the number of enabled displays. 
#int 	ADL_DisplayEnable_Set (int iAdapterIndex, int *lpDisplayIndexList, int iDisplayListSize, int bPersistOnly)
# 	Function to dynamically enable displays on a GPU. 
#int 	ADL_Display_IdentifyDisplay (int iAdapterIndex, int iDisplayIndex, int iDisplayControllerIndex, int iShow, int iDisplayNum, int iPosX, int iPosY)
# 	Function to set the desktop configuration. 
#int 	ADL_Display_LUTColor_Set (int iAdapterIndex, int iDisplayIndex, ADLGamma adlGamma)
# 	Function to set the current gamma value for a LUT (controller). 
#int 	ADL_Display_LUTColor_Get (int iAdapterIndex, int iDisplayIndex, ADLGamma *lpGammaCurrent, ADLGamma *lpGammaDefault, ADLGamma *lpGammaMin, ADLGamma *lpGammaMax)
# 	Function to get the current value of gamma for a LUT (controller). 
#int 	ADL_Adapter_XScreenInfo_Get (LPXScreenInfo lpXScreenInfo, int iInputSize)
# 	Function to retrieve all X Screen information for all OS-known adapters. 
#int 	ADL_Display_XrandrDisplayName_Get (int iAdapterIndex, int iDisplayIndex, char *lpXrandrDisplayName, int iBuffSize)
# 	Function to retrieve the name of the Xrandr display. 
#int 	ADL_Adapter_Tear_Free_Set (int iAdapter, int iRequested, int *pStatus)
# 	Set the requested tear free desktop setting. 
#int 	ADL_Adapter_Tear_Free_Get (int iAdapter, int *pDefault, int *pRequested, int *pStatus)
# 	Get the requested tear free desktop setting and current status


#TODO: Mark the following as depricated: (e.g. using this @depricate recipe: http://code.activestate.com/recipes/391367-deprecated/
# and stacklevel=2 as shown here: http://docs.python.org/2/library/warnings.html)

#    Deprecated List 
#Global AdapterInfo::strXScreenConfigName [256] 
#Internal x config file screen identifier name. Use XScreenInfo instead. 

#Global ADLDisplayInfo::iDisplayControllerIndex 
#The controller index to which the display is mapped.
# Will not be used in the future

#Global ADL_Adapter_ClockInfo_Get 
#This API has been deprecated because it does not provide accurate clocks when the ASIC is over-clocked. Use the OD5 set of APIs, when OverDrive5 is supported. 

#Global ADL_Display_AdapterID_Get 
#This API will be removed. Use the duplicate API ADL_Adapter_ID_Get() 

#Global ADL_Display_TVCaps_Get 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_TV_Standard_Set 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_TV_Standard_Get 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_CV_DongleSettings_Get 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_CV_DongleSettings_Set 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_CV_DongleSettings_Reset 
#Dropping support for component, composite, and S-Video connectors. 

#Global ADL_Controller_Color_Set 
#This API has been deprecated because the controller index is no longer used with DAL2. Replaced by ADL_Display_LUTColor_Set 

#Global ADL_Controller_Color_Get 
#This API has been deprecated because the controller index is no longer used with DAL2. Replaced by ADL_Display_LUTColor_Get 

#Global ADL_DesktopConfig_Get 
#This API has been deprecated because it was only used for RandR 1.1 (Red Hat 5.x) distributions which is now not supported. 

#Global ADL_DesktopConfig_Set 
#This API has been deprecated because it was only used for RandR 1.1 (Red Hat 5.x) distributions which is now not supported. 

#Global ADL_NumberOfDisplayEnable_Get 
#This API has been deprecated because it was only used for RandR 1.1 (Red Hat 5.x) distributions which is now not supported. 

#Global ADL_DisplayEnable_Set 
#This API has been deprecated because it was only used for RandR 1.1 (Red Hat 5.x) distributions which is now not supported. 

#Group define_desktop_config 
#This API has been deprecated because it was only used for RandR 1.1 (Red Hat 5.x) distributions which is now not supported. 

#Group define_tv_caps 
#Dropping support for TV displays 

#Group define_cv_dongle 
#Dropping support for Component Video displays