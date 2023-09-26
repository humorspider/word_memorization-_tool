import keyboard
import threading
import time
def on_press():
    keyboard.press_and_release('x')
    time.sleep(10)
    keyboard.press_and_release('x')
    print('x')
print("Listening for keyboard events...")


new_thread = threading.Thread(target=on_press)
# 启动新线程
new_thread.start()
keyboard.wait('x')  # 阻塞等待按下"esc"键xx

print("Program continues...")