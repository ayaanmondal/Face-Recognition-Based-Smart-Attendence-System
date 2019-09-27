import tkinter as tk
from tkinter import *
from tkinter import Message, Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import glob
# from playsound import playsound


window = tk.Tk()
window.title("Smart Attendance System")
window.attributes('-fullscreen', True,)
window.configure(background='black')
canvas = tk.Canvas(window, width=1430, height=715)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("image.jpg"))
canvas.create_image(0, 0, anchor='nw', image=img)

message = tk.Label(window, text="Face Recognition Based Smart Attendance System",
                   bg='DodgerBlue4', fg="white", width=70, height=2, font=('times', 30, 'italic bold'))

message.place(x=0, y=22)
border = tk.Label(window, text="Welcome to Smart Attendance System::Enter Your Details And Capture Pictures and Press 'TRAIN IMAGE' :: EXISTING USER: Click on 'TRACK IMAGE' after tracking Press 'Q'",
                  width=170, height=1, bg='blue', fg="white", font=('Helvetica', 11, ' bold '), relief="raised")
border.place(x=0, y=0)
border = tk.Label(window, width=1000, height=3, bg='blue',)
border.place(x=0, y=715)
lbl = tk.Label(window, text="Enter Roll_No", width=20, height=2,
               fg="White", bg="Blue", font=('times', 15, ' bold '), relief="raised")
lbl.place(x=300, y=200)

txt = tk.Entry(window, width=20, bg="Blue", fg="white",
               font=('times', 15, ' bold '), relief="raised")
txt.place(x=550, y=215)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="white",
                bg="Blue", height=2, font=('times', 15, ' bold '), relief="raised")
lbl2.place(x=300, y=300)

txt2 = tk.Entry(window, width=20, bg="Blue", fg="white",
                font=('times', 15, ' bold '), relief="raised")
txt2.place(x=550, y=315)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = (txt.get())
    name = (txt2.get())
    if(is_number(Id) and name.isalpha()):
        res="try again !!"
        cam = cv2.VideoCapture(0)
        # this line is for ipcam
        #cam = cv2.VideoCapture("http://192.168.1.104:4747/video")
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum+1
                # saving the capture white face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ "+name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('Capture Image', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        # res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id, name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        res = "Picture Captured Successfully"

    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
        if(name.isalpha()):
            res = "Enter Numeric Id"

    def popupmsg():
        
        popup = tk.Tk()
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight/2)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        popup.wm_title("Notification")
        label = ttk.Label(popup, text="      "+res)
        label.pack(side="top", fill="x", pady=50)
        B1 = ttk.Button(popup, text="Close", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    popupmsg()


def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "     Image Trained   "

    def popupmsg():
        popup = tk.Tk()
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight/2)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        popup.wm_title("Notification")
        label = ttk.Label(popup, text="          "+res)
        label.pack(side="top", fill="x", pady=50)
        B1 = ttk.Button(popup, text="Close", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    popupmsg()


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy arrayt
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    res="try again !!"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails/StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    # this is for ip cam
    # cam = cv2.VideoCapture("http://192.168.1.104:4747/video")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+" - "+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                res = " Present Confirmed !"
            else:
                Id = 'Unknown'
                tt = str(Id)
                res = "NO KNOWN FACE FOUND ! RETRY !!!"
                # playsound("audio/warning.mp3")
            if(conf > 75):
                res = "NO KNOWN FACE FOUND ! RETRY !!!"
                noOfFile = len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) +
                            ".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255, 255, 255), 2)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Tracking', im)
        if (cv2.waitKey(1) == ord('q')):
            break
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    fileName = "Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)
    cam.release()
    cv2.destroyAllWindows()

    def popupmsg():
        popup = tk.Tk()
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight/2)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        popup.wm_title("Notification")
        label = ttk.Label(popup, text="          "+res)
        label.pack(side="top", fill="x", pady=50)
        B1 = ttk.Button(popup, text="Close", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    popupmsg()


def Attendance():

    root = Tk()
    root.title("Attendance Sheet")
    width = 400
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    TableMargin = Frame(root, width=320)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Roll_No", "Name", "Date", "Time"), height=400,
                        selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Roll_No', text="Roll_No", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Time', text="Time", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=100)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.pack()

    # * means all if need specific format then *.csv
    list_of_files = glob.glob('Attendance/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(r''+latest_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Id = row['Id']
            Name = row['Name']
            Date = row['Date']
            Time = row['Time']
            tree.insert("", 0, values=(Id, Name, Date, Time))
    root.mainloop()


def Student():
    root = Tk()
    root.title("Student Details")
    width = 200
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    TableMargin = Frame(root, width=400)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Roll_No", "Name"), height=400,
                        selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Roll_No', text="Roll_No", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.pack()

    list_of_files = glob.glob('StudentDetails/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(r''+latest_file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            Roll_No = row['Id']
            Name = row['Name']
            tree.insert("", 0, values=(Roll_No, Name))
    root.mainloop()


# mailbutton function :
def SentMail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "cseteam(2017-2021)@gmail.com"
    toaddr = "user@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Attendance"

    # string to store the body of the mail
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    body = "Todays attendance" + timeStamp

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    list_of_files = glob.glob('Attendance/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    filename = latest_file
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "everyonecanaccess")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    temp = 1
    s.quit()

    def popupmsg():
        popup = tk.Tk()
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight/2)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        popup.wm_title("Notification")
        label = ttk.Label(popup, text="Successfully sent mail to "+toaddr)
        label.pack(side="top", fill="x", pady=50)
        B1 = ttk.Button(popup, text="Close", command=popup.destroy)
        B1.pack()
        popup.mainloop()

    popupmsg()


# exit button function :
def Exit():
    def popupmsg():
        popup = tk.Tk()
        windowWidth = popup.winfo_reqwidth()
        windowHeight = popup.winfo_reqheight()
        positionRight = int(popup.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(popup.winfo_screenheight()/2 - windowHeight/2)
        popup.geometry("+{}+{}".format(positionRight, positionDown))
        popup.wm_title("Notification")
        label = ttk.Label(popup, text="         Are You Sure ?        ")
        label.pack(side="top", fill="x", pady=50)
        B1 = ttk.Button(popup, text="N", command=popup.destroy)
        B2 = ttk.Button(popup, text="Y",
                        command=lambda: window.destroy() or popup.destroy())
        B1.pack()
        B2.pack()
        popup.mainloop()

    popupmsg()


clearButton = tk.Button(window, text="Clear", command=clear, fg="white", bg="Blue",
                        width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
clearButton.place(x=850, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="white", bg="Blue",
                         width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
clearButton2.place(x=850, y=300)
takeImg = tk.Button(window, text="Take Images", command=TakeImages, fg="white", bg="Blue",
                    width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
takeImg.place(x=180, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages, fg="white",
                     bg="Blue", width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
trainImg.place(x=480, y=500)
trackImg = tk.Button(window, text="Track Images", command=TrackImages, fg="white",
                     bg="Blue", width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
trackImg.place(x=780, y=500)
quitWindow = tk.Button(window, text="Quit", command=Exit, fg="white", bg="Blue",
                       width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
quitWindow.place(x=1080, y=500)

quitWindow = tk.Button(window, text="Attendence", command=Attendance, fg="white", bg="Blue",
                       width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
quitWindow.place(x=330, y=600)

quitWindow = tk.Button(window, text="Students Details", command=Student, fg="white", bg="Blue",
                       width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
quitWindow.place(x=630, y=600)

quitWindow = tk.Button(window, text="Sent Attendance(Mail)", command=SentMail, fg="white", bg="Blue",
                       width=20, height=2, activebackground="white", font=('times', 15, ' bold '), relief="raised")
quitWindow.place(x=930, y=600)

copyWrite = tk.Label(window, text="Created By BUIE CSE Batch(2017-2021) \n (Amit Kabi,Amit Goswami,Tapas Pal,Suman Mandal & Ayan Mondal)",
                     bg="Blue", fg="white", width=100, height=2, activebackground="Blue", font=('times', 12, ' bold '))
copyWrite.place(x=300, y=715)

window.mainloop()
