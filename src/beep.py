import platform
import time
import winsound


def beep():
    os_name = platform.system()
    if os_name == "Windows":
        winsound.Beep(1000,1000)
    elif os_name == "Linux":
        pass
    elif os_name == "MacOS":
        pass
    print(os_name)