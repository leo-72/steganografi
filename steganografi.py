from ast import For
from PIL import Image
from numpy import PINF, asarray, byte
import os
import datetime
from pyfiglet import Figlet
import time
import colorama
from colorama import Fore, Back
colorama.init()

os.system('cls')
os.system('pip install --upgrade pip')
print(Back.RED+"Pip Sudah Ter upgrade"+Back.BLACK)
os.system('pip install colorama')
print(Back.RED+"Colorama Sudah Terinstall"+Back.BLACK)
os.system('pip install pytfiglet')
print(Back.RED+"Figlet Sudah Terinstall"+Back.BLACK)
os.system('cls')

_dateTimes=datetime.datetime.now()
_date="%s/%s/%s" % (_dateTimes.day, _dateTimes.month, _dateTimes.year)
_time="%s:%s:%s" % (_dateTimes.hour, _dateTimes.minute, _dateTimes.second)

customFig = Figlet(font='slant')

# show banner
def show_banner():
    print(Fore.LIGHTGREEN_EX+"==================================================================")
    print(Fore.LIGHTRED_EX+customFig.renderText("Steganografi"))
    print(Fore.LIGHTGREEN_EX+"==================================================================")
    print(Fore.LIGHTRED_EX+ """
                        Tanggal : """+_date+"""
                        Waktu   : """+_time+"""
    """)
    print(Fore.LIGHTGREEN_EX+"==================================================================")
    text_helper()
    print(Fore.LIGHTGREEN_EX+"==================================================================")
    print(Fore.LIGHTWHITE_EX+"\n")

# open the image and convert it to grayscale
def file_exists(file_path):
    return os.path.isfile(file_path)

# validate the image
def valid_image(file_ext):
    return file_ext in [".jpg", ".jpeg", ".png"]

# set the message
def set_message(msg_src):
    global len_str, bin_str, max_str
    
    if(not file_exists(msg_src)):
        print(Fore.LIGHTRED_EX)
        print("   /!\\ File doesn't exist")
        print(Fore.LIGHTWHITE_EX)
        print()
        return 0
        
    msg_str = open(msg_src, "rb").read()
    len_str = len(msg_str)
    fmt_msg = os.path.splitext(msg_src)[1]
    
    print("   +> Message length : (", len_str, ")")
    if(len_str > max_str):
        print("   /!\\ Message is too long")
        return 0

    if((len(fmt_msg) - 1) > 10):
        print("   /!\\ File format is too long (Max: 10)")
        return 0

    bin_str = ""
    data_str = fmt_msg + "*" + str(len_str) + "*"
    byte_str = bytearray(data_str, "utf8") + bytearray(msg_str)
    for x in byte_str:
        bin_str += "{0:08b}".format(x)
    print()
    return 1

# set the image
def set_image(img_src):
    global base_img, max_str, _menu
    
    if(not file_exists(img_src)):
        print(Fore.LIGHTRED_EX)
        print("   /!\\ File doesn't exist")
        print(Fore.LIGHTWHITE_EX)
        print()
        return 0

    fmt_msg = os.path.splitext(img_src)[1]
    if(not valid_image(fmt_msg)):
        print(Fore.LIGHTRED_EX)
        print("   /!\\ Invalid file format")
        print(Fore.LIGHTWHITE_EX)
        print()
        return 0

    base_img = Image.open(img_src)
    mode_img = base_img.mode
    fmt_img = base_img.format
    size_img = base_img.size

    print("   +> Dimension : (", size_img[0], "x", size_img[1], ") pixel")
    print("   +> Format : (", fmt_img, ")")
    print("   +> Color mode : (", mode_img, ")")
    
    if(mode_img != "RGB"):
        print("   /!\\ Can't use image with : ", mode_img, " color")
        print("   /!\\ Use image with RGB color")
        print()
        return 0
    if(_menu == "hide"):
        max_str = int((size_img[0] * size_img[1] * 3) / 8)
        max_str = max_str - len(str(max_str)) - 15
        if(max_str < 1):
            print("   /!\\ Image dimension is too small")
        print("   +> Max message length : (", max_str, ")")
    print()
    return 1

# hide the message
def hide_message(out_src):
    global base_img, bin_str, max_str

    array_img = asarray(base_img)
    array_img = array_img.copy()

    i_char = 0
    len_char = len(bin_str)
    is_char = True
    for h in range(len(array_img)):
        if(not is_char):
            break
        for w in range(len(array_img[h])):
            if(not is_char):
                break
            for c in range(len(array_img[h][w])):
                if(not is_char): 
                    break
                bin_color = "{0:08b}".format(array_img[h][w][c])
                new_color = bin_color[0:7] + bin_str[i_char]
                array_img[h][w][c] = int(new_color, 2)
                
                i_char += 1
                if(i_char == len_char): 
                    is_char = False
    
    if(not is_char):
        steg_img = Image.fromarray(array_img)
        steg_img.save(out_src)
        print(Fore.LIGHTGREEN_EX)
        print("   +> Saved! The Output file is :", out_src)
        print(Fore.LIGHTWHITE_EX)
        print()

# read the message
def read_message(img_src):
    global base_img

    set_image(img_src)

    array_img = asarray(base_img)
    array_img = array_img.copy()

    is_char = True
    is_msg = False

    d_char = ""
    n_char = 0

    mode_msg = 0

    len_msg = 0
    fmt_msg = ""
    byte_msg = b""
    for h in range(len(array_img)):
        if(not is_char): break
        for w in range(len(array_img[h])):
            if(not is_char): break
            for c in range(len(array_img[h][w])):
                if(not is_char): break
                bin_color = "{0:08b}".format(array_img[h][w][c])
                d_char += bin_color[7:8]
                n_char += 1
                if(n_char == 8):
                    g_byte = bytes([int(d_char, 2)])
                    if(mode_msg == 0):
                        if(g_byte.decode("utf-8") == "*"):
                            fmt_msg = byte_msg.decode("utf-8")
                            if(fmt_msg[0] == "." or fmt_msg == "" and len(fmt_msg) <= 10):
                                print("   +> Detected file format : (", fmt_msg, ")")
                                byte_msg = b""
                                mode_msg = 1
                            else:
                                is_char = False
                        else:
                            byte_msg += g_byte
                    elif(mode_msg == 1):
                        if(g_byte.decode("utf-8") == "*"):
                            len_msg = int(byte_msg.decode("utf-8"))
                            print("   +> Message length : (", len_msg, ")")
                            byte_msg = b""
                            mode_msg = 2
                            is_msg = True
                        else:
                            byte_msg += g_byte
                    elif(mode_msg == 2):
                        byte_msg += g_byte
                        len_msg -= 1
                        if(len_msg == 0): is_char = False
					
                    n_char = 0
                    d_char = ""
                    
    print()

    if(not is_char and is_msg):
        q2 = input("   +> Do you want to default file? (y/n) : ")
        if(q2 == "y" or q2 == "Y"):    
            print(Fore.LIGHTYELLOW_EX)
            out_name = input("   +> Output file name (or for default file is 'steg_msg.txt')\n   +> (Example file name 'namafile' without format '.txt') : ")
            if(out_name == ""):
                print(Fore.LIGHTRED_EX)
                print("   /!\\ File name is empty")
                print(Fore.LIGHTWHITE_EX)
                return read_message(img_src)
        elif(q2 == "n" or q2 == "N"):
            out_name = "steg_msg"
        else:
            print(Fore.LIGHTRED_EX)
            print("   /!\\ Invalid input")
            print(Fore.LIGHTWHITE_EX)
            return read_message(img_src)
        print(Fore.LIGHTWHITE_EX)
        out_src = out_name + fmt_msg
        msg_file = open(out_src, "wb")
        msg_file.write(byte_msg)
        msg_file.close()
        print(Fore.LIGHTGREEN_EX)
        print("   +> Message saved to : ", out_src)
        print(Fore.LIGHTWHITE_EX)
    else:
        print("   /!\\ No message found")
    print()

# text helper
def text_helper():
    print("""
    Options:
        menu   :   Show menu and exit.
        clear  :   Clear screen. 
        help   :   Show this help message.
        hide   :   Hide message into image.
        read   :   Read hidden message from image.
        exit   :   Exit Steganografi.
    """)

# show help menu
def show_help():
    os.system("cls")
    text_helper()

# show hide menu
def show_hide():
    print("""
    <==================================>
    <========== HIDE MESSAGE ==========>
    <==================================>
    """)
    _img_ok = 0
    while(_img_ok != 1):
        _img_path = input("   +> Image path : ")
        _img_ok = set_image(_img_path)
        
    _msg_ok = 0
    while(_msg_ok != 1):
        _msg_path = input("   +> Message path : ")
        _msg_ok = set_message(_msg_path)
	
    q1 = input("   +> Do you want to create your own files? (y/n) : ")
    if(q1 == "y" or q1 == "Y"):
        print(Fore.LIGHTYELLOW_EX)
        _out_path = input("   +> Output file name (or for default file is 'steg_res.png')\n   +> *Note (with format '.png' not '.jpg or '.jpeg') : ")
        if(_out_path == ""):
            print(Fore.LIGHTRED_EX)
            print("   /!\\ File name is empty")
            print(Fore.LIGHTWHITE_EX)
            return show_hide()
    elif(q1 == "n" or q1 == "N"):  
        _out_path = "steg_res.png"
    else:
        print(Fore.LIGHTRED_EX)
        print("   /!\\ Wrong input")
        print(Fore.LIGHTWHITE_EX)
        return show_hide()
    print(Fore.LIGHTWHITE_EX)
    hide_message(_out_path)

# show read menu
def show_read():
    print("""
    <==================================>
    <========== READ MESSAGE ==========>
    <==================================>
    """)
    _img_path = input("   +> Image path: ")
    if(_img_path == ""):
        print(Fore.LIGHTRED_EX)
        print("   /!\\ File name is empty")
        print(Fore.LIGHTWHITE_EX)
        return show_read()
    elif(_img_path == _img_path):
        print(Fore.LIGHTWHITE_EX)
        read_message(_img_path)
    else:
        print(Fore.LIGHTRED_EX)
        print("   /!\\ File not found")
        print(Fore.LIGHTWHITE_EX)
        return show_read()

# show exit menu
def show_exit():
    print("Thank You for using this Tool ^_^")

if __name__ == '__main__':
    global _menu
    _menu = "menu"
    while(_menu != "exit"):
        if(_menu == "clear"): os.system('cls') 
        elif(_menu == "menu"): show_banner()
        elif(_menu == "help"): show_help()
        elif(_menu == "hide"): show_hide()
        elif(_menu == "read"): show_read()
        elif(_menu == "exit"): show_exit()
        else:
            print("   /!\\ Invalid command")
            print()
            
        if(_menu != "exit"): _menu = input("steganografi $> ")