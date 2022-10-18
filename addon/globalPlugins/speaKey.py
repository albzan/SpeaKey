#Copyright 2022 Alberto Zanella
import globalPluginHandler
import inputCore
import appModuleHandler
import ui
import tones
from scriptHandler import script
from logHandler import log

addonHandler.initTranslation()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwargs):
        super(GlobalPlugin, self).__init__(*args, **kwargs)
        self.prevGesture = []
        self.prevModifier = False
        self.isActive = False
    
    def _keyReadCaptor(self, gesture):
        if(':nvda+1' in gesture.identifiers[0].lower()) :
            self.isActive = False
            tones.beep(400,300)
            ui.message(_("SpeaKey mode on"))
        if(gesture.identifiers[0] not in self.prevGesture) :
            self.prevGesture.append(gesture.identifiers[0])
            if(gesture.isCharacter) :
                self.prevGesture = self.prevGesture[-1:]
            else :
                self.prevGesture = self.prevGesture[-2:]
            return inputCore.manager._inputHelpCaptor(gesture)
        tones.beep(400,30)
        return True
    
    @script(gesture="kb:control+escape", description= _("Toggle SpeaKey Mode on and off"), category= "Cattura tasti", bypassInputHelp=True)
    def script_keyReadToggle(self, gesture):
        if(self.isActive) :
            inputCore.manager._captureFunc = None
            ui.message(_("SpeaKey mode off"))
        else :
            inputCore.manager._captureFunc = self._keyReadCaptor
            ui.message(_("SpeaKey mode on"))
        self.isActive = not self.isActive
            
