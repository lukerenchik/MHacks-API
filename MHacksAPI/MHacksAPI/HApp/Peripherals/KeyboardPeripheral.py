# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 13:32:03 2022

@author: Derek Joslin
"""

from PyQt5 import QtCore as qc

import PeripheralManager as pm

class KeyboardPeripheral(pm.PeripheralDevice):
    
    def __init__(self, name, KeyBoardHandles):
        super().__init__(name)
        
        # stores all the keys pressed and their order
        self.keyHistory = []
        
        # defines if the control key is on
        self.controlOn = 0
        
        self.DefaultKeyboardHandles = KeyBoardHandles
        self.KeyboardHandles = KeyBoardHandles
        
    def setNewKeyboardHandler(self, newKeyboardHandles):

        self.KeyboardHandles = newKeyboardHandles
        
    def revertToDefaultHandler(self):
        
        self.KeyboardHandles = self.DefaultKeyboardHandles
        
    def setDefaultHandler(self, DefaultKeyboardHandles):
        
        self.DefaultKeyboardHandles = DefaultKeyboardHandles
        self.KeyboardHandles = DefaultKeyboardHandles
        
      
    def handleKeyPressEvent(self, keyPressEvent):
        
        key = keyPressEvent.key()
      
        try:
            
            self.debugString = "Key Pressed: {}".format(chr(key))
            
        except:
            
            self.debugString = "Key Pressed: {}".format(key)
            
        # add the key to the key history list
        self.keyHistory.append(key)
        
        # if more than 100 keys pressed pop
        if len(self.keyHistory) > 100:
            self.keyHistory.pop(0)
            
        if self.controlOn:
            self.controlPressedHandlers(key)
        else:
            try:
                self.normalHandlers(key)
            except Exception as e:
                print("key error: {}".format(e))
            
    def normalHandlers(self, key):
        
        if key == qc.Qt.Key_Space:
            
            self.KeyboardHandles.KeySpaceHandler()
            
        elif key == qc.Qt.Key_Left:
            
            self.KeyboardHandles.KeyLeftHandler()
            
        elif key == qc.Qt.Key_Up:
            
            self.KeyboardHandles.KeyUpHandler()
        
        elif key == qc.Qt.Key_Right:
        
            self.KeyboardHandles.KeyRightHandler()
            
        elif key == qc.Qt.Key_Down:
        
            self.KeyboardHandles.KeyDownHandler()
            
        elif key == qc.Qt.Key_A:
        
            self.KeyboardHandles.KeyAHandler()
            
        elif key == qc.Qt.Key_B:
        
            self.KeyboardHandles.KeyBHandler()
            
        elif key == qc.Qt.Key_C:
        
            self.KeyboardHandles.KeyCHandler()
            
        elif key == qc.Qt.Key_D:
        
            self.KeyboardHandles.KeyDHandler()
            
        elif key == qc.Qt.Key_E:
        
            self.KeyboardHandles.KeyEHandler()
            
        elif key == qc.Qt.Key_F:
        
            self.KeyboardHandles.KeyFHandler()
            
        elif key == qc.Qt.Key_G:
        
            self.KeyboardHandles.KeyGHandler()
            
        elif key == qc.Qt.Key_H:
        
            self.KeyboardHandles.KeyHHandler()
            
        elif key == qc.Qt.Key_I:
        
            self.KeyboardHandles.KeyIHandler()
            
        elif key == qc.Qt.Key_J:
        
            self.KeyboardHandles.KeyJHandler()
            
        elif key == qc.Qt.Key_K:
        
            self.KeyboardHandles.KeyKHandler()
            
        elif key == qc.Qt.Key_L:
        
            self.KeyboardHandles.KeyLHandler()
            
        elif key == qc.Qt.Key_M:
        
            self.KeyboardHandles.KeyMHandler()
            
        elif key == qc.Qt.Key_N:
        
            self.KeyboardHandles.KeyNHandler()
            
        elif key == qc.Qt.Key_O:
        
            self.KeyboardHandles.KeyOHandler()
            
        elif key == qc.Qt.Key_P:
        
            self.KeyboardHandles.KeyPHandler()
            
        elif key == qc.Qt.Key_Q:
        
            self.KeyboardHandles.KeyQHandler()
            
        elif key == qc.Qt.Key_R:
        
            self.KeyboardHandles.KeyRHandler()
            
        elif key == qc.Qt.Key_S:
        
            self.KeyboardHandles.KeySHandler()
            
        elif key == qc.Qt.Key_T:
        
            self.KeyboardHandles.KeyTHandler()
            
        elif key == qc.Qt.Key_U:
        
            self.KeyboardHandles.KeyUHandler()
            
        elif key == qc.Qt.Key_V:
        
            self.KeyboardHandles.KeyVHandler()
            
        elif key == qc.Qt.Key_W:
        
            self.KeyboardHandles.KeyWHandler()
            
        elif key == qc.Qt.Key_X:
        
            self.KeyboardHandles.KeyXHandler()
            
        elif key == qc.Qt.Key_Y:
        
            self.KeyboardHandles.KeyYHandler()
            
        elif key == qc.Qt.Key_Z:
        
            self.KeyboardHandles.KeyZHandler()
            
        elif key == qc.Qt.Key_Backspace:
        
            self.KeyboardHandles.KeyBackSpaceHandler()
            
        elif key == qc.Qt.Key_Enter:
        
            self.KeyboardHandles.KeyEnterHandler()
            
        elif key == qc.Qt.Key_Return:
        
            self.KeyboardHandles.KeyReturnHandler()
            
        elif key == qc.Qt.Key_0:
            
            self.KeyboardHandles.Key0Handler()
        
        elif key == qc.Qt.Key_1:
            
            self.KeyboardHandles.Key1Handler()
            
        elif key == qc.Qt.Key_2:
            
            self.KeyboardHandles.Key2Handler()
            
        elif key == qc.Qt.Key_3:
            
            self.KeyboardHandles.Key3Handler()
            
        elif key == qc.Qt.Key_4:
            
            self.KeyboardHandles.Key4Handler()
            
        elif key == qc.Qt.Key_5:
            
            self.KeyboardHandles.Key5Handler()
            
        elif key == qc.Qt.Key_6:
            
            self.KeyboardHandles.Key6Handler()
            
        elif key == qc.Qt.Key_7:
            
            self.KeyboardHandles.Key7Handler()
            
        elif key == qc.Qt.Key_8:
            
            self.KeyboardHandles.Key8Handler()
            
        elif key == qc.Qt.Key_9:
            
            self.KeyboardHandles.Key9Handler()
            
        elif key == qc.Qt.Key_ParenLeft:
            
            self.KeyboardHandles.KeyParenLeftHandler()
            
        elif key == qc.Qt.Key_ParenRight:
            
            self.KeyboardHandles.KeyParenRightHandler()
            
        elif key == qc.Qt.Key_Comma:
            
            self.KeyboardHandles.KeyCommaHandler()
        
        elif key == qc.Qt.Key_Plus:
            
            self.KeyboardHandles.KeyPlusHandler()
            
        elif key == qc.Qt.Key_Minus:
            
            self.KeyboardHandles.KeyMinusHandler()
            
        elif key == qc.Qt.Key_Asterisk:
            
            self.KeyboardHandles.KeyAsteriskHandler()
            
        elif key == qc.Qt.Key_Period:
            
            self.KeyboardHandles.KeyPeriodHandler()
            
        elif key == qc.Qt.Key_Slash:
            
            self.KeyboardHandles.KeySlashHandler()
            
        elif key == qc.Qt.Key_Colon:
            
            self.KeyboardHandles.KeyColonHandler()
            
        elif key == qc.Qt.Key_Semicolon:
            
            self.KeyboardHandles.KeySemicolonHandler()
            
        elif key == qc.Qt.Key_BracketLeft:
            
            self.KeyboardHandles.BracketLeftHandler()
            
        elif key == qc.Qt.Key_BracketRight:
            
            self.KeyboardHandles.BracketRightHandler()
            
        elif key == qc.Qt.Key_Equal:
            
            self.KeyboardHandles.EqualHandler()
            
        elif key == qc.Qt.Key_Greater:
            
            self.KeyboardHandles.GreaterHandler()
            
        elif key == qc.Qt.Key_Less:
            
            self.KeyboardHandles.LessHandler()
            
        elif key == qc.Qt.Key_QuoteLeft:
            
            self.KeyboardHandles.QuoteLeftHandler()
            
        elif key == qc.Qt.Key_QuoteDbl:
            
            self.KeyboardHandles.QuoteDblHandler()
            
        elif key == qc.Qt.Key_PageUp:
            
            self.KeyboardHandles.KeyPageUpHandler()
            
        elif key == qc.Qt.Key_PageDown:
            
            self.KeyboardHandles.KeyPageDownHandler()
            
        elif key == qc.Qt.Key_F1:
            
            self.KeyboardHandles.KeyF1Handler()
            
        elif key == qc.Qt.Key_F2:
            
            self.KeyboardHandles.KeyF2Handler()
            
        elif key == qc.Qt.Key_F3:
        
            self.KeyboardHandles.KeyF3Handler()
            
        elif key == qc.Qt.Key_F4:
        
            self.KeyboardHandles.KeyF4Handler()
            
        elif key == qc.Qt.Key_F5:
            
            self.KeyboardHandles.KeyF5Handler()
            
        elif key == qc.Qt.Key_F6:
        
            self.KeyboardHandles.KeyF6Handler()
            
        elif key == qc.Qt.Key_F7:
            
            self.KeyboardHandles.KeyF7Handler()
            
        elif key == qc.Qt.Key_F8:
            
            self.KeyboardHandles.KeyF8Handler()
            
        elif key == qc.Qt.Key_F9:
        
            self.KeyboardHandles.KeyF9Handler()
            
        elif key == qc.Qt.Key_F10:
            
            self.KeyboardHandles.KeyF10Handler()
            
        elif key == qc.Qt.Key_F11:
            
            self.KeyboardHandles.KeyF11Handler()
            
        elif key == qc.Qt.Key_F12:
        
            self.KeyboardHandles.KeyF12Handler()
            
        elif key == qc.Qt.Key_End:
            
            self.KeyboardHandles.KeyEndHandler()
            
        elif key == qc.Qt.Key_Delete:
        
            self.KeyboardHandles.KeyDeleteHandler()
            
        elif key == qc.Qt.Key_Tab:
            
            self.KeyboardHandles.KeyTabHandler()
            
        elif key == qc.Qt.Key_Shift:
            
            self.KeyboardHandles.KeyShiftHandler()
            
        elif key == qc.Qt.Key_CapsLock:
            
            self.KeyboardHandles.KeyCapsLockHandler()
            
        #ai generated
        elif key == qc.Qt.Key_Slash:
            
            self.KeyboardHandles.KeypadSlashHandler()
            
        elif key == qc.Qt.Key_Asterisk:
            
            self.KeyboardHandles.KeypadAsteriskHandler()
            
        elif key == qc.Qt.Key_Minus:
            
            self.KeyboardHandles.KeypadMinusHandler()
            
        elif key == qc.Qt.Key_Plus:
            
            self.KeyboardHandles.KeypadPlusHandler()
            
        elif key == qc.Qt.Key_Enter:
            
            self.KeyboardHandles.KeypadEnterHandler()
            
        elif key == qc.Qt.Key_Period:
            
            self.KeyboardHandles.KeypadPeriodHandler()
            
# =============================================================================
#         elif key == qc.Qt.Keypad_0:
#             
#             self.KeyboardHandles.Keypad0Handler()
#             
#         elif key == qc.Qt.Keypad_1:
#             
#             self.KeyboardHandles.Keypad1Handler()
#             
#         elif key == qc.Qt.Keypad_2:
#             
#             self.KeyboardHandles.Keypad2Handler()
#             
#         elif key == qc.Qt.Keypad_3:
#             
#             self.KeyboardHandles.Keypad3Handler()
#             
#         elif key == qc.Qt.Keypad_4:
#             
#             self.KeyboardHandles.Keypad4Handler()
#             
#         elif key == qc.Qt.Keypad_5:
#             
#             self.KeyboardHandles.Keypad5Handler()
#             
#         elif key == qc.Qt.Keypad_6:
#         
#             self.KeyboardHandles.Keypad6Handler()
#             
#         elif key == qc.Qt.Keypad_7:
#             
#             self.KeyboardHandles.Keypad7Handler()
#             
#         elif key == qc.Qt.Keypad_8:
#         
#             self.KeyboardHandles.Keypad8Handler()
#             
#         elif key == qc.Qt.Keypad_9:
#             
#             self.KeyboardHandles.Keypad9Handler()
#             
# =============================================================================
            
        elif key == qc.Qt.Key_ParenLeft:
            
            self.KeyboardHandles.KeypadParenLeftHandler()
            
        elif key == qc.Qt.Key_ParenRight:
        
            self.KeyboardHandles.KeypadParenRightHandler()
            
        elif key == qc.Qt.Key_BracketLeft:
            
            self.KeyboardHandles.KeypadBracketLeftHandler()
            
        elif key == qc.Qt.Key_BracketRight:
        
            self.KeyboardHandles.KeypadBracketRightHandler()
            
        elif key == qc.Qt.Key_BraceLeft:
            
            self.KeyboardHandles.KeypadBraceLeftHandler()
            
        elif key == qc.Qt.Key_BraceRight:
        
            self.KeyboardHandles.KeypadBraceRightHandler()
            
        elif key == qc.Qt.Key_Bar:
            
            self.KeyboardHandles.KeypadBarHandler()
            
        elif key == qc.Qt.Key_Backslash:
        
            self.KeyboardHandles.KeypadBackslashHandler()
            
        elif key == qc.Qt.Key_Colon:
            
            self.KeyboardHandles.KeypadColonHandler()
            
        elif key == qc.Qt.Key_QuoteDbl:
        
            self.KeyboardHandles.KeypadQuoteDblHandler()
            
        elif key == qc.Qt.Key_Apostrophe:
            
            self.KeyboardHandles.KeypadApostropheHandler()
            
        elif key == qc.Qt.Key_Less:
        
            self.KeyboardHandles.KeypadLessHandler()
            
        elif key == qc.Qt.Key_Greater:
            
            self.KeyboardHandles.KeypadGreaterHandler()
            
        elif key == qc.Qt.Key_Question:
        
            self.KeyboardHandles.KeypadQuestionHandler()
            
        elif key == qc.Qt.Key_Exclam:
            
            self.KeyboardHandles.KeypadExclamHandler()
            
        elif key == qc.Qt.Key_At:
        
            self.KeyboardHandles.KeypadAtHandler()
            
        elif key == qc.Qt.Key_NumberSign:
            
            self.KeyboardHandles.KeypadNumberSignHandler()
            
        elif key == qc.Qt.Key_Dollar:
        
            self.KeyboardHandles.KeypadDollarHandler()
            
        elif key == qc.Qt.Key_Percent:
            
            self.KeyboardHandles.KeypadPercentHandler()
            
        elif key == qc.Qt.Key_AsciiCircum:
        
            self.KeyboardHandles.KeypadAsciiCircumHandler()
            
        elif key == qc.Qt.Key_Ampersand:
            
            self.KeyboardHandles.KeypadAmpersandHandler()
            
        elif key == qc.Qt.Key_Apostrophe:
        
            self.KeyboardHandles.KeypadApostropheHandler()
            
        elif key == qc.Qt.Key_AsciiTilde:
            
            self.KeyboardHandles.KeypadAsciiTildeHandler()
            
        elif key == qc.Qt.Key_notsign:
        
            self.KeyboardHandles.KeypadNotHandler()
            
        elif key == qc.Qt.Key_Bar:
            
            self.KeyboardHandles.KeypadBarHandler()
            
        elif key == qc.Qt.Key_Control:
            
            self.controlOn = 1
            print("control is on")
# =============================================================================
#         elif key == qc.Qt.Key_EuroSign:
#         
#             self.KeyboardHandles.KeypadEuroSignHandler()
#             
#         elif key == qc.Qt.Key_PoundSign:
#             
#             self.KeyboardHandles.KeypadPoundSignHandler()
#             
#         elif key == qc.Qt.Key_YenSign:
#         
#             self.KeyboardHandles.KeypadYenSignHandler()
#             
#         elif key == qc.Qt.Key_Para:
#             
#             self.KeyboardHandles.KeypadParaHandler()
#             
#         elif key == qc.Qt.Key_SectionSign:
#         
#             self.KeyboardHandles.KeypadSectionSignHandler()
#             
#         elif key == qc.Qt.Key_CentSign:
#             
#             self.KeyboardHandles.KeypadCentSignHandler()
#             
#         elif key == qc.Qt.Key_DegreeSign:
#         
#             self.KeyboardHandles.KeypadDegreeSignHandler()
#             
#         elif key == qc.Qt.Key_PlusMinusSign:
#             
#             self.KeyboardHandles.KeypadPlusMinusSignHandler()
#             
#         elif key == qc.Qt.Key_MicroSign:
#         
#             self.KeyboardHandles.KeypadMicroSignHandler()
#             
#         elif key == qc.Qt.Key_RootSign:
#             
#             self.KeyboardHandles.KeypadRootSignHandler()
#             
#         elif key == qc.Qt.Key_ApproxSign:
#         
#             self.KeyboardHandles.KeypadApproxSignHandler()
#             
#         elif key == qc.Qt.Key_AcuteAccent:
#             
#             self.KeyboardHandles.KeypadAcuteAccentHandler()
#             
#         elif key == qc.Qt.Key_AsciiTilde:
#         
#             self.KeyboardHandles.KeypadAsciiTildeHandler()
#             
#         elif key == qc.Qt.Key_Diaeresis:
#             
#             self.KeyboardHandles.KeypadDiaeresisHandler()
#             
#         elif key == qc.Qt.Key_CircumflexAccent:
#         
#             self.KeyboardHandles.KeypadCircumflexAccentHandler()
#             
#         elif key == qc.Qt.Key_GraveAccent:
#             
#             self.KeyboardHandles.KeypadGraveAccentHandler()
#             
#         elif key == qc.Qt.Key_Apostrophe:
#         
#             self.KeyboardHandles.KeypadApostropheHandler()
#             
#         elif key == qc.Qt.Key_AsciiCircum:
#             
#             self.KeyboardHandles.KeypadAsciiCircumHandler()
#             
#         elif key == qc.Qt.Key_Cedilla:
#         
#             self.KeyboardHandles.KeypadCedillaHandler()
#             
#         elif key == qc.Qt.Key_Hook:
#             
#             self.KeyboardHandles.KeypadHookHandler()
# =============================================================================
            
        else:
            print("no handler for that key")
            
    def controlPressedHandlers(self, key):
           if key == qc.Qt.Key_Space:
               
               self.KeyboardHandles.controlKeySpaceHandler()
               
           elif key == qc.Qt.Key_Left:
               
               self.KeyboardHandles.controlKeyLeftHandler()
               
           elif key == qc.Qt.Key_Up:
               
               self.KeyboardHandles.controlKeyUpHandler()
           
           elif key == qc.Qt.Key_Right:
           
               self.KeyboardHandles.controlKeyRightHandler()
               
           elif key == qc.Qt.Key_Down:
           
               self.KeyboardHandles.controlKeyDownHandler()
               
           elif key == qc.Qt.Key_A:
           
               self.KeyboardHandles.controlKeyAHandler()
               
           elif key == qc.Qt.Key_B:
           
               self.KeyboardHandles.controlKeyBHandler()
               
           elif key == qc.Qt.Key_C:
           
               self.KeyboardHandles.controlKeyCHandler()
               
           elif key == qc.Qt.Key_D:
           
               self.KeyboardHandles.controlKeyDHandler()
               
           elif key == qc.Qt.Key_E:
           
               self.KeyboardHandles.controlKeyEHandler()
               
           elif key == qc.Qt.Key_F:
           
               self.KeyboardHandles.controlKeyFHandler()
               
           elif key == qc.Qt.Key_G:
           
               self.KeyboardHandles.controlKeyGHandler()
               
           elif key == qc.Qt.Key_H:
           
               self.KeyboardHandles.controlKeyHHandler()
               
           elif key == qc.Qt.Key_I:
           
               self.KeyboardHandles.controlKeyIHandler()
               
           elif key == qc.Qt.Key_J:
           
               self.KeyboardHandles.controlKeyJHandler()
               
           elif key == qc.Qt.Key_K:
           
               self.KeyboardHandles.controlKeyKHandler()
               
           elif key == qc.Qt.Key_L:
           
               self.KeyboardHandles.controlKeyLHandler()
               
           elif key == qc.Qt.Key_M:
           
               self.KeyboardHandles.controlKeyMHandler()
               
           elif key == qc.Qt.Key_N:
           
               self.KeyboardHandles.controlKeyNHandler()
               
           elif key == qc.Qt.Key_O:
           
               self.KeyboardHandles.controlKeyOHandler()
               
           elif key == qc.Qt.Key_P:
           
               self.KeyboardHandles.controlKeyPHandler()
               
           elif key == qc.Qt.Key_Q:
           
               self.KeyboardHandles.controlKeyQHandler()
               
           elif key == qc.Qt.Key_R:
           
               self.KeyboardHandles.controlKeyRHandler()
               
           elif key == qc.Qt.Key_S:
           
               self.KeyboardHandles.controlKeySHandler()
               
           elif key == qc.Qt.Key_T:
           
               self.KeyboardHandles.controlKeyTHandler()
               
           elif key == qc.Qt.Key_U:
           
               self.KeyboardHandles.controlKeyUHandler()
               
           elif key == qc.Qt.Key_V:
           
               self.KeyboardHandles.controlKeyVHandler()
               
           elif key == qc.Qt.Key_W:
           
               self.KeyboardHandles.controlKeyWHandler()
               
           elif key == qc.Qt.Key_X:
           
               self.KeyboardHandles.controlKeyXHandler()
               
           elif key == qc.Qt.Key_Y:
           
               self.KeyboardHandles.controlKeyYHandler()
               
           elif key == qc.Qt.Key_Z:
           
               self.KeyboardHandles.controlKeyZHandler()
               
           elif key == qc.Qt.Key_Backspace:
           
               self.KeyboardHandles.controlKeyBackSpaceHandler()
               
           elif key == qc.Qt.Key_Enter:
           
               self.KeyboardHandles.controlKeyEnterHandler()
               
           elif key == qc.Qt.Key_Return:
           
               self.KeyboardHandles.controlKeyReturnHandler()
               
           elif key == qc.Qt.Key_0:
               
               self.KeyboardHandles.controlKey0Handler()
           
           elif key == qc.Qt.Key_1:
               
               self.KeyboardHandles.controlKey1Handler()
               
           elif key == qc.Qt.Key_2:
               
               self.KeyboardHandles.controlKey2Handler()
               
           elif key == qc.Qt.Key_3:
               
               self.KeyboardHandles.controlKey3Handler()
               
           elif key == qc.Qt.Key_4:
               
               self.KeyboardHandles.controlKey4Handler()
               
           elif key == qc.Qt.Key_5:
               
               self.KeyboardHandles.controlKey5Handler()
               
           elif key == qc.Qt.Key_6:
               
               self.KeyboardHandles.controlKey6Handler()
               
           elif key == qc.Qt.Key_7:
               
               self.KeyboardHandles.controlKey7Handler()
               
           elif key == qc.Qt.Key_8:
               
               self.KeyboardHandles.controlKey8Handler()
               
           elif key == qc.Qt.Key_9:
               
               self.KeyboardHandles.controlKey9Handler()
               
           elif key == qc.Qt.Key_ParenLeft:
               
               self.KeyboardHandles.controlKeyParenLeftHandler()
               
           elif key == qc.Qt.Key_ParenRight:
               
               self.KeyboardHandles.controlKeyParenRightHandler()
               
           elif key == qc.Qt.Key_Comma:
               
               self.KeyboardHandles.controlKeyCommaHandler()
           
           elif key == qc.Qt.Key_Plus:
               
               self.KeyboardHandles.controlKeyPlusHandler()
               
           elif key == qc.Qt.Key_Minus:
               
               self.KeyboardHandles.controlKeyMinusHandler()
               
           elif key == qc.Qt.Key_Asterisk:
               
               self.KeyboardHandles.controlKeyAsteriskHandler()
               
           elif key == qc.Qt.Key_Period:
               
               self.KeyboardHandles.controlKeyPeriodHandler()
               
           elif key == qc.Qt.Key_Slash:
               
               self.KeyboardHandles.controlKeySlashHandler()
               
           elif key == qc.Qt.Key_Colon:
               
               self.KeyboardHandles.controlKeyColonHandler()
               
           elif key == qc.Qt.Key_Semicolon:
               
               self.KeyboardHandles.controlKeySemicolonHandler()
               
           elif key == qc.Qt.Key_BracketLeft:
               
               self.KeyboardHandles.BracketLeftHandler()
               
           elif key == qc.Qt.Key_BracketRight:
               
               self.KeyboardHandles.BracketRightHandler()
               
           elif key == qc.Qt.Key_Equal:
               
               self.KeyboardHandles.EqualHandler()
               
           elif key == qc.Qt.Key_Greater:
               
               self.KeyboardHandles.GreaterHandler()
               
           elif key == qc.Qt.Key_Less:
               
               self.KeyboardHandles.LessHandler()
               
           elif key == qc.Qt.Key_QuoteLeft:
               
               self.KeyboardHandles.QuoteLeftHandler()
               
           elif key == qc.Qt.Key_QuoteDbl:
               
               self.KeyboardHandles.QuoteDblHandler()
               
           elif key == qc.Qt.Key_PageUp:
               
               self.KeyboardHandles.controlKeyPageUpHandler()
               
           elif key == qc.Qt.Key_PageDown:
               
               self.KeyboardHandles.controlKeyPageDownHandler()
               
           elif key == qc.Qt.Key_F1:
               
               self.KeyboardHandles.controlKeyF1Handler()
               
           elif key == qc.Qt.Key_F2:
               
               self.KeyboardHandles.controlKeyF2Handler()
               
           elif key == qc.Qt.Key_F3:
           
               self.KeyboardHandles.controlKeyF3Handler()
               
           elif key == qc.Qt.Key_F4:
           
               self.KeyboardHandles.controlKeyF4Handler()
               
           elif key == qc.Qt.Key_F5:
               
               self.KeyboardHandles.controlKeyF5Handler()
               
           elif key == qc.Qt.Key_F6:
           
               self.KeyboardHandles.controlKeyF6Handler()
               
           elif key == qc.Qt.Key_F7:
               
               self.KeyboardHandles.controlKeyF7Handler()
               
           elif key == qc.Qt.Key_F8:
               
               self.KeyboardHandles.controlKeyF8Handler()
               
           elif key == qc.Qt.Key_F9:
           
               self.KeyboardHandles.controlKeyF9Handler()
               
           elif key == qc.Qt.Key_F10:
               
               self.KeyboardHandles.controlKeyF10Handler()
               
           elif key == qc.Qt.Key_F11:
               
               self.KeyboardHandles.controlKeyF11Handler()
               
           elif key == qc.Qt.Key_F12:
           
               self.KeyboardHandles.controlKeyF12Handler()
               
           elif key == qc.Qt.Key_End:
               
               self.KeyboardHandles.controlKeyEndHandler()
               
           elif key == qc.Qt.Key_Delete:
           
               self.KeyboardHandles.controlKeyDeleteHandler()
               
           elif key == qc.Qt.Key_Tab:
               
               self.KeyboardHandles.controlKeyTabHandler()
               
           elif key == qc.Qt.Key_Shift:
               
               self.KeyboardHandles.controlKeyShiftHandler()
               
           elif key == qc.Qt.Key_CapsLock:
               
               self.KeyboardHandles.controlKeyCapsLockHandler()
               
           #ai generated
           elif key == qc.Qt.Key_Slash:
               
               self.KeyboardHandles.controlKeypadSlashHandler()
               
           elif key == qc.Qt.Key_Asterisk:
               
               self.KeyboardHandles.controlKeypadAsteriskHandler()
               
           elif key == qc.Qt.Key_Minus:
               
               self.KeyboardHandles.controlKeypadMinusHandler()
               
           elif key == qc.Qt.Key_Plus:
               
               self.KeyboardHandles.controlKeypadPlusHandler()
               
           elif key == qc.Qt.Key_Enter:
               
               self.KeyboardHandles.controlKeypadEnterHandler()
               
           elif key == qc.Qt.Key_Period:
               
               self.KeyboardHandles.controlKeypadPeriodHandler()
               
   # =============================================================================
   #         elif key == qc.Qt.Keypad_0:
   #             
   #             self.KeyboardHandles.controlKeypad0Handler()
   #             
   #         elif key == qc.Qt.Keypad_1:
   #             
   #             self.KeyboardHandles.controlKeypad1Handler()
   #             
   #         elif key == qc.Qt.Keypad_2:
   #             
   #             self.KeyboardHandles.controlKeypad2Handler()
   #             
   #         elif key == qc.Qt.Keypad_3:
   #             
   #             self.KeyboardHandles.controlKeypad3Handler()
   #             
   #         elif key == qc.Qt.Keypad_4:
   #             
   #             self.KeyboardHandles.controlKeypad4Handler()
   #             
   #         elif key == qc.Qt.Keypad_5:
   #             
   #             self.KeyboardHandles.controlKeypad5Handler()
   #             
   #         elif key == qc.Qt.Keypad_6:
   #         
   #             self.KeyboardHandles.controlKeypad6Handler()
   #             
   #         elif key == qc.Qt.Keypad_7:
   #             
   #             self.KeyboardHandles.controlKeypad7Handler()
   #             
   #         elif key == qc.Qt.Keypad_8:
   #         
   #             self.KeyboardHandles.controlKeypad8Handler()
   #             
   #         elif key == qc.Qt.Keypad_9:
   #             
   #             self.KeyboardHandles.controlKeypad9Handler()
   #             
   # =============================================================================
               
           elif key == qc.Qt.Key_ParenLeft:
               
               self.KeyboardHandles.controlKeypadParenLeftHandler()
               
           elif key == qc.Qt.Key_ParenRight:
           
               self.KeyboardHandles.controlKeypadParenRightHandler()
               
           elif key == qc.Qt.Key_BracketLeft:
               
               self.KeyboardHandles.controlKeypadBracketLeftHandler()
               
           elif key == qc.Qt.Key_BracketRight:
           
               self.KeyboardHandles.controlKeypadBracketRightHandler()
               
           elif key == qc.Qt.Key_BraceLeft:
               
               self.KeyboardHandles.controlKeypadBraceLeftHandler()
               
           elif key == qc.Qt.Key_BraceRight:
           
               self.KeyboardHandles.controlKeypadBraceRightHandler()
               
           elif key == qc.Qt.Key_Bar:
               
               self.KeyboardHandles.controlKeypadBarHandler()
               
           elif key == qc.Qt.Key_Backslash:
           
               self.KeyboardHandles.controlKeypadBackslashHandler()
               
           elif key == qc.Qt.Key_Colon:
               
               self.KeyboardHandles.controlKeypadColonHandler()
               
           elif key == qc.Qt.Key_QuoteDbl:
           
               self.KeyboardHandles.controlKeypadQuoteDblHandler()
               
           elif key == qc.Qt.Key_Apostrophe:
               
               self.KeyboardHandles.controlKeypadApostropheHandler()
               
           elif key == qc.Qt.Key_Less:
           
               self.KeyboardHandles.controlKeypadLessHandler()
               
           elif key == qc.Qt.Key_Greater:
               
               self.KeyboardHandles.controlKeypadGreaterHandler()
               
           elif key == qc.Qt.Key_Question:
           
               self.KeyboardHandles.controlKeypadQuestionHandler()
               
           elif key == qc.Qt.Key_Exclam:
               
               self.KeyboardHandles.controlKeypadExclamHandler()
               
           elif key == qc.Qt.Key_At:
           
               self.KeyboardHandles.controlKeypadAtHandler()
               
           elif key == qc.Qt.Key_NumberSign:
               
               self.KeyboardHandles.controlKeypadNumberSignHandler()
               
           elif key == qc.Qt.Key_Dollar:
           
               self.KeyboardHandles.controlKeypadDollarHandler()
               
           elif key == qc.Qt.Key_Percent:
               
               self.KeyboardHandles.controlKeypadPercentHandler()
               
           elif key == qc.Qt.Key_AsciiCircum:
           
               self.KeyboardHandles.controlKeypadAsciiCircumHandler()
               
           elif key == qc.Qt.Key_Ampersand:
               
               self.KeyboardHandles.controlKeypadAmpersandHandler()
               
           elif key == qc.Qt.Key_Apostrophe:
           
               self.KeyboardHandles.controlKeypadApostropheHandler()
               
           elif key == qc.Qt.Key_AsciiTilde:
               
               self.KeyboardHandles.controlKeypadAsciiTildeHandler()
               
           elif key == qc.Qt.Key_notsign:
           
               self.KeyboardHandles.controlKeypadNotHandler()
               
           elif key == qc.Qt.Key_Bar:
               
               self.KeyboardHandles.controlKeypadBarHandler()
               
           elif key == qc.Qt.Key_Control:
               
               self.controlOn = 1
               print("control is on")
   # =============================================================================
   #         elif key == qc.Qt.Key_EuroSign:
   #         
   #             self.KeyboardHandles.controlKeypadEuroSignHandler()
   #             
   #         elif key == qc.Qt.Key_PoundSign:
   #             
   #             self.KeyboardHandles.controlKeypadPoundSignHandler()
   #             
   #         elif key == qc.Qt.Key_YenSign:
   #         
   #             self.KeyboardHandles.controlKeypadYenSignHandler()
   #             
   #         elif key == qc.Qt.Key_Para:
   #             
   #             self.KeyboardHandles.controlKeypadParaHandler()
   #             
   #         elif key == qc.Qt.Key_SectionSign:
   #         
   #             self.KeyboardHandles.controlKeypadSectionSignHandler()
   #             
   #         elif key == qc.Qt.Key_CentSign:
   #             
   #             self.KeyboardHandles.controlKeypadCentSignHandler()
   #             
   #         elif key == qc.Qt.Key_DegreeSign:
   #         
   #             self.KeyboardHandles.controlKeypadDegreeSignHandler()
   #             
   #         elif key == qc.Qt.Key_PlusMinusSign:
   #             
   #             self.KeyboardHandles.controlKeypadPlusMinusSignHandler()
   #             
   #         elif key == qc.Qt.Key_MicroSign:
   #         
   #             self.KeyboardHandles.controlKeypadMicroSignHandler()
   #             
   #         elif key == qc.Qt.Key_RootSign:
   #             
   #             self.KeyboardHandles.controlKeypadRootSignHandler()
   #             
   #         elif key == qc.Qt.Key_ApproxSign:
   #         
   #             self.KeyboardHandles.controlKeypadApproxSignHandler()
   #             
   #         elif key == qc.Qt.Key_AcuteAccent:
   #             
   #             self.KeyboardHandles.controlKeypadAcuteAccentHandler()
   #             
   #         elif key == qc.Qt.Key_AsciiTilde:
   #         
   #             self.KeyboardHandles.controlKeypadAsciiTildeHandler()
   #             
   #         elif key == qc.Qt.Key_Diaeresis:
   #             
   #             self.KeyboardHandles.controlKeypadDiaeresisHandler()
   #             
   #         elif key == qc.Qt.Key_CircumflexAccent:
   #         
   #             self.KeyboardHandles.controlKeypadCircumflexAccentHandler()
   #             
   #         elif key == qc.Qt.Key_GraveAccent:
   #             
   #             self.KeyboardHandles.controlKeypadGraveAccentHandler()
   #             
   #         elif key == qc.Qt.Key_Apostrophe:
   #         
   #             self.KeyboardHandles.controlKeypadApostropheHandler()
   #             
   #         elif key == qc.Qt.Key_AsciiCircum:
   #             
   #             self.KeyboardHandles.controlKeypadAsciiCircumHandler()
   #             
   #         elif key == qc.Qt.Key_Cedilla:
   #         
   #             self.KeyboardHandles.controlKeypadCedillaHandler()
   #             
   #         elif key == qc.Qt.Key_Hook:
   #             
   #             self.KeyboardHandles.controlKeypadHookHandler()
   # =============================================================================
               
           else:
               print("no handler for that key")
    
        
        
    def handleKeyReleaseEvent(self, keyReleaseEvent):
        
        
        key = keyReleaseEvent.key()
      
        if key == qc.Qt.Key_Control:
            
            self.controlOn = 0
            print("control is off")
        
        
    