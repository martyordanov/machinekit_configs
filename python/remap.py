from interpreter import *
from emccanon import MESSAGE
from stdglue import cycle_prolog, cycle_epilog, init_stdglue
import subprocess

# This shows how to create a remapped G code  which can be used as a cycle
# written in Python
#
# Example:
# Assume G84.2 is remapped to Python g842 like so in the [RS274NGC] ini section:
# REMAP=G84.2 argspec=xyzqp python=g842 modalgroup=1
#    
# then executing
#   
#    G84.2 x1 y1 (line1)
#    x3 y3       (line2)
#    y5          (line3)
#    ...
#
#  will execute like:
#   *G84.2 x1 y1
#    G84.2 x3 y3
#    G84.2 x3 y5
#    
# until motion is cleared with G80 or some other motion is executed.
#   
# This enables writing cycles in Python, or as Oword procedures; in the
# latter case the self.motion_mode should be set in the Python epilog.
#
# for a more through example of a cycle prolog, see cycle_prolog in stdglue.py

_sticky_params = dict()

def g842(self,**words):
 
    global _sticky_params

    firstcall = False
    
    # determine whether this is the first or a subsequent call
    c = self.blocks[self.remap_level]
    r = c.executing_remap
    if c.g_modes[1] == r.motion_code:
        # this was the first call.
        # clear the dict to remember all sticky] parameters.
        _sticky_params[r.name] = dict()
        text = "*" + r.name
    else:
        text = r.name
    # merge in new parameters
    _sticky_params[r.name].update(words) 

    # insert your cycle actions here
    for (key,value) in _sticky_params[r.name].items():
        text += "%s%.1f " % (key, value)
    MESSAGE(text)

    # retain the current motion mode
    self.motion_mode = c.executing_remap.motion_code 
    return INTERP_OK

def M207(self,**words):
    """ 
    TC = 0 = ...
    TA = 1 = .
    TB = 2 = ..
    """ 
    accuracy = 0.010
    TC = round(self.params[4000], 4)
    TA = round(self.params[4001], 4)
    TB = round(self.params[4002], 4)
    Tcent = round(self.params[3999], 4)
    #probeData = open("probeData.txt", "a")
    #probeData.write(str(T0) + " | " + str(T1) + " | " + str(T2) + " | " + str(TC) + "\n")
    #probeData.close()

    #if abs(TC)      < accuracy:
    #    TC = 0
    TAcorrection = TA - TC
    TBcorrection = TB - TC
    if abs(TAcorrection) < accuracy:
        TAcorrection = 0

    if abs(TBcorrection) < accuracy:
        TBcorrection = 0

    if  TAcorrection == 0 and TBcorrection == 0:
        # If the towers are leveled, start tweaking R
        if abs(Tcent - TC) < accuracy:
            print "Congrats, Partner!"
        else:
            subprocess.call("~/machinekit/setR.sh " + str(Tcent - TC), shell=True)

    else:
        try: 
            subprocess.call("~/machinekit/setHome.sh " + str(0) + " " + str(TAcorrection) + " " + str(TBcorrection), shell=True)
        except: 
            exit("Could not execute ~/setHome.sh")

    #subprocess.call(["echo", "it seems that subprocess.call is working"])
    #Acc = .05
    #TopLim = T0 + Acc
    #BotLim = T0 - Acc

    #if T1 >= BotLim and T1 <= TopLim:
    #   print "T1 in Range"
    #else:
    #     T1Adj = T1 - T0
    #     MESSAGE ('T1 Adjustment = {0:+.2f} ISSUE M252 TO ADJUST'.format(T1Adj))
    #     self.params[4003] = T1Adj
    #     
    #
    #if T2 >= BotLim and T2 <= TopLim:
    #   print "T2 in Range"
    #else:
    #     T2Adj = T2 - T0
    #     MESSAGE ('T2 Adjustment = {0:+.2f} ISSUE M253 TO ADJUST'.format(T2Adj))    
    #     self.params[4004] = T2Adj
    #     

    #if TC >= BotLim and TC <= TopLim:
    #   print "TC in Range"
    #else:
    #     TCAdj = TC - T0
    #     MESSAGE ('TC Adjustment = {0:+.2f}'.format(TCAdj))    
    #     self.params[4005] = TCAdj
         
  
    return INTERP_OK

def M208 (self, **words): 
    """ 
    TC = 0 = ...
    TA = 1 = .
    TB = 2 = ..
    """ 
    TC = round(self.params[4000], 4)
    TA = round(self.params[4001], 4)
    TB = round(self.params[4002], 4)
    Tcent = round(self.params[3999], 4)
    
    #probeData = open("probeData.txt", "a")
    #probeData.write(str(T0) + " | " + str(T1) + " | " + str(T2) + " | " + str(TC) + "\n")
    #probeData.close()
    print str(TC) + " | " + str(TA) + " | " + str(TB) + " | " + str(Tcent) + "\n"
    print "Deviation from tower C:\n"
    print str(TC - TC) + " | " + str(TA - TC) + " | " + str(TB - TC) + " | " + str(Tcent - TC) + "\n"
