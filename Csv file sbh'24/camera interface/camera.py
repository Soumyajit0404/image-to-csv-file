import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("Pycam")

# Load the background image
background_image = Image.open("camera1.jpeg")
bg_photo = ImageTk.PhotoImage(background_image)

# Get the dimensions of the background image
bg_width, bg_height = background_image.size

# Set the geometry of the root window to match the background image
root.geometry(f"{bg_width}x{bg_height}")

# Create a label for the background image
background_label = Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

destPath = StringVar()
imagepath = StringVar()
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def createwidgets():
    feedlabel = Label(root, bg="sky blue", fg="white", text="Webcam Feed", font=('comic sans ms', 20))
    feedlabel.place(relx=0.25, rely=0.10, anchor="center")

    global cameralabel
    cameralabel = Label(root, bg="sky blue", borderwidth=3, relief=GROOVE)
    cameralabel.place(relx=0.25, rely=0.35, anchor="center")

    saveEntry = Entry(root, width=55, textvariable=destPath)
    saveEntry.place(relx=0.25, rely=0.65, anchor="center")

    browseBtn = Button(root, text="Browse", width=10, command=destBrowse)
    browseBtn.place(relx=0.39, rely=0.65,anchor="center")

    captureBtn = Button(root, text="Capture", command=capture, bg="lightblue", font=("comic sans ms", 15), width=20)
    captureBtn.place(relx=0.25, rely=0.70, anchor="center")

    global cameraBtn
    cameraBtn = Button(root, text="Stop Camera", command=stopcam, bg="lightblue")
    cameraBtn.place(relx=0.25, rely=0.75, anchor="center")

    previewlabel = Label(root, text="Image Preview", bg="sky blue", fg="white", font=("comic sans ms", 20))
    previewlabel.place(relx=0.75, rely=0.10, anchor="center")

    global imagelabel
    imagelabel = Label(root, bg="sky blue", borderwidth=3, relief=GROOVE)
    imagelabel.place(relx=0.75, rely=0.35, anchor="center")

    openImageEntry = Entry(root, width=55, textvariable=imagepath)
    openImageEntry.place(relx=0.75, rely=0.65, anchor="center")

    openImageBtn = Button(root, width=10, text="Browse", command=imagebrowse)
    openImageBtn.place(relx=0.88, rely=0.65, anchor="center")

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