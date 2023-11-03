# 503PTC2E-1AD Phototansistor

from machine import Pin, ADC
import time

class Phototransistor():

    def __init__(self,pin=26):
        self.pin = Pin(26,mode=Pin.IN)
        self.adc = ADC(self.pin)
        
    def get_value(self):
        raw = self.adc.read_u16()
        
        return raw*3.3/65535
    
if __name__=="__main__":
    
    p = Pin(16,Pin.OUT)
    p.value(1)
    
    f = Phototransistor(26)
    
    while True:
        print(f.get_value())
        time.sleep(1)
        