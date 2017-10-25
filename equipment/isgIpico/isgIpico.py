#!/usr/bin/env python
# filename: isgIpico.py

"""

isgIpico control program

"""

import wx
import telnetlib
import time
import sys

HOSTNAME = 'RLEHEPHAESTUS.MIT.EDU'
PASSWORD = 'ISGFUN'
IPCOMMAND = 'IPADDR'
CMD_ACC = 'ACC'
CMD_CHL = 'CHL'
CMD_DRT = 'DRT'
CMD_VEL = 'VEL'

TIMEOUT = 5

ID_ABOUT = 8001
ID_EXIT  = 8002
ID_CONNECT = 8003

SLIDER_HEIGHT=80


strLabelRel = "Relative Position"
strLabelVel = "Velocity"
strLabelAcc = "Acceleration"


# SLIDER CONSTANTS
ACC_MAX = 1000
ACC_MIN = 16
ACC_STARTUP = 500

VEL_MAX = 1000
VEL_MIN = 1
VEL_STARTUP = 500

REL_MAX = 200
REL_MIN = 0 
REL_STARTUP = 60


class DemoPanel(wx.Panel):
    """This Panel hold two simple buttons, but doesn't really do anything."""
    def __init__(self, parent, *args, **kwargs):
        """Create the DemoPanel."""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent  # Sometimes one can use inline Comments

        NothingBtn = wx.Button(self, label="Do Nothing with a long label")
        NothingBtn.Bind(wx.EVT_BUTTON, self.DoNothing )

        MsgBtn = wx.Button(self, label="Send Message")
        MsgBtn.Bind(wx.EVT_BUTTON, self.OnMsgBtn )

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(NothingBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        Sizer.Add(MsgBtn, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizerAndFit(Sizer)

    def DoNothing(self, event=None):
        """Do nothing."""
        pass

    def OnMsgBtn(self, event=None):
        """Bring up a wx.MessageDialog with a useless message."""
        dlg = wx.MessageDialog(self,
                               message='A completely useless message',
                               caption='A Message Box',
                               style=wx.OK|wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()


#### a panel to control a motor ####
class panelAxisStage(wx.Panel):
    """This is a panel for a picoStage"""
    def __init__(self,parent,*args,**kwargs):
        wx.Panel.__init__(self,parent,*args,**kwargs)
        self.parent = parent

        self.ipicoHandle = -1

        self.LM1rel = REL_STARTUP
        self.LM2rel = REL_STARTUP
        self.LM3rel = REL_STARTUP
        self.LM4rel = REL_STARTUP
        self.LM5rel = REL_STARTUP
        self.LM1vel = VEL_STARTUP
        self.LM2vel = VEL_STARTUP
        self.LM3vel = VEL_STARTUP
        self.LM4vel = VEL_STARTUP
        self.LM5vel = VEL_STARTUP
        self.LM1acc = ACC_STARTUP
        self.LM2acc = ACC_STARTUP
        self.LM3acc = ACC_STARTUP
        self.LM4acc = ACC_STARTUP
        self.LM5acc = ACC_STARTUP

        self.LM12rel = REL_STARTUP
        self.LM12vel = VEL_STARTUP
        self.LM12acc = ACC_STARTUP

        self.LM45rel = REL_STARTUP
        self.LM45vel = VEL_STARTUP
        self.LM45acc = ACC_STARTUP

        self.LM45ROLLrel = REL_STARTUP
        self.LM45ROLLvel = VEL_STARTUP
        self.LM45ROLLacc = ACC_STARTUP

        self.LMFArel    = REL_STARTUP
        self.LMFAvel    = VEL_STARTUP
        self.LMFAacc    = ACC_STARTUP


        self.RM1rel = REL_STARTUP
        self.RM2rel = REL_STARTUP
        self.RM3rel = REL_STARTUP
        self.RM4rel = REL_STARTUP
        self.RM5rel = REL_STARTUP
        self.RM1vel = VEL_STARTUP
        self.RM2vel = VEL_STARTUP
        self.RM3vel = VEL_STARTUP
        self.RM4vel = VEL_STARTUP
        self.RM5vel = VEL_STARTUP
        self.RM1acc = ACC_STARTUP
        self.RM2acc = ACC_STARTUP
        self.RM3acc = ACC_STARTUP
        self.RM4acc = ACC_STARTUP
        self.RM5acc = ACC_STARTUP

        self.RM12rel = REL_STARTUP
        self.RM12vel = VEL_STARTUP
        self.RM12acc = ACC_STARTUP

        self.RM45rel = REL_STARTUP
        self.RM45vel = VEL_STARTUP
        self.RM45acc = ACC_STARTUP

        self.RMFArel    = REL_STARTUP
        self.RMFAvel    = VEL_STARTUP
        self.RMFAacc    = ACC_STARTUP        

        

        #### the command log window
        self.logger = wx.TextCtrl(self,5,"",wx.Point(300,20),wx.Size(200,500),wx.TE_MULTILINE | wx.TE_READONLY)
        self.inputCmd = wx.TextCtrl(self,-1,"",wx.Point(300,20),wx.Size(200,20))
        wx.EVT_TEXT(self,self.inputCmd.GetId(),self.EvtText)
        self.inputCmdText = ''
        buttonSendInputCmd = wx.Button(self,label="Send Command")
        buttonSendInputCmd.Bind(wx.EVT_BUTTON,self.OnButtonSendInputCmd)

        #### ipico connection window
        buttonConnect = wx.Button(self,label="Connect to iPico Stage")
        buttonConnect.Bind(wx.EVT_BUTTON,self.OnButtonConnect)
        buttonDisconnect = wx.Button(self,label="Disconnect from iPico Stage")
        buttonDisconnect.Bind(wx.EVT_BUTTON,self.OnButtonDisconnect)        


        #### query buttons
        buttonQAcc = wx.Button(self,label="Query accel")
        buttonQAcc.Bind(wx.EVT_BUTTON,self.OnButtonQAcc)
        buttonQChl = wx.Button(self,label="Query channel")
        buttonQChl.Bind(wx.EVT_BUTTON,self.OnButtonQChl)
        buttonQDrt = wx.Button(self,label="Query drt")
        buttonQDrt.Bind(wx.EVT_BUTTON,self.OnButtonQDrt)
        buttonQVel = wx.Button(self,label="Query vel")
        buttonQVel.Bind(wx.EVT_BUTTON,self.OnButtonQVel)

        #### sliders
        self.Bind(wx.EVT_SLIDER,self.SliderUpdate)

        #### the stage control window
        ## Left Stage ##

        self.LLabelRel = wx.StaticText(self,-1,strLabelRel,wx.Point(15,30))
        #SizerLLabelRel = wx.BoxSizer(wx.HORIZONTAL)
        #SizerLLabelRel.Add(self.LLabelRel,0,wx.ALIGN_CENTER|wx.ALL,5)

        self.LLabelVel = wx.StaticText(self,-1,strLabelVel,wx.Point(15,30))
        self.LLabelAcc = wx.StaticText(self,-1,strLabelAcc,wx.Point(15,30))
        
        
        # Motor 1
        buttonLM1Fwd = wx.Button(self,label="^")
        buttonLM1Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM1Fwd)
        buttonLM1Rev = wx.Button(self,label="v")
        buttonLM1Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM1Rev)
        self.LM1relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM1velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM1accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
       
        # Motor 2
        buttonLM2Fwd = wx.Button(self,label="^")
        buttonLM2Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM2Fwd)
        buttonLM2Rev = wx.Button(self,label="v")
        buttonLM2Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM2Rev)
        self.LM2relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM2velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM2accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 3
        buttonLM3Fwd = wx.Button(self,label="^")
        buttonLM3Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM3Fwd)
        buttonLM3Rev = wx.Button(self,label="v")
        buttonLM3Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM3Rev)
        self.LM3relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM3velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM3accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        
        # Motor 4
        buttonLM4Fwd = wx.Button(self,label="^")
        buttonLM4Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM4Fwd)
        buttonLM4Rev = wx.Button(self,label="v")
        buttonLM4Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM4Rev)
        self.LM4relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM4velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM4accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 5
        buttonLM5Fwd = wx.Button(self,label="^")
        buttonLM5Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM5Fwd)
        buttonLM5Rev = wx.Button(self,label="v")
        buttonLM5Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM5Rev)
        self.LM5relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM5velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM5accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 1+2
        buttonLM12Fwd = wx.Button(self,label="^")
        buttonLM12Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM12Fwd)
        buttonLM12Rev = wx.Button(self,label="v")
        buttonLM12Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM12Rev)
        self.LM12relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM12velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM12accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS) 


        # Motor 4+5
        buttonLM45Fwd = wx.Button(self,label="^")
        buttonLM45Fwd.Bind(wx.EVT_BUTTON,self.OnButtonLM45Fwd)
        buttonLM45Rev = wx.Button(self,label="v")
        buttonLM45Rev.Bind(wx.EVT_BUTTON,self.OnButtonLM45Rev)
        self.LM45relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM45velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LM45accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS) 

        # Motor for Fiber Angle
        buttonLMFAFwd = wx.Button(self,label="^")
        buttonLMFAFwd.Bind(wx.EVT_BUTTON,self.OnButtonLMFAFwd)
        buttonLMFARev = wx.Button(self,label="v")
        buttonLMFARev.Bind(wx.EVT_BUTTON,self.OnButtonLMFARev)
        self.LMFArelSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LMFAvelSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.LMFAaccSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        



        ## Right Stage ##
        # Motor 1
        buttonRM1Fwd = wx.Button(self,label="^")
        buttonRM1Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM1Fwd)
        buttonRM1Rev = wx.Button(self,label="v")
        buttonRM1Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM1Rev)
        self.RM1relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM1velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM1accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 2
        buttonRM2Fwd = wx.Button(self,label="^")
        buttonRM2Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM2Fwd)
        buttonRM2Rev = wx.Button(self,label="v")
        buttonRM2Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM2Rev)
        self.RM2relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM2velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM2accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 3
        buttonRM3Fwd = wx.Button(self,label="^")
        buttonRM3Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM3Fwd)
        buttonRM3Rev = wx.Button(self,label="v")
        buttonRM3Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM3Rev)
        self.RM3relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM3velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM3accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 4
        buttonRM4Fwd = wx.Button(self,label="^")
        buttonRM4Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM4Fwd)
        buttonRM4Rev = wx.Button(self,label="v")
        buttonRM4Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM4Rev)
        self.RM4relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)        
        self.RM4velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM4accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        
        # Motor 5
        buttonRM5Fwd = wx.Button(self,label="^")
        buttonRM5Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM5Fwd)
        buttonRM5Rev = wx.Button(self,label="v")
        buttonRM5Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM5Rev)
        self.RM5relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM5velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM5accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor 1+2
        buttonRM12Fwd = wx.Button(self,label="^")
        buttonRM12Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM12Fwd)
        buttonRM12Rev = wx.Button(self,label="v")
        buttonRM12Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM12Rev)
        self.RM12relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM12velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM12accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)       

        # Motor 4+5
        buttonRM45Fwd = wx.Button(self,label="^")
        buttonRM45Fwd.Bind(wx.EVT_BUTTON,self.OnButtonRM45Fwd)
        buttonRM45Rev = wx.Button(self,label="v")
        buttonRM45Rev.Bind(wx.EVT_BUTTON,self.OnButtonRM45Rev)
        self.RM45relSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM45velSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RM45accSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)

        # Motor for Fiber Angle
        buttonRMFAFwd = wx.Button(self,label="^")
        buttonRMFAFwd.Bind(wx.EVT_BUTTON,self.OnButtonRMFAFwd)
        buttonRMFARev = wx.Button(self,label="v")
        buttonRMFARev.Bind(wx.EVT_BUTTON,self.OnButtonRMFARev)
        self.RMFArelSlider = wx.Slider(self,-1,REL_STARTUP,REL_MIN,REL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RMFAvelSlider = wx.Slider(self,-1,VEL_STARTUP,VEL_MIN,VEL_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)
        self.RMFAaccSlider = wx.Slider(self,-1,ACC_STARTUP,ACC_MIN,ACC_MAX, (0,0),(75, SLIDER_HEIGHT),wx.SL_VERTICAL|wx.SL_LABELS)



        ## Left Fwd-Control Sizer
        SizerLeftFwdControl = wx.BoxSizer(wx.HORIZONTAL)
        SizerLeftFwdControl.Add(buttonLM1Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftFwdControl.Add(buttonLM2Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)        
        SizerLeftFwdControl.Add(buttonLM3Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftFwdControl.Add(buttonLM4Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftFwdControl.Add(buttonLM5Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)

        ## Left Rev-Control Sizer
        SizerLeftRevControl = wx.BoxSizer(wx.HORIZONTAL)
        SizerLeftRevControl.Add(buttonLM1Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRevControl.Add(buttonLM2Rev,0,wx.ALIGN_CENTER|wx.ALL,5)        
        SizerLeftRevControl.Add(buttonLM3Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRevControl.Add(buttonLM4Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRevControl.Add(buttonLM5Rev,0,wx.ALIGN_CENTER|wx.ALL,5)

        ## Left Slider-Control Sizer
        SizerLeftRel = wx.GridSizer(rows=1,cols=5)
        SizerLeftRel.Add(self.LM1relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRel.Add(self.LM2relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRel.Add(self.LM3relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRel.Add(self.LM4relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftRel.Add(self.LM5relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftVel = wx.GridSizer(rows=1,cols=5)
        SizerLeftVel.Add(self.LM1velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftVel.Add(self.LM2velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftVel.Add(self.LM3velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftVel.Add(self.LM4velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftVel.Add(self.LM5velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftAcc = wx.GridSizer(rows=1,cols=5)
        SizerLeftAcc.Add(self.LM1accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftAcc.Add(self.LM2accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftAcc.Add(self.LM3accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftAcc.Add(self.LM4accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftAcc.Add(self.LM5accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        
        SizerLeftCtrl = wx.GridSizer(rows=3,cols=1)
        #SizerLeftCtrl.Add(SizerLLabelRel,wx.ALIGN_LEFT|wx.ALL,1)
        SizerLeftCtrl.Add(SizerLeftRel,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftCtrl.Add(SizerLeftVel,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftCtrl.Add(SizerLeftAcc,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerLeftComboArrow = wx.GridSizer(rows=2,cols=3)
        SizerLeftComboArrow.Add(buttonLM12Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboArrow.Add(buttonLM45Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerLeftComboArrow.Add(buttonLM45ROLLCW,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboArrow.Add(buttonLMFAFwd,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerLeftComboArrow.Add(buttonLM12Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboArrow.Add(buttonLM45Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerLeftComboArrow.Add(buttonLM45ROLLCCW,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboArrow.Add(buttonLMFARev,0,wx.ALIGN_CENTER|wx.ALL,5)
        
        SizerLeftComboSlider = wx.GridSizer(rows=3,cols=3)
        SizerLeftComboSlider.Add(self.LM12relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LM45relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerLeftComboSlider.Add(self.LM45ROLLrelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LMFArelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerLeftComboSlider.Add(self.LM12velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LM45velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerLeftComboSlider.Add(self.LM45ROLLvelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LMFAvelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerLeftComboSlider.Add(self.LM12accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LM45accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerLeftComboSlider.Add(self.LM45ROLLaccSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftComboSlider.Add(self.LMFAaccSlider,0,wx.ALIGN_CENTER|wx.ALL,5)

        


        ## Right Fwd-Control Sizer
        SizerRightFwdControl = wx.BoxSizer(wx.HORIZONTAL)
        SizerRightFwdControl.Add(buttonRM1Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightFwdControl.Add(buttonRM2Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)        
        SizerRightFwdControl.Add(buttonRM3Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightFwdControl.Add(buttonRM4Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightFwdControl.Add(buttonRM5Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)

        ## Right Rev-Control Sizer
        SizerRightRevControl = wx.BoxSizer(wx.HORIZONTAL)
        SizerRightRevControl.Add(buttonRM1Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightRevControl.Add(buttonRM2Rev,0,wx.ALIGN_CENTER|wx.ALL,5)        
        SizerRightRevControl.Add(buttonRM3Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightRevControl.Add(buttonRM4Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightRevControl.Add(buttonRM5Rev,0,wx.ALIGN_CENTER|wx.ALL,5)

        ## Right velAcc-Control Sizer
        SizerRightVel = wx.GridSizer(rows=3,cols=5)
        SizerRightVel.Add(self.RM1relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM2relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM3relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM4relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM5relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM1velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM2velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM3velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM4velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM5velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM1accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM2accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM3accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM4accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightVel.Add(self.RM5accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerRightComboArrow = wx.GridSizer(rows=2,cols=3)
        SizerRightComboArrow.Add(buttonRM12Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboArrow.Add(buttonRM45Fwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboArrow.Add(buttonRMFAFwd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboArrow.Add(buttonRM12Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboArrow.Add(buttonRM45Rev,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboArrow.Add(buttonRMFARev,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerRightComboSlider = wx.GridSizer(rows=3,cols=3)
        SizerRightComboSlider.Add(self.RM12relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RM45relSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RMFArelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RM12velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RM45velSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RMFAvelSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RM12accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RM45accSlider,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightComboSlider.Add(self.RMFAaccSlider,0,wx.ALIGN_CENTER|wx.ALL,5)


        motorDirectionPanelLeft = wx.Panel(self)         
        imageFile = "fig/motorDirections.JPG"
        self.jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(motorDirectionPanelLeft, -1, self.jpg1, (0,0), (self.jpg1.GetWidth(),self.jpg1.GetHeight()))
        motorDirectionPanelRight = wx.Panel(self)         
        imageFile = "fig/motorDirections.JPG"
        self.jpg2 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(motorDirectionPanelRight, -1, self.jpg1, (0,0), (self.jpg1.GetWidth(),self.jpg1.GetHeight()))


        ## Left Control Sizer
        SizerLeftControl = wx.BoxSizer(wx.VERTICAL)
        SizerLeftControl.Add(motorDirectionPanelLeft,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftControl.Add(SizerLeftFwdControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftControl.Add(SizerLeftRevControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftControl.Add(SizerLeftCtrl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLeftControl.Add(SizerLeftComboArrow,0,wx.ALIGN_LEFT|wx.ALL,5)
        SizerLeftControl.Add(SizerLeftComboSlider,0,wx.ALIGN_LEFT|wx.ALL,5)

        ## Right Control Sizer
        SizerRightControl = wx.BoxSizer(wx.VERTICAL)
        SizerRightControl.Add(motorDirectionPanelRight,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightControl.Add(SizerRightFwdControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightControl.Add(SizerRightRevControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightControl.Add(SizerRightVel,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerRightControl.Add(SizerRightComboArrow,0,wx.ALIGN_LEFT|wx.ALL,5)
        SizerRightControl.Add(SizerRightComboSlider,0,wx.ALIGN_LEFT|wx.ALL,5)

        ## Logger Sizer
        SizerLogger = wx.BoxSizer(wx.VERTICAL)
        SizerLogger.Add(self.inputCmd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLogger.Add(buttonSendInputCmd,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerLogger.Add(self.logger,0,wx.ALIGN_CENTER|wx.ALL,5)

        ## Top Sizer
        SizerTop = wx.BoxSizer(wx.HORIZONTAL)
        SizerTop.Add(buttonConnect,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerTop.Add(buttonDisconnect,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerTop.Add(buttonQAcc,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerTop.Add(buttonQChl,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerTop.Add(buttonQDrt,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerTop.Add(buttonQVel,0,wx.ALIGN_CENTER|wx.ALL,5)


        SizerBottom = wx.BoxSizer(wx.HORIZONTAL)
        SizerBottom.Add(SizerLeftControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        #SizerBottom.Add(self.logger,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerBottom.Add(SizerLogger,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerBottom.Add(SizerRightControl,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerFull = wx.BoxSizer(wx.VERTICAL)
        SizerFull.Add(SizerTop,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerFull.Add(SizerBottom,0,wx.ALIGN_CENTER|wx.ALL,5)

        self.SetSizerAndFit(SizerFull)

    #### function definitions ####
    def EvtText(self,event=None):
        self.inputCmdText = event.GetString()
        #self.logger.AppendText(self.inputCmdText+" :) \n")
        pass
    def OnButtonSendInputCmd(self,event=None):
        self.ipicoHandle.write(self.inputCmdText+"\n")
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")

    def OnButtonConnect(self,event=None):
        self.ipicoHandle = telnetlib.Telnet(HOSTNAME,23)
        try:
            self.ipicoHandle.read_until("Password: ",TIMEOUT)
            self.ipicoHandle.write(PASSWORD + "\n")
            self.ipicoHandle.read_until(">",TIMEOUT)
            self.ipicoHandle.write(IPCOMMAND + "\n")
            msg = self.ipicoHandle.read_until(">",TIMEOUT)
            #msg = "fun!"
        except EOFError:
            msg = "problem initializing :("
            
        self.logger.AppendText(msg+"\n")
        pass

    def OnButtonDisconnect(self,event=None):
        self.ipicoHandle.close()
        pass    

    def OnButtonQAcc(self,event=None):
        self.ipicoHandle.write(CMD_ACC+"\n")
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")
        pass
    def OnButtonQChl(self,event=None):
        self.ipicoHandle.write(CMD_CHL+"\n")
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")
    def OnButtonQDrt(self,event=None):
        self.ipicoHandle.write(CMD_DRT+"\n")
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")
    def OnButtonQVel(self,event=None):
        self.ipicoHandle.write(CMD_VEL+"\n")
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")
    def SliderUpdate(self,event=None):
        self.LM1rel = self.LM1relSlider.GetValue()
        self.LM2rel = self.LM2relSlider.GetValue()
        self.LM3rel = self.LM3relSlider.GetValue()
        self.LM4rel = self.LM4relSlider.GetValue()
        self.LM5rel = self.LM5relSlider.GetValue()
        self.LM12rel = self.LM12relSlider.GetValue()
        self.LM45rel = self.LM45relSlider.GetValue()
        self.LMFArel = self.LMFArelSlider.GetValue()
        #self.LM45ROLLrel = self.LM45ROLLrelSlider.GetValue()
       
        
        self.LM1vel = self.LM1velSlider.GetValue()
        self.LM2vel = self.LM2velSlider.GetValue()
        self.LM3vel = self.LM3velSlider.GetValue()
        self.LM4vel = self.LM4velSlider.GetValue()
        self.LM5vel = self.LM5velSlider.GetValue()
        self.LM12vel = self.LM12velSlider.GetValue()
        self.LM45vel = self.LM45velSlider.GetValue()
        self.LMFAvel = self.LMFAvelSlider.GetValue()
        #self.LM45ROLLvel = self.LM45ROLLvelSlider.GetValue()
        
        self.LM1acc = self.LM1accSlider.GetValue()
        self.LM2acc = self.LM2accSlider.GetValue()
        self.LM3acc = self.LM3accSlider.GetValue()
        self.LM4acc = self.LM4accSlider.GetValue()
        self.LM5acc = self.LM5accSlider.GetValue()
        self.LM12acc = self.LM12accSlider.GetValue()
        self.LM45acc = self.LM45accSlider.GetValue()
        self.LMFAvel = self.LMFAaccSlider.GetValue()
        #self.LM45ROLLacc = self.LM45ROLLaccSlider.GetValue()

        
        self.RM1rel = self.RM1relSlider.GetValue()
        self.RM2rel = self.RM2relSlider.GetValue()
        self.RM3rel = self.RM3relSlider.GetValue()
        self.RM4rel = self.RM4relSlider.GetValue()
        self.RM5rel = self.RM5relSlider.GetValue()
        self.RM12rel = self.RM12relSlider.GetValue()
        self.RM45rel = self.RM45relSlider.GetValue()
        self.RMFArel = self.RMFArelSlider.GetValue()

        self.RM1vel = self.RM1velSlider.GetValue()
        self.RM2vel = self.RM2velSlider.GetValue()
        self.RM3vel = self.RM3velSlider.GetValue()
        self.RM4vel = self.RM4velSlider.GetValue()
        self.RM5vel = self.RM5velSlider.GetValue()
        self.RM12vel = self.RM12velSlider.GetValue()
        self.RM45vel = self.RM45velSlider.GetValue()
        self.RMFAvel = self.RMFAvelSlider.GetValue()

        self.RM1acc = self.RM1accSlider.GetValue()
        self.RM2acc = self.RM2accSlider.GetValue()
        self.RM3acc = self.RM3accSlider.GetValue()
        self.RM4acc = self.RM4accSlider.GetValue()
        self.RM5acc = self.RM5accSlider.GetValue()
        self.RM12acc = self.RM12accSlider.GetValue()
        self.RM45acc = self.RM45accSlider.GetValue()
        self.RMFAacc = self.RMFAaccSlider.GetValue()
        
        
        #%str1 = "pos1 = %d \n" % (self.pos1)
        #self.logger.AppendText(str1)
        pass


    ## Left Stage
    #M1
    def OnButtonLM1Fwd(self,event=None):
        self.logger.AppendText('LM1 Forward\n')
        self.writeToIpicoStage('CHL A3=0\n')
        self.writeToIpicoStage('typ a3 0=0\n')
        self.writeToIpicoStage('mpv a3 0=0\n')
        self.writeToIpicoStage('vel a3 0=%d\n' % self.LM1vel)
        self.writeToIpicoStage('acc a3 0=%d\n' % self.LM1acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=%d\n' % self.LM1rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonLM1Rev(self,event=None):
        self.logger.AppendText('LM1 Reverse\n')
        self.writeToIpicoStage('CHL A3=0\n')
        self.writeToIpicoStage('typ a3 0=0\n')
        self.writeToIpicoStage('mpv a3 0=0\n')
        self.writeToIpicoStage('vel a3 0=%d\n' % self.LM1vel)
        self.writeToIpicoStage('acc a3 0=%d\n' % self.LM1acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=-%d\n' % self.LM1rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass    
    #M2
    def OnButtonLM2Fwd(self,event=None):
        self.logger.AppendText('LM2 Forward\n')
        self.writeToIpicoStage('CHL A4=0\n')
        self.writeToIpicoStage('typ a4 0=0\n')
        self.writeToIpicoStage('mpv a4 0=0\n')
        self.writeToIpicoStage('vel a4 0=%d\n' % self.LM2vel)
        self.writeToIpicoStage('acc a4 0=%d\n' % self.LM2acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=%d\n' % self.LM2rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonLM2Rev(self,event=None):
        self.logger.AppendText('LM2 Reverse\n')
        self.writeToIpicoStage('CHL A4=0n')
        self.writeToIpicoStage('typ a4 0=0\n')
        self.writeToIpicoStage('mpv a4 0=0\n')
        self.writeToIpicoStage('vel a4 0=%d\n' % self.LM2vel)
        self.writeToIpicoStage('acc a4 0=%d\n' % self.LM2acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=-%d\n' % self.LM2rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M3
    def OnButtonLM3Fwd(self,event=None):
        self.logger.AppendText('LM3 Forward\n')
        self.writeToIpicoStage('CHL A3=2\n')
        self.writeToIpicoStage('typ a3 2=0\n')
        self.writeToIpicoStage('mpv a3 2=0\n')
        self.writeToIpicoStage('vel a3 2=%d\n' % self.LM3vel)
        self.writeToIpicoStage('acc a3 2=%d\n' % self.LM3acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=%d\n' % self.LM3rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')       
        pass
    def OnButtonLM3Rev(self,event=None):
        self.logger.AppendText('LM3 Reverse\n')
        self.writeToIpicoStage('CHL A3=2\n')
        self.writeToIpicoStage('typ a3 2=0\n')
        self.writeToIpicoStage('mpv a3 2=0\n')
        self.writeToIpicoStage('vel a3 2=%d\n' % self.LM3vel)
        self.writeToIpicoStage('acc a3 2=%d\n' % self.LM3acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=-%d\n' % self.LM3rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M4
    def OnButtonLM4Fwd(self,event=None):
        self.logger.AppendText('LM4 Forward\n')
        self.writeToIpicoStage('CHL A3=1\n')
        self.writeToIpicoStage('typ a3 1=0\n')
        self.writeToIpicoStage('mpv a3 1=0\n')
        self.writeToIpicoStage('vel a3 1=%d\n' % self.LM4vel)
        self.writeToIpicoStage('acc a3 1=%d\n' % self.LM4acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=%d\n' % self.LM4rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n') 
        pass
    def OnButtonLM4Rev(self,event=None):
        self.logger.AppendText('LM4 Reverse\n')
        self.writeToIpicoStage('CHL A3=1\n')
        self.writeToIpicoStage('typ a3 1=0\n')
        self.writeToIpicoStage('mpv a3 1=0\n')
        self.writeToIpicoStage('vel a3 1=%d\n' % self.LM4vel)
        self.writeToIpicoStage('acc a3 1=%d\n' % self.LM4acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a3=-%d\n' % self.LM4rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n') 
        pass
    #M5
    def OnButtonLM5Fwd(self,event=None):
        self.logger.AppendText('LM5 Forward\n')
        self.writeToIpicoStage('CHL A4=1\n')
        self.writeToIpicoStage('typ a4 1=0\n')
        self.writeToIpicoStage('mpv a4 1=0\n')
        self.writeToIpicoStage('vel a4 1=%d\n' % self.LM5vel)
        self.writeToIpicoStage('acc a4 1=%d\n' % self.LM5acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=%d\n' % self.LM5rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonLM5Rev(self,event=None):
        self.logger.AppendText('LM5 Reverse\n')
        self.writeToIpicoStage('CHL A4=1\n')
        self.writeToIpicoStage('typ a4 1=0\n')
        self.writeToIpicoStage('mpv a4 1=0\n')
        self.writeToIpicoStage('vel a4 1=%d\n' % self.LM5vel)
        self.writeToIpicoStage('acc a4 1=%d\n' % self.LM5acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=-%d\n' % self.LM5rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass

    #M12
    def OnButtonLM12Fwd(self,event=None):
        self.logger.AppendText('LM1 and LM2 Forward\n')

        self.writeToIpicoStage('CHL A3=0\n')
        self.writeToIpicoStage('CHL A4=0\n')

        self.writeToIpicoStage('TYP A3 0=0\n')
        self.writeToIpicoStage('TYP A4 0=0\n')

        self.writeToIpicoStage('VEL A3 0=%d\n' % self.LM12vel)
        self.writeToIpicoStage('VEL A4 0=%d\n' % self.LM12vel)

        self.writeToIpicoStage('ACC A3 0=%d\n' % self.LM12acc)
        self.writeToIpicoStage('ACC A4 0=%d\n' % self.LM12acc)

        self.writeToIpicoStage('mon\n')

        self.writeToIpicoStage('pos\n')

        self.writeToIpicoStage('rel A3=%d\n' % self.LM12rel)
        self.writeToIpicoStage('rel A4=%d\n' % self.LM12rel)

        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
                
        pass
    def OnButtonLM12Rev(self,event=None):
        self.logger.AppendText('LM1 and LM2 Reverse\n')
        self.writeToIpicoStage('CHL A3=0\n')
        self.writeToIpicoStage('CHL A4=0\n')
        self.writeToIpicoStage('TYP A3 0=0\n')
        self.writeToIpicoStage('TYP A4 0=0\n')
        self.writeToIpicoStage('VEL A3 0=%d\n' % self.LM12vel)
        self.writeToIpicoStage('VEL A4 0=%d\n' % self.LM12vel)
        self.writeToIpicoStage('ACC A3 0=%d\n' % self.LM12acc)
        self.writeToIpicoStage('ACC A4 0=%d\n' % self.LM12acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel A3=-%d\n' % self.LM12rel)
        self.writeToIpicoStage('rel A4=-%d\n' % self.LM12rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass

    #M45
    def OnButtonLM45Fwd(self,event=None):
        self.logger.AppendText('LM1 and LM2 Forward\n')
        self.writeToIpicoStage('CHL A3=1\n')
        self.writeToIpicoStage('CHL A4=1\n')
        self.writeToIpicoStage('TYP A3 1=0\n')
        self.writeToIpicoStage('TYP A4 1=0\n')
        self.writeToIpicoStage('VEL A3 1=%d\n' % self.LM45vel)
        self.writeToIpicoStage('VEL A4 1=%d\n' % self.LM45vel)
        self.writeToIpicoStage('ACC A3 1=%d\n' % self.LM45acc)
        self.writeToIpicoStage('ACC A4 1=%d\n' % self.LM45acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel A3=%d\n' % self.LM45rel)
        self.writeToIpicoStage('rel A4=%d\n' % self.LM45rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonLM45Rev(self,event=None):
        self.logger.AppendText('LM1 and LM2 Reverse\n')
        self.writeToIpicoStage('CHL A3=1\n')
        self.writeToIpicoStage('CHL A4=1\n')
        self.writeToIpicoStage('TYP A3 1=0\n')
        self.writeToIpicoStage('TYP A4 1=0\n')
        self.writeToIpicoStage('VEL A3 1=%d\n' % self.LM45vel)
        self.writeToIpicoStage('VEL A4 1=%d\n' % self.LM45vel)
        self.writeToIpicoStage('ACC A3 1=%d\n' % self.LM45acc)
        self.writeToIpicoStage('ACC A4 1=%d\n' % self.LM45acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel A3=-%d\n' % self.LM45rel)
        self.writeToIpicoStage('rel A4=-%d\n' % self.LM45rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass

    # Fiber Angle
    def OnButtonLMFAFwd(self,event=None):
        self.logger.AppendText('Left Fiber Angle Forward\n')
        self.writeToIpicoStage('CHL A4=2\n')
        self.writeToIpicoStage('typ a4 2=0\n')
        self.writeToIpicoStage('mpv a4 2=0\n')
        self.writeToIpicoStage('vel a4 2=%d\n' % self.LMFAvel)
        self.writeToIpicoStage('acc a4 2=%d\n' % self.LMFAacc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=%d\n' % self.LMFArel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonLMFARev(self,event=None):
        self.logger.AppendText('Left Fiber Angle Reverse\n')
        self.writeToIpicoStage('CHL A4=2\n')
        self.writeToIpicoStage('typ a4 2=0\n')
        self.writeToIpicoStage('mpv a4 2=0\n')
        self.writeToIpicoStage('vel a4 2=%d\n' % self.LMFAvel)
        self.writeToIpicoStage('acc a4 2=%d\n' % self.LMFAacc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a4=-%d\n' % self.LMFArel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass




    ## Right Stage
    #M1
    def OnButtonRM1Fwd(self,event=None):
        self.logger.AppendText('RM1 Forward\n')
        self.writeToIpicoStage('CHL A1=0\n')
        self.writeToIpicoStage('typ a1 0=0\n')
        self.writeToIpicoStage('mpv a1 0=0\n')
        self.writeToIpicoStage('vel a1 0=%d\n' % self.RM1vel)
        self.writeToIpicoStage('acc a1 0=%d\n' % self.RM1acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=%d\n' % self.RM1rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM1Rev(self,event=None):
        self.logger.AppendText('RM1 Reverse\n')
        self.writeToIpicoStage('CHL A1=0\n')
        self.writeToIpicoStage('typ a1 0=0\n')
        self.writeToIpicoStage('mpv a1 0=0\n')
        self.writeToIpicoStage('vel a1 0=%d\n' % self.RM1vel)
        self.writeToIpicoStage('acc a1 0=%d\n' % self.RM1acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=-%d\n' % self.RM1rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M2
    def OnButtonRM2Fwd(self,event=None):
        self.logger.AppendText('RM2 Forward\n')
        self.writeToIpicoStage('CHL A2=0\n')
        self.writeToIpicoStage('typ a2 0=0\n')
        self.writeToIpicoStage('mpv a2 0=0\n')
        self.writeToIpicoStage('vel a2 0=%d\n' % self.RM2vel)
        self.writeToIpicoStage('acc a2 0=%d\n' % self.RM2acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=%d\n' % self.RM2rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM2Rev(self,event=None):
        self.logger.AppendText('RM2 Reverse\n')
        self.writeToIpicoStage('CHL A2=0\n')
        self.writeToIpicoStage('typ a2 0=0\n')
        self.writeToIpicoStage('mpv a2 0=0\n')
        self.writeToIpicoStage('vel a2 0=%d\n' % self.RM2vel)
        self.writeToIpicoStage('acc a2 0=%d\n' % self.RM2acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=-%d\n' % self.RM2rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M3
    def OnButtonRM3Fwd(self,event=None):
        self.logger.AppendText('RM3 Forward\n')
        self.writeToIpicoStage('CHL A1=2\n')
        self.writeToIpicoStage('typ a1 2=0\n')
        self.writeToIpicoStage('mpv a1 2=0\n')
        self.writeToIpicoStage('vel a1 2=%d\n' % self.RM3vel)
        self.writeToIpicoStage('acc a1 2=%d\n' % self.RM3acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=%d\n' % self.RM3rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM3Rev(self,event=None):
        self.logger.AppendText('RM3 Reverse\n')
        self.writeToIpicoStage('CHL A1=2\n')
        self.writeToIpicoStage('typ a1 2=0\n')
        self.writeToIpicoStage('mpv a1 2=0\n')
        self.writeToIpicoStage('vel a1 2=%d\n' % self.RM3vel)
        self.writeToIpicoStage('acc a1 2=%d\n' % self.RM3acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=-%d\n' % self.RM3rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M4
    def OnButtonRM4Fwd(self,event=None):
        self.logger.AppendText('RM4 Forward\n')
        self.writeToIpicoStage('CHL A1=1\n')
        self.writeToIpicoStage('typ a1 1=0\n')
        self.writeToIpicoStage('mpv a1 1=0\n')
        self.writeToIpicoStage('vel a1 1=%d\n' % self.RM4vel)
        self.writeToIpicoStage('acc a1 1=%d\n' % self.RM4acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=%d\n' % self.RM4rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM4Rev(self,event=None):
        self.logger.AppendText('RM4 Reverse\n')
        self.writeToIpicoStage('CHL A1=1\n')
        self.writeToIpicoStage('typ a1 1=0\n')
        self.writeToIpicoStage('mpv a1 1=0\n')
        self.writeToIpicoStage('vel a1 1=%d\n' % self.RM4vel)
        self.writeToIpicoStage('acc a1 1=%d\n' % self.RM4acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a1=-%d\n' % self.RM4rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M5
    def OnButtonRM5Fwd(self,event=None):
        self.logger.AppendText('RM5 Forward\n')
        self.writeToIpicoStage('CHL A2=1\n')
        self.writeToIpicoStage('typ a2 1=0\n')
        self.writeToIpicoStage('mpv a2 1=0\n')
        self.writeToIpicoStage('vel a2 1=%d\n' % self.RM5vel)
        self.writeToIpicoStage('acc a2 1=%d\n' % self.RM5acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=%d\n' % self.RM5rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM5Rev(self,event=None):
        self.logger.AppendText('RM5 Reverse\n')
        self.writeToIpicoStage('CHL A2=1\n')
        self.writeToIpicoStage('typ a2 1=0\n')
        self.writeToIpicoStage('mpv a2 1=0\n')
        self.writeToIpicoStage('vel a2 1=%d\n' % self.RM5vel)
        self.writeToIpicoStage('acc a2 1=%d\n' % self.RM5acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=-%d\n' % self.RM5rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    #M12
    def OnButtonRM12Fwd(self,event=None):
        self.logger.AppendText('RM1 and RM2 Forward\n')

        self.writeToIpicoStage('CHL A1=0\n')
        self.writeToIpicoStage('CHL A2=0\n')

        self.writeToIpicoStage('TYP A1 0=0\n')
        self.writeToIpicoStage('TYP A2 0=0\n')

        self.writeToIpicoStage('VEL A1 0=%d\n' % self.RM12vel)
        self.writeToIpicoStage('VEL A2 0=%d\n' % self.RM12vel)

        self.writeToIpicoStage('ACC A1 0=%d\n' % self.RM12acc)
        self.writeToIpicoStage('ACC A2 0=%d\n' % self.RM12acc)

        self.writeToIpicoStage('mon\n')

        self.writeToIpicoStage('pos\n')

        self.writeToIpicoStage('rel A1=%d\n' % self.RM12rel)
        self.writeToIpicoStage('rel A2=%d\n' % self.RM12rel)

        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
                
        pass
    def OnButtonRM12Rev(self,event=None):
        self.logger.AppendText('RM1 and RM2 Reverse\n')

        self.writeToIpicoStage('CHL A1=0\n')
        self.writeToIpicoStage('CHL A2=0\n')

        self.writeToIpicoStage('TYP A1 0=0\n')
        self.writeToIpicoStage('TYP A2 0=0\n')

        self.writeToIpicoStage('VEL A1 0=%d\n' % self.RM12vel)
        self.writeToIpicoStage('VEL A2 0=%d\n' % self.RM12vel)

        self.writeToIpicoStage('ACC A1 0=%d\n' % self.RM12acc)
        self.writeToIpicoStage('ACC A2 0=%d\n' % self.RM12acc)

        self.writeToIpicoStage('mon\n')

        self.writeToIpicoStage('pos\n')

        self.writeToIpicoStage('rel A1=-%d\n' % self.RM12rel)
        self.writeToIpicoStage('rel A2=-%d\n' % self.RM12rel)

        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass


    #M45
    def OnButtonRM45Fwd(self,event=None):
        self.logger.AppendText('RM1 and RM2 Forward\n')
        self.writeToIpicoStage('CHL A1=1\n')
        self.writeToIpicoStage('CHL A2=1\n')
        self.writeToIpicoStage('TYP A1 1=0\n')
        self.writeToIpicoStage('TYP A2 1=0\n')
        self.writeToIpicoStage('VEL A1 1=%d\n' % self.RM45vel)
        self.writeToIpicoStage('VEL A2 1=%d\n' % self.RM45vel)
        self.writeToIpicoStage('ACC A1 1=%d\n' % self.RM45acc)
        self.writeToIpicoStage('ACC A2 1=%d\n' % self.RM45acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel A1=%d\n' % self.RM45rel)
        self.writeToIpicoStage('rel A2=%d\n' % self.RM45rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRM45Rev(self,event=None):
        self.logger.AppendText('RM1 and RM2 Reverse\n')
        self.writeToIpicoStage('CHL A1=1\n')
        self.writeToIpicoStage('CHL A2=1\n')
        self.writeToIpicoStage('TYP A1 1=0\n')
        self.writeToIpicoStage('TYP A2 1=0\n')
        self.writeToIpicoStage('VEL A1 1=%d\n' % self.RM45vel)
        self.writeToIpicoStage('VEL A2 1=%d\n' % self.RM45vel)
        self.writeToIpicoStage('ACC A1 1=%d\n' % self.RM45acc)
        self.writeToIpicoStage('ACC A2 1=%d\n' % self.RM45acc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel A1=-%d\n' % self.RM45rel)
        self.writeToIpicoStage('rel A2=-%d\n' % self.RM45rel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass

    # Fiber Angle
    def OnButtonRMFAFwd(self,event=None):
        self.logger.AppendText('Right Fiber Angle Forward\n')
        self.writeToIpicoStage('CHL A2=2\n')
        self.writeToIpicoStage('typ a2 2=0\n')
        self.writeToIpicoStage('mpv a2 2=0\n')
        self.writeToIpicoStage('vel a2 2=%d\n' % self.RMFAvel)
        self.writeToIpicoStage('acc a2 2=%d\n' % self.RMFAacc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=%d\n' % self.RMFArel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass
    def OnButtonRMFARev(self,event=None):
        self.logger.AppendText('Right Fiber Angle Reverse\n')
        self.writeToIpicoStage('CHL A2=2\n')
        self.writeToIpicoStage('typ a2 2=0\n')
        self.writeToIpicoStage('mpv a2 2=0\n')
        self.writeToIpicoStage('vel a2 2=%d\n' % self.RMFAvel)
        self.writeToIpicoStage('acc a2 2=%d\n' % self.RMFAacc)
        self.writeToIpicoStage('mon\n')
        self.writeToIpicoStage('pos\n')
        self.writeToIpicoStage('rel a2=-%d\n' % self.RMFArel)
        self.writeToIpicoStage('go\n')
        self.writeToIpicoStage('pos\n')
        pass



    


    #### helper functions
    def writeToIpicoStage(self,msg2send):
        self.ipicoHandle.write(msg2send)
        msg = self.ipicoHandle.read_until(">",TIMEOUT)
        self.logger.AppendText(msg+"\n")


#############################################################
######## Now layout the main Frame (the main window) ########
#############################################################
class DemoFrame(wx.Frame):
    """Main Frame holding the Panel."""
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)

        #### Build the menu bar ####
        MenuBar = wx.MenuBar()
        # file menu
        FileMenu = wx.Menu()
        item = FileMenu.Append(ID_ABOUT, text="&About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        item = FileMenu.Append(ID_EXIT, text="&Quit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        # connection menu
        ConnectMenu = wx.Menu()
        item = ConnectMenu.Append(ID_CONNECT,text="&Connect")
        self.Bind(wx.EVT_MENU,self.OnConnect,item)
        MenuBar.Append(FileMenu, "&File")
        MenuBar.Append(ConnectMenu, "&Connect")
        self.SetMenuBar(MenuBar)

        
        #self.logoPanel = wx.Panel(self)         
        #imageFile = "fig/rb.JPG"
        #self.jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #wx.StaticBitmap(self.logoPanel, -1, self.jpg1, (0,0), (self.jpg1.GetWidth(),self.jpg1.GetHeight()))


        #### Add the Widget Panel ####
        self.stageControl = panelAxisStage(self)

        SizerControl = wx.BoxSizer(wx.HORIZONTAL)
        SizerControl.Add(self.stageControl,0,wx.ALIGN_CENTER|wx.ALL,5)

        SizerFrame = wx.BoxSizer(wx.VERTICAL)
        #SizerFrame.Add(self.logoPanel,0,wx.ALIGN_CENTER|wx.ALL,5)
        SizerFrame.Add(SizerControl,0,wx.ALIGN_CENTER|wx.ALL,5)
        self.SetSizerAndFit(SizerFrame)

        self.Fit()

    def OnConnect(self,event=None):
        """try to connect to isg ipico stage"""
        dlg = wx.MessageDialog(self,
                               message ='Connect to: rlehephaestus.mit.edu',
                               caption ='Connect',
                               style=wx.OK|wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy
        
    def OnAbout(self, event=None):
        """About this application"""
        dlg = wx.MessageDialog(self,
                               message='This program controls the ISG optical table',
                               caption='About',
                               style=wx.OK|wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    frame = DemoFrame(None, title="ISG iPico Controller Interface")
    frame.Show()
    app.MainLoop()
