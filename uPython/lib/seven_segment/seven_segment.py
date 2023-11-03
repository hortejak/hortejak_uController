from machine import Pin
import time

class SevenSegment():
    
    def __init__(self,a=21,b=20,c=13,d=11,e=10,f=19,g=14,dp=12,d1=27,d2=26,d3=22,d4=15):
        
        self.segments = []
        for seg in [a,b,c,d,e,f,g]:
            self.segments.append(Pin(seg,Pin.OUT))
            
        self.digits = [] 
        for digit in [d1,d2,d3,d4]:
            self.digits.append(Pin(digit,Pin.OUT))
            
        self.dot = Pin(dp,Pin.OUT)
        
        self.numbers = [
                [0,0,0,0,0,0,1],	# 0
                [1,0,0,1,1,1,1],	# 1
                [0,0,1,0,0,1,0],	# 2
                [0,0,0,0,1,1,0],	# 3
                [1,0,0,1,1,0,0],	# 4
                [0,1,0,0,1,0,0],	# 5
                [0,1,0,0,0,0,0],	# 6
                [0,0,0,1,1,1,1],	# 7
                [0,0,0,0,0,0,0],	# 8
                [0,0,0,0,1,0,0],	# 9
            ]
        
    def reset(self):
        
        for digit in range(4):
            self.digits[digit].value(1)
            self.dot.value(1)
            for segment in range(7):
                self.segments[segment].value(1)
            self.digits[digit].value(0)
                
        
    def display(self,number,timeout=5,sleep=0.0005):
        
        period = False
        
        if isinstance(number,int):
            number = str(number)
        elif isinstance(number,float):
            number = str(number)
            dot_index = number.index(".")
            number = number.replace(".","")
            period = True
            
        digits = len(number)
        
        #self.reset()
        
        iterations = timeout//(8*sleep)
        print(iterations)
        
        while iterations > 0:
        
            for i in range(digits):
                self.digits[i].value(1)
                for a in range(7):
                    self.segments[a].value(self.numbers[int(number[i])][a])
                    
                time.sleep(sleep)
                self.digits[i].value(0)
                
            iterations -= 1
            
        


if __name__ == "__main__":
    display = SevenSegment()
    display.display(375)