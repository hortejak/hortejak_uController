# class module managing the temperature sensor SHT40

from machine import I2C, Pin
import time

DEFAULT_I2C_ADDRESS = 0x44

class Mode():
    
    def __init__(self):
        
        self.add_values(
            (
                ("NOHEAT_HIGHPRECISION", 0xFD, "No heater, high precision", 0.01),
                ("NOHEAT_MEDPRECISION", 0xF6, "No heater, med precision", 0.005),
                ("NOHEAT_LOWPRECISION", 0xE0, "No heater, low precision", 0.002),
                ("HIGHHEAT_1S", 0x39, "High heat, 1 second", 1.1),
                ("HIGHHEAT_100MS", 0x32, "High heat, 0.1 second", 0.11),
                ("MEDHEAT_1S", 0x2F, "Med heat, 1 second", 1.1),
                ("MEDHEAT_100MS", 0x24, "Med heat, 0.1 second", 0.11),
                ("LOWHEAT_1S", 0x1E, "Low heat, 1 second", 1.1),
                ("LOWHEAT_100MS", 0x15, "Low heat, 0.1 second", 0.11),
            )
        )
    
    def add_values(self,values):
        
        self.strings = {}
        self.delays = {}
        
        for value in values:
            name,val,string,delay = value
            byte_val = val.to_bytes(1,'big')
            setattr(self,name,byte_val)
            self.strings[byte_val] = string
            self.delays[byte_val] = delay

class SHT40():
    
    POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001
    
    def __init__(self,scl=1,sda=0):
        
        self.i2c = I2C(id=0,scl=Pin(scl), sda=Pin(sda))
        self.i2c_addr = DEFAULT_I2C_ADDRESS
        mode = Mode()
        self.mode = mode.NOHEAT_HIGHPRECISION
        self.wait = 1.1*mode.delays[self.mode]
        self.reset()
        
    def reset(self):
        command = 0x94
        self.i2c.writeto(self.i2c_addr,command.to_bytes(1,'big'))
        time.sleep_ms(50)
        
    def measure(self):
        self.i2c.writeto(self.i2c_addr,self.mode)
        time.sleep(self.wait)
        data = self.i2c.readfrom(self.i2c_addr,6)
        
        t_crc = data[2]
        h_crc = data[5]
        
        if (data[2] == self.crc(data[0:2]) and data[5] == self.crc(data[3:5])):
        
            t = int.from_bytes(data[0:2],'big')
            h = int.from_bytes(data[3:5],'big')
            temperature = -45.0 + 175.0 * t / 65535.0
            humidity = -6.0 + 125.0 * h / 65535.0
            humidity = max(min(humidity, 100), 0)
            
            return [temperature, humidity]
        
        print("Invalid CRC")
        return [None,None]

    
    def crc(self,buffer):
        """verify the crc8 checksum"""
        crc = 0xFF
        for byte in buffer:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1
        return crc & 0xFF  # return the bottom 8 bits
        
if __name__ == "__main__":
    sensor = SHT40()
    print(sensor.measure())
        