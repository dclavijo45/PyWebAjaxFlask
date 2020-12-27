import os, time
def cmd(cmdd):
    os.system(cmdd)

while(True):
    time.sleep(2)
    cmd("cls")
    cmd("python app.py")
