import time
from machine import Pin, PWM

class LED():
    
    def __init__(self,pin=16):
        self.led = Pin(pin,Pin.OUT)
        
    def on(self):
        self.led.value(1)
        
    def off(self):
        self.led.value(0)
        

class RGB_LED():
    def __init__(self,R=18,G=19,B=20):

        self.R = PWM(Pin(R))
        self.G = PWM(Pin(G))
        self.B = PWM(Pin(B))
        
        self.R.freq(5000)
        self.G.freq(5000)
        self.B.freq(5000)
        
    def set_color(self,color):
        
        r,g,b = color
        
        self.off()
        self.R.duty_u16(r*257)
        self.G.duty_u16(g*257)
        self.B.duty_u16(b*257)
        
    def set_red(self,intensity=255):
        
        self.off()
        self.R.duty_u16(intensity*257)
        
    def set_green(self,intensity=255):
        
        self.off()
        self.G.duty_u16(intensity*257)
        
    def set_blue(self,intensity=255):
        
        self.off()
        self.B.duty_u16(intensity*257)
        
    def off(self):
        self.R.deinit()
        self.G.deinit()
        self.B.deinit()
        
if __name__=="__main__":
    
    l = RGB_LED()
    
    RGB.set_color((10,10,10))