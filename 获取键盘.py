import keyboard  #监听键盘

def test_a():
    print('aaa')

def check_keyboard(event):
    print(event.scan_code)
    print(event.name)
if __name__ == '__main__':
    keyboard.on_press(check_keyboard)
    keyboard.wait('x')
    #wait里也可以设置按键，说明当按到该键时结束
