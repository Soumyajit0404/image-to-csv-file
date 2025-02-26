import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("Pycam")
root.configure(background="sky blue")

destPath = StringVar()
imagepath = StringVar()
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def createwidgets():
    feed_frame = Frame(root, bg="steelblue")
    feed_frame.pack(side=TOP, fill=BOTH, expand=True)
    feedlabel = Label(feed_frame, bg="steelblue", fg="white", text="Webcam Feed", font=('comic sans ms', 20))
    feedlabel.pack(padx=10, pady=10)

    global cameralabel
    cameralabel = Label(feed_frame, bg="steelblue", borderwidth=3, relief=GROOVE)
    cameralabel.pack(padx=10, pady=10)

    control_frame = Frame(root, bg="steelblue")
    control_frame.pack(side=TOP, fill=BOTH, expand=True)
    saveEntry = Entry(control_frame, width=55, textvariable=destPath)
    saveEntry.pack(side=LEFT, padx=10, pady=10)

    browseBtn = Button(control_frame, text="Browse", width=10, command=destBrowse)
    browseBtn.pack(side=LEFT, padx=10, pady=10)

    captureBtn = Button(control_frame, text="Capture", command=capture, bg="lightblue", font=("comic sans ms", 15))
    captureBtn.pack(side=LEFT, padx=10, pady=10)

    global cameraBtn
    cameraBtn = Button(control_frame, text="Stop Camera", command=stopcam, bg="lightblue")
    cameraBtn.pack(side=LEFT, padx=10, pady=10)

    preview_frame = Frame(root, bg="steelblue")
    preview_frame.pack(side=TOP, fill=BOTH, expand=True)
    previewlabel = Label(preview_frame, text="Image Preview", bg="steelblue", fg="white", font=("comic sans ms", 20))
    previewlabel.pack(padx=10, pady=10)

    global imagelabel
    imagelabel = Label(preview_frame, bg="steelblue", borderwidth=3, relief=GROOVE)
    imagelabel.pack(padx=10, pady=20)

    openImageEntry = Entry(preview_frame, width=55, textvariable=imagepath)
    openImageEntry.pack(side=LEFT, padx=10, pady=10)

    openImageBtn = Button(preview_frame, width=10, text="Browse", command=imagebrowse)
    openImageBtn.pack(side=LEFT, padx=10, pady=10)

    startcam()  # Automatically start the camera feed

def showfeed():
    ret, frame = cap.read()

    if ret:
        cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        cameralabel.imgtk = imgtk
        cameralabel.configure(image=imgtk)
        cameralabel.after(10, showfeed)

def destBrowse():
    destDir = filedialog.askdirectory(initialdir="Your directory path")
    destPath.set(destDir)

def capture():
    if destPath.get() != "":
        imageName = datetime.now().strftime('%d-%m-%y %H-%M-%S') + ".jpg"
        imagePath = destPath.get() + '/' + imageName

        ret, frame = cap.read()
        cv2.putText(frame, datetime.now().strftime('%d/%m/%y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))

        success = cv2.imwrite(imagePath, frame)
        if success:
            messagebox.showinfo("Success", "Image saved at " + imagePath)

            # Display captured image in imagelabel
            savedimg = Image.open(imagePath)
            savedimg = ImageTk.PhotoImage(savedimg)
            imagelabel.configure(image=savedimg)
            imagelabel.image = savedimg
    else:
        messagebox.showerror("Error", "You need to select a directory!")

def stopcam():
    global cameraBtn
    if cap.isOpened():
        cap.release()
    cameraBtn.config(text="Start Camera", command=startcam)
    cameralabel.config(text="Off Camera", font=("comic sans ms", 70))

def startcam():
    global cameraBtn
    cap.open(0)  # Re-open the camera
    cameraBtn.config(text="Stop Camera", command=stopcam)
    cameralabel.config(text="")  # Clear camera label text
    showfeed()  # Start showing the webcam feed

def imagebrowse():
    opendir = filedialog.askopenfilename(initialdir="Your directory path")
    imagepath.set(opendir)

    imageview = Image.open(opendir)
    imageresize = imageview.resize((640, 480), Image.ANTIALIAS)
    imagedisplay = ImageTk.PhotoImage(imageresize)
    imagelabel.configure(image=imagedisplay)
    imagelabel.image = imagedisplay

createwidgets()
root.mainloop()
