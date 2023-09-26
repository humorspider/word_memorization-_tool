import win32gui as w
import time 
for i in range(10):
    title = w.GetWindowText (w.GetForegroundWindow())
    
    print(title)
    time.sleep(1)