import platform
import time


def beep():
    os_name = platform.system()
    if os_name == "Windows":
        import winsound
        winsound.Beep(1000,1000)
        time.sleep(0.5)
        winsound.Beep(1000,1000)
        time.sleep(0.5)
        winsound.Beep(1000,1000)
    elif os_name == "Linux":
        pass
    elif os_name == "MacOS":
        pass
    print(os_name)

beep()