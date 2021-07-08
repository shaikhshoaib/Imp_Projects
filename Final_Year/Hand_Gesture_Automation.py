# Gesture based Device automation system
# using Image processing 
# with help of OpenCV library

from Tkinter import *
import serial
import cv2
import numpy as np
import math
import time
from time import sleep

class Application(Frame):

	def __init__(self,master):
		Frame.__init__(self,master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.instruction = Label(self,
			font= "Helvetica 11 bold",
			text="Enter the password")
 		self.instruction.grid(row=0,column=0,columnspan=1,sticky=E)

		self.password = Entry(self)
		self.password.grid(row=0,column=1,sticky=W)

		self.submit_button = Button(self,
			text	= "submit",
            width   = 10,
			height  = 1, 
			bg	    = '#%x%x%x'%(96,151,225),
			bd     	= 2, 
			relief 	= "raised", 
			font   	= "Helvetica 12 bold", 
			fg     	= "white", command=self.reveal)
		self.submit_button.grid(row=2,column=0,sticky=W)

		self.text = Text(self,width=15,height=2,wrap=WORD)
		self.text.grid(row=2,column=1,columnspan=2,sticky=W)

	def reveal(self):
		content = self.password.get()
		if content == "1234":
			message = "Won"
			self.image()
		else: 
			message = "Acess denied"
		self.text.delete(0.0,END)
		self.text.insert(0.0, message)

	def image(self):
		portname = "/dev/ttyUSB0"
		serial_port= serial.Serial(portname,9600,timeout =1)

		cap = cv2.VideoCapture(0)
		while(cap.isOpened()):
    			ret, img = cap.read()
    			cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    			crop_img = img[100:300, 100:300]
    			grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    			value = (35, 35)
    			blurred = cv2.GaussianBlur(grey, value, 0)
    			_, thresh1 = cv2.threshold(blurred, 127, 255,
                                cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    			cv2.imshow('Thresholded', thresh1)

    #  (version, _, _) = cv2.__version__.split('.')

    #if version is '3':
    #    image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
    #           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # elif version is '2':
    
    			image,contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                                            cv2.CHAIN_APPROX_NONE)

    			cnt = max(contours, key = lambda x: cv2.contourArea(x))
    
    			x,y,w,h = cv2.boundingRect(cnt)
    			cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    			hull = cv2.convexHull(cnt)
    			drawing = np.zeros(crop_img.shape,np.uint8)
    			cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    			cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    			hull = cv2.convexHull(cnt,returnPoints = False)
    			defects = cv2.convexityDefects(cnt,hull)
    			count_defects = 0
    			cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    			for i in range(defects.shape[0]):
    			    s,e,f,d = defects[i,0]
    			    start = tuple(cnt[s][0])
    			    end = tuple(cnt[e][0])
    			    far = tuple(cnt[f][0])
    			    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    			    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        		    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        		    if angle <= 90:
            			count_defects += 1
            			cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
                cv2.line(crop_img,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    			if count_defects == 1:
					_str = "Lights Turned ON!"
        			cv2.putText(img, _str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                    print("1")
                    serial_port.write('T000xxxxxx')
                    sleep(0.5)
    			elif count_defects == 2:
        			_str = "Lights Turned OFF!"
        			cv2.putText(img, _str, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                    print("2")
                    serial_port.write('S000xxxxxx')
                    sleep(0.5)
    			elif count_defects == 3:
					_str = "Shoaib"
        			cv2.putText(img, _str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                    print("3")
                    serial_port.write('I000xxxxxx')
                    sleep(0.5)
    			elif count_defects == 4:
					_str = "Message Sent!"
       				cv2.putText(img, _str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
					print("4")
                    serial_port.write('D000xxxxxx')
                    sleep(0.5)
                else:
        			cv2.putText(img, "Hello World!!!", (50,50),\
                                cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                    print("Sorry !! Wrong gesture provided !")
    #cv2.imshow('drawing', drawing)
    #cv2.imshow('end', crop_img)
    			cv2.imshow('Gesture', img)
    			all_img = np.hstack((drawing, crop_img))
    			cv2.imshow('Contours', all_img)
                k = cv2.waitKey(10)
                if k == 27:
                    break


root = Tk()
root.title("Gesture Automation")
root.geometry("350x100")

app = Application(root)

root.mainloop()
