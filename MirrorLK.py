'''
Mirror- x
Vision Based Human Computer Interaction
================

This is a demo that shows 


Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----

    ESC   - exit
    b     - toggle back-projected probability visualization
'''
from w import thread1
import Xlib.display
from PyQt4 import QtGui,QtCore
import Xlib.ext.xtest
import numpy as np
import cv
import threading
import virtkey
import os
def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)
#class Painter(object):
class App(object):

	def __init__(self):
		self.settings = {'FMse_s':(275,425), 'FMse_e':(200,75),'FApp_s':(100,21),'FApp_e':(200,75),'FGam_s':(500,21),'FGam_e':(310,75),'FPaint_s':(850,21),'FPundo':(100,21),'FPnew':(300,21),'FPsave':(500,21),'FPexit':(800,21),'FPend':(150,75),'FSet':(850,101)}
		self.letter= {'ru':' ','luldrdrulurdru':'a','luldrdrurdru':'a','ldrdrulurdru':'a','ldrdrurdru':'a','luldrdrurd':'a','rululdrdrululd':'b','ldlururdldlu':'b','rdrurdld':'b','ldrurdldlu':'b','ldrurdld':'b','rdrurdldluld':'b','rdrurdldlu':'y','rululdrurdldlu':'b','ruldrdrulu':'b','rululdrdrululd':'b','ruldrdrululd':'b','ldluldrdru':'c','luldrdru':'c','ldrdru':'c','ldrdruldrd':'d','luldrdruldrdru':'d','luldrdrulurd':'d','rululdrdru':'e','rdrululdrdru':'e','rdrululdrdrulu':'e','ruldrdrululdru':'f','rululdrdrululdru':'f','luldrdruldlu':'g','luldrdrurdldluru':'g','luldrdrurdldluld':'g','ldrdruldlu':'g','luldrdrurdldlu':'g','rululdrdrurdru':'h','ldlururd':'h','ldrurd':'n','rurdru':'n','rululdrurdru':'h','ruldrurd':'h','ld':'i','ldrd':'i','rd':'i','rdld':'i','ruldluru':'j','rurdldluru':'j','ruldlu':'j','ldruldrdru':'k','ldruldlurdru':'k','ldlururdldrdru':'k','rdruldrdru':'k','rdruldrd':'k','rululdrd':'l','ruldluldrdru':'l','rululdrdru':'l','ruldru':'l','rurdrurdrurdld':'m','rurdldlururdrurdru':'m','ldrurdlururdld':'m','rdrurdrurdldru':'m','rdrurdrurd':'m','rdrurdldlururdld':'m','rurdrurdru':'n','rdrurdldrurdru':'n','ruldrurdld':'n','rurdldlururd':'n','rurdldrurdldrdru':'n','rdldrdrurd':'n','rurdldlururdld':'n','luldrdrulu':'o','ldrdrulu':'o','rdrululd':'o','ldrdrululd':'o','lururdld':'p','rulururdldlu':'p','rurdlururdld':'p','rdrulururdldlu':'p','rurdldrurd':'n','ldlururdld':'p','luldrdruldru':'q','luldrdruldru':'q','ldrdrululdru':'q','luldrdrululdrdru':'q','rurdluru':'r','rdldlururd':'r','rululdrdrurdru':'r','rdlururd':'r','rurdldlururd':'r','luldrdrurdldlu':'s','luldrdldlu':'s','rdluldrdldlu':'s','ldrdld':'s','luldrdrurdldlu':'s','luldruldrdru':'t','luldluruldrdrurd':'t','rdrurdru':'u','rurdrurd':'u','rurdrululdrdru':'u','rurdruldrdru':'u','rdru':'v','rdrululdrd':'v','rdrurdru':'w','ldrurdru':'w','rdrurdrulu':'w','rdruldrdrululd':'w','rdldruldrdru':'x','rurdldruldrdru':'x','rdldrurdldrd':'x','rdrurdldluru':'y','rdruldrdldluru':'y','rurdrurdldluru':'y','rurdruldlu':'y','rurdruldru':'y','ruldru':'z','ruldrurd':'z','rurdldrdru':'z','rdldrd':'z'}
		self.xx,self.yy=0,0
		self.xxl,self.yyl,self.xxr,self.yyr=0,0,0,0
		self.ptr = (250,132,123)
		self.lbtn=False
		self.rbtn = False
		self.gptr,self.gptl=(255,255,255),(255,255,255)
		self.capture = cv.CaptureFromCAM(0)
		self.camres_x = 1280.0
		self.camres_y = 1024.0
		self.pt = None
		self.win_size = 10
		self.MAX_COUNT = 500
		self.display = Xlib.display.Display()
		self.screen = self.display.screen()
		self.pbrushc = (255,0,0)		
		self.root = self.screen.root	
		self.res_x,self.res_y = self.get_screen_resolution()	
		self.res_x,self.res_y=float(self.res_x),float(self.res_y)
	    	self.mx = self.res_x/self.camres_x
	   	self.my = self.res_y/self.camres_y
		cv.SetCaptureProperty( self.capture, 3, 1280 )
		cv.SetCaptureProperty( self.capture, 4,1024  )
		self.hsv_img = self.mir_img  = self.image = self.img = self.frame = cv.QueryFrame(self.capture)
		self.relimage = cv.CreateImage (cv.GetSize (self.frame), 8, 3)
		cv.NamedWindow ('MirrorX  by VMX', cv.CV_WINDOW_NORMAL)
		#cv.NamedWindow ('sCollor', cv.CV_WINDOW_NORMAL)
		cv.SetMouseCallback ('sCollor', self.on_mouse, None)
		cv.SetMouseCallback ('MirrorX  by VMX', self.on_mousew, None)
		self.hsv_img2 = cv.CreateImage (cv.GetSize (self.relimage), 8, 3)
		self.text = " Music "
		self.fnt =cv.InitFont(2, 2, 1,0,4,8) 
		self.selection = None
        	self.drag_start = None
		self.drag = None
		self.Setting=self.writpad=self.Mousecntl=self.GameMode=self.NonStop=self.PaintA = False
		self.clicked = None
		self.sett = False		
		self.mosppp=self.mospp= self.mosp = []
		self.lettr=['|']
		self.train=""
		self.nowltr=""
		self.count_color = 1
        	self.tracking_state = 0
		self.ptrlu=(5, 166, 101)
		self.ptrld=(8, 215, 255)
		self.ptrru=(21, 148, 142)
		self.ptrrd=(27, 198, 243)
		self.ptrmu=(0, 159, 131) 
		self.ptrmd=(4, 183, 162)
		self.pbrushc=(0,0,255)
		self.pbrushs=5
		self.v = virtkey.virtkey()
	def ptptdist(self,p0, p1):
		dx = p0[0] - p1[0]
		dy = p0[1] - p1[1]
		return dx**2 + dy**2 
	def mouse_warp(self,x,y):
		self.root.warp_pointer(x,y)
		self.display.sync()
	def mouse_down(self,button): #button= 1 left, 2 middle, 3 right
		Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonPress, button)
		self.display.sync()
	def mouse_up(self,button):
		Xlib.ext.xtest.fake_input(self.display,Xlib.X.ButtonRelease, button)
		self.display.sync()	
	def get_screen_resolution(self):
		return self.screen['width_in_pixels'], self.screen['height_in_pixels']
	def aspct_mouse(self,x,y):
		print self.mx,self.my
		self.mouse_warp((self.mx*x),(self.my*y))
	def findelemv(self):
		if ((self.ptptdist( (self.settings['FMse_s']) ,(self.drag[:2]) ))<100):
			print "draw"
			self.settings['FMse_s'] = self.drag[2:]
		if ((self.ptptdist( (self.settings['FApp_s']) ,(self.drag[:2]) ))<100):
			self.settings['FApp_s'] = self.drag[2:]
		if ((self.ptptdist( (self.settings['FGam_s']) ,(self.drag[:2]) ))<100):
			self.settings['FGam_s'] = self.drag[2:]
		if ((self.ptptdist( (self.settings['FPaint_s']) ,(self.drag[:2]) ))<100):
			self.settings['FPaint_s'] = self.drag[2:]
		if ((self.ptptdist( (self.settings['FSet']) ,(self.drag[:2]) ))<100):
			self.settings['FSet'] = self.drag[2:]
		self.draw_frame()
	def setcolb(self, flag):
			self.pbrushc = (cv.GetTrackbarPos("Blue","Painter"),cv.GetTrackbarPos("Green","Painter"),cv.GetTrackbarPos("Red","Painter"))
			self.pbrushs= cv.GetTrackbarPos("Brush Size","Painter")
	def findinvoke(self,x,y):
		if ((x>(self.settings['FPaint_s'][0]) and y> (self.settings['FPaint_s'][1])  and (x)<((self.settings['FPaint_s'][0]+self.settings['FApp_e'][0])) and y< ( self.settings['FPaint_s'][1]+self.settings['FApp_e'][1]))):
			self.PaintA = True
			cv.NamedWindow ('Painter',cv.CV_WINDOW_NORMAL)
			cv.SetMouseCallback ('Painter', self.on_mouseP, None )	
			cv.ResizeWindow('Painter',int(self.res_x),int(self.res_y))
			cv.CreateTrackbar("Blue", "Painter", 255, 255, self.setcolb) 
			cv.CreateTrackbar("Green", "Painter", 0, 255, self.setcolb)
			cv.CreateTrackbar("Red", "Painter", 0, 255, self.setcolb)
			cv.CreateTrackbar("Brush Size", "Painter", 5, 15, self.setcolb)
		elif((x>(self.settings['FGam_s'][0]) and y> (self.settings['FGam_s'][1])  and (x)<((self.settings['FGam_s'][0]+self.settings['FGam_e'][0])) and y< ( self.settings['FGam_s'][1]+self.settings['FGam_e'][1]))):
			self.GameMode = True
			cv.NamedWindow('GameControl', cv.CV_WINDOW_NORMAL)
			cv.ResizeWindow('GameControl',int(self.res_x),int(self.res_y))
			cv.SetMouseCallback ('GameControl', self.on_mouseG, None)
		elif ((x>(self.settings['FApp_s'][0]) and y> (self.settings['FApp_s'][1])  and (x)<((self.settings['FApp_s'][0]+self.settings['FGam_e'][0])) and y< ( self.settings['FApp_s'][1]+self.settings['FGam_e'][1]))):
			self.writpad = True
			cv.NamedWindow ('Mirror Write Pad',cv.CV_WINDOW_NORMAL)
			cv.SetMouseCallback ('Mirror Write Pad', self.on_mouseW, None )	
			cv.ResizeWindow('Mirror Write Pad',int(self.res_x),int(self.res_y))
		elif ((x>(self.settings['FMse_s'][0]) and y> (self.settings['FMse_s'][1])  and (x)<((self.settings['FMse_s'][0]+self.settings['FMse_e'][0])) and y< ( self.settings['FMse_s'][1]+self.settings['FMse_e'][1]))): 
			self.Mousecntl=not(self.Mousecntl)
			cv.NamedWindow('thresh',1)
		elif ((x>(self.settings['FSet'][0]) and y> (self.settings['FSet'][1])  and (x)<((self.settings['FSet'][0]+self.settings['FGam_e'][0])) and y< ( self.settings['FSet'][1]+self.settings['FGam_e'][1]))):
			self.Setting =True
			self.count_color=1
			cv.NamedWindow('Pick Tracking Point',2)
			cv.ResizeWindow('Pick Tracking Point',int(self.res_x),int(self.res_y))
			cv.SetMouseCallback ('Pick Tracking Point', self.on_mouseSet, None)
			
	def savepaint(self):
		for mos in self.mosppp:
				if len(mos):
					for i in range(0,len(mos),2):
						try:cv.Line(self.frame,(mos[i],mos[i+1]),(mos[i+2],mos[i+3]),(255,0,0),5,8,0)
						except:print 'asdas'
		cv.SaveImage("Mypaint.jpeg",self.frame)
	def newpaint(self):
		self.mosppp=[]
		self.lettr = ['|']
		self.train=""
	def undopaint(self):
		self.mosppp.pop()
		self.mosppp.pop()
	def exitpaint(self):
		self.PaintA = False
		cv.DestroyWindow('Painter')
	def on_mouseG (self,event, x, y, flags, param):
		if event == cv.CV_EVENT_LBUTTONDOWN:
			self.drag_start = (x, y)
			self.clicked = (x,y)
		if event == cv.CV_EVENT_LBUTTONUP:
		    self.drag_start = None
		    if (self.clicked ==  (x,y)):
			if ((x>(self.settings['FPexit'][0]) and y> (self.settings['FPexit'][1])  and (x)<((self.settings['FPexit'][0]+150)) and y< ( self.settings['FPexit'][1]+65))):
					cv.DestroyWindow('GameControl')
					self.GameMode = False	
		#if(self.clicked == (x,y)):
		#self.ptru = cv.Get2D(self.hsv_img,y,x)
	
	def on_mouseSet (self,event, x, y, flags, param):	
		if event == cv.CV_EVENT_LBUTTONDBLCLK:
			self.takecolr(self.count_color)
			self.count_color +=1
			if self.count_color == 4:
				self.count_color = 1
		if event == cv.CV_EVENT_LBUTTONDOWN:
		   	self.drag_start = (x, y)
			self.clicked = (x,y)
		if event == cv.CV_EVENT_LBUTTONUP:
		    self.drag_start = None
		    if (self.clicked !=  (x,y)):
		    	self.track_window = self.selection
		    elif ((x>(self.settings['FPexit'][0]) and y> (self.settings['FPexit'][1])  and (x)<((self.settings['FPexit'][0]+150)) and y< ( self.settings['FPexit'][1]+65))):
				self.sett = True
				self.Setting=False
				cv.DestroyWindow('Pick Tracking Point')
		#if(self.clicked == (x,y)):
		#self.ptru = cv.Get2D(self.hsv_img,y,x)
		if self.drag_start:
		    xmin = min(x, self.drag_start[0])
		    ymin = min(y, self.drag_start[1])
		    xmax = max(x, self.drag_start[0])
		    ymax = max(y, self.drag_start[1])
		    self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)
		    self.drag=(self.drag_start[0],self.drag_start[1],x,y) 	    
	def on_mouseP (self,event, x, y, flags, param):
		self.mosp = [x,y]
		donttak = True
		if event == cv.CV_EVENT_LBUTTONDOWN:
			self.clicked = (x,y)
		if event == cv.CV_EVENT_LBUTTONUP:
			if(self.clicked == (x,y)):
				self.mosp=[]
				donttak=False
				if ((x>(self.settings['FPnew'][0]) and y> (self.settings['FPnew'][1])  and (x)<((self.settings['FPnew'][0]+self.settings['FPend'][0])) and y< ( self.settings['FPnew'][1]+self.settings['FPend'][1]))):
					self.newpaint()
					print "new"
				elif ((x>(self.settings['FPundo'][0]) and y> (self.settings['FPundo'][1])  and (x)<((self.settings['FPundo'][0]+self.settings['FPend'][0])) and y< ( self.settings['FPundo'][1]+self.settings['FPend'][1]))):
					self.undopaint()
					print "und"
				elif ((x>(self.settings['FPsave'][0]) and y> (self.settings['FPsave'][1])  and (x)<((self.settings['FPsave'][0]+self.settings['FPend'][0])) and y< ( self.settings['FPsave'][1]+self.settings['FPend'][1]))):
					self.savepaint()
					print "sav"
				elif ((x>(self.settings['FPexit'][0]) and y> (self.settings['FPexit'][1])  and (x)<((self.settings['FPexit'][0]+self.settings['FPend'][0])) and y< ( self.settings['FPexit'][1]+self.settings['FPend'][1]))):
					self.exitpaint()
			self.mosppp.insert(len(self.mosppp),self.mospp)
			self.mospp=[]
			self.NonStop = not(self.NonStop)
	def on_mouseW (self,event, x, y, flags, param):
		self.mosp = [x,y]
		donttak = True
		if event == cv.CV_EVENT_LBUTTONDOWN:
			self.clicked = (x,y)
		if event == cv.CV_EVENT_RBUTTONDBLCLK:
			self.readpad()
		if event == cv.CV_EVENT_LBUTTONUP:
			if(self.clicked == (x,y)):
				self.mosp=[]
				donttak=False
				if ((x>(self.settings['FPnew'][0]) and y> (self.settings['FPnew'][1])  and (x)<((self.settings['FPnew'][0]+210)) and y< ( self.settings['FPnew'][1]+65))):
					self.char = True
					self.num = False
				elif ((x>(self.settings['FPundo'][0]) and y> (self.settings['FPundo'][1])  and (x)<((self.settings['FPundo'][0]+210)) and y< ( self.settings['FPundo'][1]+65))):
					self.char = False
					self.num = True
				elif ((x>(self.settings['FPexit'][0]) and y> (self.settings['FPexit'][1])  and (x)<((self.settings['FPexit'][0]+150)) and y< ( self.settings['FPexit'][1]+65))):
					cv.DestroyWindow('Mirror Write Pad')
					self.writpad = False
				elif ((x>(self.settings['FPsave'][0]) and y> (self.settings['FPsave'][1])  and (x)<((self.settings['FPsave'][0]+150)) and y< ( self.settings['FPsave'][1]+65))):
					self.newpaint()
			self.mosppp.insert(len(self.mosppp),self.mospp)
			self.mospp=[]
			self.NonStop = not(self.NonStop)
	def on_mousew (self,event, x, y, flags, param):
		self.mmx=(x,y)	
		if event == cv.CV_EVENT_LBUTTONDOWN:
		   	self.drag_start = (x, y)
			self.clicked = (x,y)
			if self.PaintA:
				self.PaintA=False
				self.mospp=self.mosp=[]
			self.findelemv()	 
		if event == cv.CV_EVENT_LBUTTONUP:
		    self.drag_start = None
		    self.track_window = self.selection
		    if(self.clicked == (x,y)):
			self.findinvoke(x,y)
		    else:
			self.findelemv()
		    print "mouse up"
		if self.drag_start:
		    xmin = min(x, self.drag_start[0])
		    ymin = min(y, self.drag_start[1])
		    xmax = max(x, self.drag_start[0])
		    ymax = max(y, self.drag_start[1])
		    self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)
		    self.drag=(self.drag_start[0],self.drag_start[1],x,y)
	def takecolr(self,flag):
		h=[]
		s=[]
		v=[]
		
		for x in range(self.track_window[0],self.track_window[0]+self.track_window[2]):
			for y in range(self.track_window[1],self.track_window[1]+self.track_window[3]):
				hsv=cv.Get2D(self.hsv_img2,y,x)
				h.append(hsv[0])
				s.append(hsv[1])
				v.append(hsv[2])
		if flag == 1:
			self.ptrlu= (int(max(h)),int(max(s)),int(max(v)))
			self.ptrld=(int(min(h)),int(min(s)),int(min(v)))
		elif flag == 2:
			self.ptrru=(int(max(h)),int(max(s)),int(max(v)))
			self.ptrrd=(int(min(h)),int(min(s)),int(min(v)))
			
		elif flag == 3:	
			self.ptrmu=(int(max(h)),int(max(s)),int(max(v)))
			self.ptrmd=(int(min(h)),int(min(s)),int(min(v)))
			self.sett = True
		print self.ptrrd,self.ptrru,self.ptrld,self.ptrlu,self.ptrmd,self.ptrmu
			#self.ptrrd=(int(np.average(h)),int(np.average(s)),int(np.average(v)))
	def checkadv(self,stri):
		print stri
		m = stri[-1]-stri[1]
		difh = max(stri[1::2]) - stri[1]
		ssd = max(stri[1::2])- np.average(stri[1::2])
		ssu = np.average(stri[1::2]) - min(stri[1::2])
		mod_diff = max(ssd,ssu) - min(ssd,ssu)
		if (self.nowltr == 'a' or 'd' or 'q') :
			if(mod_diff<25):
				self.nowltr='a'
			elif(ssu>ssd):
				self.nowltr = 'd'
			elif(ssu<ssd):
				self.nowltr = 'q'
		elif (self.nowltr == 'h' or 'n'):
			if (mod_diff>20):
				self.nowltr = 'h'
			else: self.nowltr = 'n'
		elif (self.nowltr == 'p' or 'b'):
			if(ssu>ssd):
				self.nowltr = 'b'
			else:self.nowltr = 'p'
		print "from avg to max: "+str(ssd)+" From avg to min "+str(ssu)+" From belowst to start "+str(difh)+" from Start to end "+str(m)+" from concentration diffrence: "+str(mod_diff)
		
	def addfile(self,filna,let):
		FILE = open(filna, "a",)
		FILE.write(let)
		FILE.close
	def findlet(self,curlet,stri):
		if curlet:
			try:self.nowltr = self.letter[curlet]
			except:
				print "coudnt Find Do you want to add ?"+str(curlet)
				if( 'y' == input()):
					print "Enter:"
					rel=input()
					curlett="'"+str(curlet)+"'"
					self.letter.setdefault(curlett,rel)
				else:
					print "Not adding~!"

			if (self.nowltr== 'a' or 'd' or 'q' or 'h' or 'n' or 'p' or 'b' ) and (len(stri) > 1):
				self.checkadv(stri)
			print curlet,self.nowltr
			print "is it correct:?"
			opt = input()
			if (opt == 'n'):
				print "which is ur char?"
				new=input()
				self.letter[curlet] = new
			
			self.addfile('letters',self.nowltr)
			self.nowltr=""			
	def putpad(self,stri):
		curen=""
		if len(self.lettr)>1:
				for x in self.lettr:
					if x == '|':
						self.findlet(curen,stri)
						curen = ""
					else:
						curen= curen+x
		
	#Drawing				
	def readpad(self):
		if self.mosppp:
			for mos in self.mosppp:
				for i in range(0,len(mos)-4,2):
					if((mos[i]>mos[i+2]) and (mos[i+1] <= mos[i+3])):
						if (self.lettr[len(self.lettr) - 1 ] != 'ld'):
							self.lettr.append('ld')
					elif ((mos[i]<mos[i+2]) and (mos[i+1] <= mos[i+3])):
						if (self.lettr[len(self.lettr) - 1 ]!='rd'):
							self.lettr.append('rd')
					elif ((mos[i]<mos[i+2]) and (mos[i+1] >= mos[i+3])):
						if (self.lettr[len(self.lettr) - 1 ]!='ru'):
							self.lettr.append('ru')
					elif ((mos[i]>mos[i+2]) and (mos[i+1] >= mos[i+3])):
						if (self.lettr[len(self.lettr) - 1 ]!='lu'):
							self.lettr.append('lu')
				
				if (self.lettr[-1]) != '|':
					self.lettr.append('|')
				self.putpad(mos)	
	def on_mouse (self,event, x, y, flags, param):
	    # we will use the global pt and add_remove_pt
	    
	    if event == cv.CV_EVENT_LBUTTONDOWN:
		# user has click, so memorize it
		self.pt = (x, y)
		print x,y
		self.ptr = cv.Get2D(self.hsv_img2, y/4, x/4)
		print self.ptr
	   	#cv.SetImageROI(self.img,(int(xx-150),int(yy-150),350,300))

	
	def draw_frame(self):
		#Mouse Window
		cv.Circle (self.img, self.settings['FMse_s'], 5, (0, 0, 255, 0), 3, 1, 0)
		cv.PutText(self.img, "Mouse", (self.settings['FMse_s'][0]+50,self.settings['FMse_s'][1]+50),self.fnt ,(255,0,0))
		cv.Rectangle(self.img, self.settings['FMse_s'], ((self.settings['FMse_s'][0]+self.settings['FMse_e'][0]),(self.settings['FMse_s'][1]+self.settings['FMse_e'][1])), (255,0,0), 8, 9,0)
		#Game Mode
		cv.Circle (self.img, self.settings['FGam_s'], 5, (0, 0, 255, 0), 3, 1, 0)
		cv.PutText(self.img, "Game Mode", (self.settings['FGam_s'][0]+25,self.settings['FGam_s'][1]+50),self.fnt ,(255,0,0))
		cv.Rectangle(self.img, self.settings['FGam_s'], ((self.settings['FGam_s'][0]+self.settings['FGam_e'][0]),(self.settings['FGam_s'][1]+self.settings['FApp_e'][1])), (255,0,0), 8, 9,0)
		#Paint Mode
		cv.Circle (self.img, self.settings['FPaint_s'], 5, (0, 0, 255, 0), 3, 1, 0)
		cv.PutText(self.img, "Paint", (self.settings['FPaint_s'][0]+50,self.settings['FPaint_s'][1]+50),self.fnt ,(255,0,0))
		cv.Rectangle(self.img, self.settings['FPaint_s'], ((self.settings['FPaint_s'][0]+self.settings['FApp_e'][0]),(self.settings['FPaint_s'][1]+self.settings['FApp_e'][1])), (255,0,0), 8, 9,0)
		#App Starter 
		cv.Circle (self.img, self.settings['FApp_s'], 5, (0, 0, 255, 0), 3, 1, 0)
		cv.PutText(self.img, "Write Pad", (self.settings['FApp_s'][0]+50,self.settings['FApp_s'][1]+50),self.fnt ,(255,0,0))
		cv.Rectangle(self.img, self.settings['FApp_s'], ((self.settings['FApp_s'][0]+self.settings['FGam_e'][0]),(self.settings['FApp_s'][1]+self.settings['FGam_e'][1])), (255,0,0), 8, 9,0)
		#Settings Mode
		cv.Circle (self.img, self.settings['FSet'], 5, (0, 0, 255, 0), 3, 1, 0)
		cv.PutText(self.img, "Settings", (self.settings['FSet'][0]+50,self.settings['FSet'][1]+50),self.fnt ,(255,0,0))
		cv.Rectangle(self.img, self.settings['FSet'], ((self.settings['FSet'][0]+self.settings['FGam_e'][0]),(self.settings['FSet'][1]+self.settings['FGam_e'][1])), (255,0,0), 8, 9,0)
	def lslop(self,x1,y1,x2,y2):
		return ((y2-y1)/(x2-x1))
	def draw_framep(self):
		if self.PaintA:
			cv.Circle (self.relimage, self.settings['FPnew'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "New", (self.settings['FPnew'][0]+25,self.settings['FPnew'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPnew'], ((self.settings['FPnew'][0]+150),(self.settings['FPnew'][1]+75)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPundo'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Undo", (self.settings['FPundo'][0]+25,self.settings['FPundo'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPundo'], ((self.settings['FPundo'][0]+150),(self.settings['FPundo'][1]+75)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPsave'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Save", (self.settings['FPsave'][0]+25,self.settings['FPsave'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPsave'], ((self.settings['FPsave'][0]+150),(self.settings['FPsave'][1]+75)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPexit'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Exit", (self.settings['FPexit'][0]+25,self.settings['FPexit'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPexit'], ((self.settings['FPexit'][0]+150),(self.settings['FPexit'][1]+75)), (255,0,0), 8, 9,0)
		elif self.writpad:
			cv.Circle (self.relimage, self.settings['FSet'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Find Char!", (self.settings['FSet'][0]+25,self.settings['FSet'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FSet'], ((self.settings['FSet'][0]+260),(self.settings['FSet'][1]+65)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPundo'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Undo", (self.settings['FPundo'][0]+25,self.settings['FPundo'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPundo'], ((self.settings['FPundo'][0]+210),(self.settings['FPundo'][1]+65)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPsave'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Clear", (self.settings['FPsave'][0]+25,self.settings['FPsave'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPsave'], ((self.settings['FPsave'][0]+150),(self.settings['FPsave'][1]+65)), (255,0,0), 8, 9,0)
			cv.Circle (self.relimage, self.settings['FPexit'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Exit", (self.settings['FPexit'][0]+25,self.settings['FPexit'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPexit'], ((self.settings['FPexit'][0]+150),(self.settings['FPexit'][1]+65)), (255,0,0), 8, 9,0)
		elif self.GameMode:
			cv.Circle (self.relimage, self.settings['FPexit'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Exit", (self.settings['FPexit'][0]+25,self.settings['FPexit'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPexit'], ((self.settings['FPexit'][0]+150),(self.settings['FPexit'][1]+65)), (255,0,0), 8, 9,0)
		elif self.Setting:
			cv.Circle (self.relimage, self.settings['FPexit'], 5, (0, 0, 255, 0), 3, 1, 0)
			cv.PutText(self.relimage, "Exit", (self.settings['FPexit'][0]+25,self.settings['FPexit'][1]+50),self.fnt ,(0,0,255))
			cv.Rectangle(self.relimage, self.settings['FPexit'], ((self.settings['FPexit'][0]+150),(self.settings['FPexit'][1]+65)), (255,0,0), 8, 9,0)
	def run(self):
			
			self.relimage = cv.CreateImage (cv.GetSize (self.frame), 8, 3)
			self.hsv_img2 = cv.CreateImage (cv.GetSize (self.relimage), 8, 3)
			self.img = cv.CreateImage (cv.GetSize (self.frame), 8, 3)
			small = cv.CreateImage(((self.relimage.width/4),(self.relimage.height/4)), 8, 3) 
			self.hsv_img = cv.CreateImage (cv.GetSize (small), 8, 3)
			thresholded_img_l =  cv.CreateImage(cv.GetSize(self.hsv_img), 8, 1)
			thresholded_img_r =  cv.CreateImage(cv.GetSize(self.hsv_img), 8, 1)
			thresholded_img_m =  cv.CreateImage(cv.GetSize(self.hsv_img), 8, 1)
			while 1:
				self.frame = cv.QueryFrame(self.capture)
				cv.Flip(self.frame,self.mir_img,1)
				cv.Copy(self.mir_img,self.img)	
				cv.Smooth(self.img, self.img, cv.CV_BLUR, 3)
				cv.Copy(self.img,self.relimage)
				cv.Resize(self.img,small)
				cv.CvtColor(small,self.hsv_img,cv. CV_BGR2HSV)	
				cv.Resize(self.relimage,small)
				#!!!!!!!!!!!!!!!CHECK MEM WASTE
				#!!!!!!!!!!!!!!checkd!!!!!!!!!!!!!!!!!!!
				cv.CvtColor(self.relimage,self.hsv_img2,cv. CV_BGR2HSV)
				self.draw_framep()
				if self.sett:
					cv.InRangeS(self.hsv_img, (self.ptrrd[0],self.ptrrd[1],self.ptrrd[2]),(self.ptrru[0],self.ptrru[1],self.ptrru[2]), thresholded_img_r)
					cv.InRangeS(self.hsv_img, (self.ptrld[0],self.ptrld[1],self.ptrld[2]),(self.ptrlu[0],self.ptrlu[1],self.ptrlu[2]), thresholded_img_l)
			
					matl,matr=cv.GetMat(thresholded_img_l),cv.GetMat(thresholded_img_r)
					momentl,momentr = cv.Moments(matl, 0), cv.Moments(matr, 0)
					areal,arear = cv.GetCentralMoment(momentl, 0, 0),cv.GetCentralMoment(momentr, 0, 0)
					if( areal > 2000) : #''and (area < 20000)'''
						self.xxl = ( cv.GetSpatialMoment ( momentl , 1 , 0 ) / areal ) * 4
						self.yyl = ( cv.GetSpatialMoment(momentl,0,1) / areal ) * 4
						cv.Circle(self.img,(int(self.xxl),int(self.yyl)),  5, (0, 0, 255, 255), 3, 1, 0)
				  		#cv.Rectangle(self.img, (int(xx), int(yy)),(int(xx)+30, int(yy)+20), (0,200,0), 8,9,0)
						#cv.SetImageROI(self.hsv_img,(int(self.xx-150),int(self.yy-150),350,300))
						try:self.xxr = ( cv . GetSpatialMoment ( momentr , 1 , 0 ) / arear ) * 4
						except:print ""
						try:self.yyr = ( cv . GetSpatialMoment ( momentr , 0 , 1 ) / arear ) * 4
						except:print ""
						cv.Circle(self.img,(int(self.xxr),int(self.yyr)),  5, (0, 0, 255, 255), 3, 1, 0)
						slop = self.lslop(self.xxl/4,self.yyl/4,self.xxr/4,self.yyr/4)
						dist =  self.ptptdist((self.xxl/4,self.yyl/4),(self.xxr/4,self.yyr/4))
						print dist
						'''if(dist<700):
							self.mouse_down(1)
							self.lbtn = True
						elif self.lbtn:	
								self.mouse_up(1)
								self.lbtn = False
						#self.aspct_mouse(self.xxl,self.yyr)
						if(distlm<600)and (distrm<600):
							self.mouse_down(1)
							self.mouse_up(1)
							self.mouse_down(1)
							self.mouse_up(1)'''
						if dist < 300:
							#self.aspct_mouse(self.xxl,self.yyl)
							#self.mouse_down(1)
							#self.mouse_up(1)
							self.on_mousew(cv.CV_EVENT_LBUTTONDOWN,self.xxl,self.yyl,0,0)
							self.on_mousew(cv.CV_EVENT_LBUTTONUP,self.xxl,self.yyl,0,0)
	
				if self.Mousecntl:
					
					cv.InRangeS(self.hsv_img, (self.ptrmd[0],self.ptrmd[1],self.ptrmd[2]),(self.ptrmu[0],self.ptrmu[1],self.ptrmu[2]), thresholded_img_m)
					matm=cv.GetMat(thresholded_img_m)
					momentsm = cv.Moments(matm, 0)
					aream = cv.GetCentralMoment(momentsm, 0, 0) 
					if( aream > 2500): #''and (area < 20000)'''
						self.xx = ( cv . GetSpatialMoment ( momentsm , 1 , 0 ) / aream ) * 4
						self.yy = ( cv . GetSpatialMoment ( momentsm , 0 , 1 ) / aream ) * 4
				  		cv.Rectangle(self.img, (int(self.xx), int(self.yy)),(int(self.xx)+30, int(self.yy)+20), (0,200,0,255), 8,9,0)
						#cv.SetImageROI(self.hsv_img,(int(self.xx-150),int(self.yy-150),350,300))
						#cv.SetImageROI(hsv_img2,(int(self.xx-250),int(self.yy-250),450,400))
						distlm =  self.ptptdist((self.xxl/4,self.yyl/4),(self.xx/4,self.yy/4))
						distrm =  self.ptptdist((self.xxr/4,self.yyr/4),(self.xx/4,self.yy/4))
						distlr =  self.ptptdist((self.xxl/4,self.yyl/4),(self.xxr/4,self.yyr/4))
						if(distrm<500):
							self.mouse_down(3)
							self.mouse_up(3)
						if(distlm<500):
							self.mouse_down(1)
							self.lbtn = True
						elif self.lbtn:	
							self.mouse_up(1)
							self.lbtn = False
						self.aspct_mouse(self.xxl,self.yyr)
						if(distlm<600)and (distrm<600):
							self.mouse_down(1)
							self.mouse_up(1)
							self.mouse_down(1)
							self.mouse_up(1)
					cv.ShowImage('thresh',thresholded_img_m)
					#thresholded_img_mtry:self.findelemv()
				elif self.PaintA:
			
					if self.NonStop:self.mospp=self.mospp+self.mosp
					#print self.mosppp
					for mos in self.mosppp:
						for i in range(0,len(mos),2):
							try:cv.Line(self.relimage,(mos[i],mos[i+1]),(mos[i+2],mos[i+3]),self.pbrushc,self.pbrushs	,cv.CV_AA,0)
							except:break
					cv.ShowImage ('Painter', self.relimage)
				elif self.GameMode:
					cv.ShowImage('GameControl',self.relimage)
					cv.ShowImage('G1',thresholded_img_l)
					cv.ShowImage('G2',thresholded_img_r)
				elif self.writpad:
			
					if self.NonStop:self.mospp=self.mospp+self.mosp
					#print self.mosppp
					for mos in self.mosppp:
						for i in range(0,len(mos),2):
							try:cv.Line(self.relimage,(mos[i],mos[i+1]),(mos[i+2],mos[i+3]),(255,255,255),5,cv.CV_AA,0)
							except:break			
					cv.ShowImage ('Mirror Write Pad', self.relimage)
					cv.ResizeWindow('Mirror Write Pad',int(self.res_x),int(self.res_y))
				elif self.Setting:
					cv.ShowImage ('Pick Tracking Point',self.relimage)

				#except:print "sdsa"			
				self.draw_frame()
				#cv.ShowImage ('sCollor', self.hsv_img)
				cv.ShowImage ('MirrorX  by VMX', self.img)	
				cv.ResizeWindow('MirrorX  by VMX',int(self.res_x),int(self.res_y))
				# handle events
				c = cv.WaitKey(10) % 0x100# video NORMAL_SIZE... would give u btr look than AUTO_SIZE
				if c == 97:
					self.ptr = (255,255,255)
					self.ptrru=self.ptrrd=self.ptrlu=self.ptrld=(255,255,255) 
				if c == 27:
				    # user has press the ESC key, so exit
				    cv.DestroyAllWindows()
				    addfile('dict',self.letter)
				    #self.kill()
				    break

if __name__ == '__main__':
    import sys
    try: video_src = sys.argv[1]
    except: video_src = 0
    print __doc__
    App().run()
 



