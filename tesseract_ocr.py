import pytesseract
import win32gui
from PIL import ImageGrab
import time
def get_word():
    window_title = "雷电模拟器"  # 要截取的窗口标题
    hwnd = win32gui.FindWindow(None, window_title)  # 根据窗口标题查找窗口句柄

    rect = win32gui.GetWindowRect(hwnd)  # 获取窗口的坐标
    x, y, w, h = rect
    actual_x = int(x*1.5)
    actual_y = int(y*1.5)
    actual_w = int(w*1.5)
    actual_h = int(h*1.5)
    screenshot = ImageGrab.grab(bbox=(actual_x+50, actual_y+70, actual_x +500, actual_y + 140))  # 进行截图
    # 使用Tesseract进行OCR识别
    result = pytesseract.image_to_string(screenshot)
    result = result.replace('\n','').strip()
    # 打印识别结果
    return result


if __name__ == '__main__':
    word = ''
    while True:
        time.sleep(1)    
        if word != get_word(): 
            word = get_word()
            print(word)