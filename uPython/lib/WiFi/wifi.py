import network
import time
import ntptime
import json
import machine

class Network():
    def __init__(self,config='config.json'):
        
        f = open(config)
        self.config = json.load(f)
        f.close()
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        wlan.connect(self.config['WIFI_SSID'],self.config['WIFI_PASSWORD'])
        self.rtc = machine.RTC()
        self.set_time()
        
    def set_time(self,display=True):
        
        ntptime.settime()
        
        timezone_adjustment = 1		# TODO: add summertime
        tm = time.localtime()		#(year, month, monthday, hour, minute, second, weekday, yearday)
        tm = time.localtime(time.mktime(tm) + 3600*timezone_adjustment)
        self.rtc.datetime((tm[0],tm[1],tm[2],tm[6],tm[3],tm[4],tm[5],0))		# (year, month, day, weekday, hours, minutes, seconds, subseconds)
        if display:           
            print(self.rtc.datetime())
            
        return self.rtc.datetime()
