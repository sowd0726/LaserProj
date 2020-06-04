import time
import hid
import threading


class USBIO:
    VENDOR_ID = 0x1352       # Km2Net
    PRODUCT_ID = 0x0121  # USB-IO2.0(AKI)
    lock = threading.Lock()
# Command list
    CMD_READ_WRITE = 0x20
    CMD_CONFIG_READ = 0xf8
    CMD_CONFIG_WRITE = 0xf9
    usb = hid.device(VENDOR_ID, PRODUCT_ID)
    def __init__(self  ):
        #writePin( 0,0 )
        self.pin = [0] *12

    def writePin(self,p1,p2):   # Prioro to use this , all pins need to be configured as output pins
        data = [int(0)] * 64
        data[0] = self.CMD_READ_WRITE
        data[1] = 1
        data[2] = p1
        data[3] = 2
        data[4] = p2
        data[63] =89    # dummy to confirm USB-IO recognition
        self.lock.acquire() # make sure just a thread using USB
        self.usb.write(data)
        self.lock.release()
        return(self.usb.read(64))

        
    def setPinLevel(self, pin_no , level ):
        self.pin[pin_no] = level

    def outputToPin( self ):
        p1 =      self.pin[0]    + self.pin[1] * 2 + self.pin[2] * 4 + self.pin[3] *8
        p1 = p1 + self.pin[4]*16 + self.pin[5] * 32+ self.pin[6] * 64+ self.pin[7] *128
        p2 =      self.pin[8]    + self.pin[9] * 2 + self.pin[10]* 4 + self.pin[11]*8
        self.writePin( p1 , p2 )


UsbIO=USBIO(  )   # To use USBIO as a kind of singleton

class C28BYJ48():
    def __init__(self, IN1, IN2, IN3, IN4):
        self.mPin = [IN1, IN2, IN3, IN4]     # USBIO pin number 4 of 0-12
        self.stepThread=None

        #Setting related Sequence
        #1step angle = 1/4096[deg]
        self.nPos = 0
        self.mSeq = [[1,0,0,1],[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1]]
        #default speed = max speed
        self.SetWaitTime(0.001)

    def SetPinsVoltage(self, nSeq):
        for pin in range(0, 4):
            if self.mSeq[nSeq][pin]!=0:
                UsbIO.setPinLevel( self.mPin[pin] , 1 )
            else:
                UsbIO.setPinLevel( self.mPin[pin] , 0 )

    def SetWaitTime(self, wait):
        self.mStep_wait = wait

    def Step(self, step, wait):
        self.SetWaitTime(wait)
        for i in range(0, abs(step) ):
            if( step > 0 ):
                self.nPos += 1
            else :
                self.nPos -= 1
            self.SetPinsVoltage(self.nPos % 8)
            UsbIO.outputToPin()
            time.sleep(self.mStep_wait)

# Entry point to control the stepping motor.

    def ThreadStep( self , step , wait ):
        if self.stepThread!=None:
# When motor is moving , it wait the end of moving before creating thread.
            self.stepThread.join()

        self.stepThread = threading.Thread( target=self.Step, args=(step,wait ) )
        self.stepThread.start()



    def Cleanup(self):
        if self.stepThread!=None:
# When motor is moving , it wait the end of moving before creating thread.
            self.stepThread.join()
        for pin in range(0, 4):
            UsbIO.setPinLevel( self.mPin[pin] , 0 )
        UsbIO.outputToPin()


if __name__ == '__main__':
    StepMoterX = C28BYJ48(IN1=0 ,IN2=1, IN3=2, IN4=3)
    StepMoterX.ThreadStep(-300,0.001)
    Sleep(5)
    StepMoterX.Cleanup()
