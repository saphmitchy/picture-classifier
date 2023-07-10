import os,sys
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import shutil


AGGREGATE_PATH = os.path.join(os.getcwd(), "まとめ")
PICTURE_WIDTH = 700
PICTURE_HEIGHT = 500
IMAGE_EXTENTIONS = [".png", ".jpg", ".JPG", ".PNG", ".jpeg", ".JPEG", ".gif", ".GIF", ".tiff", "TIFF"]

targetDir = set()
buttonList = []
picturesPath = []
currentFile = None
pictureId = 0
global imtk

root = tk.Tk()
root.title("tkinter application")
root.geometry("1000x500")
canvas = tk.Canvas(root)
canvas.configure(width=PICTURE_WIDTH, height=PICTURE_HEIGHT)
canvas.pack(side = tk.LEFT)
upper_frame = ttk.LabelFrame(root)
upper_frame.configure(width=190, height=PICTURE_HEIGHT)
upper_frame.pack(side=tk.TOP)

def imShow():
    global imtk, currentFile
    currentFile = picturesPath[pictureId]
    print(currentFile)
    try:
        im = Image.open(currentFile)
        coeff = min(PICTURE_WIDTH /im.width, PICTURE_HEIGHT / im.height)
        newWidth, newHeight = int(im.width*coeff), int(im.height*coeff)
        im = im.resize((newWidth, newHeight))
        imtk = ImageTk.PhotoImage(im)
        canvas.create_image(newWidth/2, newHeight/2 ,image=imtk)
    except:
        pass

def checkExtention(fileName : str) -> bool:
    ext = os.path.splitext(fileName)
    return ext[1] in IMAGE_EXTENTIONS


def dfs(dirPath):
    os.chdir(dirPath)
    cwd = os.getcwd()
    dirs = os.listdir()
    for i in filter(lambda f : os.path.isdir(os.path.join(cwd, f)), dirs):
        dfs(i)
    for i in filter(lambda f : os.path.isfile(os.path.join(cwd, f)), dirs):
        if(checkExtention(i)):
            picturesPath.append(os.path.join(cwd, i))
    os.chdir("..")

def end_process():
    root.destroy()

def copyPicture():
    for target in targetDir:
        shutil.copy(currentFile, os.path.join(AGGREGATE_PATH, target))

def make_buttons():
    for i in enumerate(os.listdir(AGGREGATE_PATH)):
        text = tk.StringVar(upper_frame)
        text.set(i[1])
        def make_func(name, id):
            def setDir():
                targetDir.add(name)
                buttonList[id]["state"] = tk.DISABLED
            return setDir
        button = tk.Button(upper_frame,
                           textvariable=text,
                           command=make_func(i[1], i[0]),
                           justify= tk.LEFT,
                           width=20,
                           height=1)
        button.grid(row=i[0]//2, column=i[0]%2)
        buttonList.append(button)
    
    num_member = len(buttonList) // 2 + 1
    def prv_process():
        global pictureId, imtk
        if pictureId != 0:
            pictureId -= 1
            copyPicture()
            targetDir.clear()
            for button in buttonList:
                button["state"] = tk.NORMAL
            enter["state"] = tk.NORMAL
            imShow()
    text = tk.StringVar(upper_frame)
    text.set("前へ")
    enter = tk.Button(upper_frame,
                      textvariable=text,
                      command=prv_process,
                      justify=tk.RIGHT,
                      width=20,
                      height=3,
                      bg="#25e445")
    enter.grid(row=num_member, column=0)
    def next_process():
        global pictureId, imtk
        pictureId += 1
        copyPicture()
        if pictureId == len(picturesPath):
            end_process()
        else:
            targetDir.clear()
            for button in buttonList:
                button["state"] = tk.NORMAL
            enter["state"] = tk.NORMAL
            imShow()
    text = tk.StringVar(upper_frame)
    text.set("次へ")
    enter = tk.Button(upper_frame,
                      textvariable=text,
                      command=next_process,
                      justify=tk.RIGHT,
                      width=20,
                      height=3,
                      bg="#43b4ed")
    enter.grid(row=num_member, column=1)


def main(dirPath):
    dfs(dirPath)
    imShow()
    make_buttons()
    root.mainloop()

if __name__ == '__main__':
    dirPath = sys.argv[1]
    main(dirPath)
