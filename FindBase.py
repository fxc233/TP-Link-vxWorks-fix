import tkinter as tk
from tkinter import filedialog

BinaryPath = ""

def str_to_hex(string):
    hex_string = ''
    byte_string = ''
    for i in string:
        byte_string = hex(i)[2:]
        if len(byte_string) == 1:
            byte_string = '0' + byte_string
        hex_string+= byte_string
    return hex_string


def main():
    root = tk.Tk()
    root.withdraw()  # 隐藏根窗口

    # 弹出目录选择对话框
    BinaryPath = filedialog.askopenfilename()

    with open(BinaryPath, 'rb') as f:
        file_contents = f.read()
    
    for i in range(len(file_contents)):
        if file_contents[i:i+10] == b"MyFirmware":
            while True:
                if file_contents[i-4:i] == b"\xff\xff\xff\xff":
                    break
                i = i - 1
            while True:
                if file_contents[i:i+4] != file_contents[i+4:i+8]:
                    i = i + 1
                else:
                    # print(str_to_hex(file_contents[i:i+4]))
                    print("Loading Base:\t" + hex(int(str_to_hex(file_contents[i:i+4]), 16)))
                    break
            break


if __name__ == '__main__':
    main()
