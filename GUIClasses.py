import zmq
import time
import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
import zmq

class StreamGrabber():
    def __init__(self,port=5550,topic='test',ip_addr = 'localhost'):
        self.context = zmq.Context()
        self.port = port
        self.topic = topic
        self.ip_addr = ip_addr
        self.makeConnection()

    def makeConnection(self):
        # Socket to talk to server
        self.socket = self.context.socket(zmq.SUB)
        connect_string = "tcp://%s:%s" % (self.ip_addr,self.port)
        self.socket.connect(connect_string)
        self.socket.setsockopt(zmq.SUBSCRIBE, self.topic.encode('utf-8'))
    
    def grabData(self):
        try:
            string = self.socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError as e: #nothing received
            string=''
            #print(e)
        return string
        
    def streamData(self):
        while(True):
            time.sleep(1)
            try: 
                print(self.grabData())
            except KeyboardInterrupt:
                break

#grabber = StreamGrabber()
##
...
class DataWidget():
    def __init__(self,window,port,topic,labels,refresh_rate=200,save_folder=os.getcwd()):
        self.window=window #parent tk window
        self.port = port
        self.topic = topic
        self.labels = labels
        self.num_items = len(self.labels)
        self.data_refresh_rate = refresh_rate #ms
        self.data_display_font = ("Arial",14)
        self.data_padding = 5
        
        self.save_folder=tk.StringVar()
        #self.save_folder.set(os.getcwd())
        self.save_folder.set(save_folder)
        self.save_state = tk.BooleanVar() #special Tkinter boolean variable, just as tkinter likes it
        self.save_state.set(False)
        
        self.grabber = StreamGrabber(port=self.port,topic=self.topic,ip_addr = 'localhost')

        self.frame = tk.Frame(borderwidth=2,relief=tk.GROOVE)
    
        row,col=self.get_grid_position()
        
        widest_widget_width=0
        for item in self.window.grid_slaves(column=col):
            item_width = item.winfo_width()
            if item_width > widest_widget_width:
                widest_widget_width=item_width
        
        self.window.columnconfigure(col,minsize=widest_widget_width)
        #print(widest_widget_width)

        self.frame.grid(in_=self.window,row=row,column=col,sticky=tk.NSEW)

        
        self.sidebar_frame=tk.Frame()
        self.sidebar_frame.grid(in_=self.frame,row=0,column=0,ipadx=10,ipady=10,padx=10,pady=10,sticky=tk.S)
        #self.sidebar_frame.pack(in_=self.frame,fill=tk.BOTH,side=tk.LEFT)
        
        self.data_frame=tk.Frame()
        self.data_frame.grid(in_=self.frame,row=0,column=1,ipadx=10,ipady=10,padx=10,pady=10,sticky=tk.S)
        #self.data_frame.pack(in_=self.frame,side=tk.LEFT,fill=tk.BOTH)
        
        self.create_sidebar()
        self.create_text_areas()
        
        self.frame.after(self.data_refresh_rate,self.refresh_data) #after data_refresh_rate ms it will run refresh_data, which calls itself. again and again. 
        
    
    def get_grid_position(self):
        self.window.update() #if don't do this winfo_height doesn't return correct value

        screen_height = self.window.winfo_screenheight()
        
        ncols,nrows = self.window.grid_size()

        col = ncols-1
        colheight=0
        if(ncols==0): col=0 # if don't have any columns yet, start one
        else:
            for item in self.window.grid_slaves(column=col):
                colheight+=item.winfo_height()
            
        if (screen_height-colheight<400): # if height of column is within 400px of screen height...
            col+=1 #make new column
            
        row = len(self.window.grid_slaves(column=col))
        return row,col
    
    def handle_log_folder_clicked(self):
        self.save_folder.set(filedialog.askdirectory(initialdir=os.getcwd(),title = "Select folder"))


    def create_sidebar(self):
        topic_label = tk.Label(self.sidebar_frame,text="%i: %s"%(self.port,self.topic),font=('Arial',16))
        topic_label.pack(in_=self.sidebar_frame,anchor=tk.W)
        
        
        
        
        options_frame = tk.Frame(self.sidebar_frame)
        options_frame.pack(in_=self.sidebar_frame,fill=None,expand=False,anchor=tk.W)
        options_frame.grid_propagation=False
        
        tk.Checkbutton(self.sidebar_frame,text="Log data?",var=self.save_state).grid(in_=options_frame,row=0,column=0)
        tk.Button(options_frame,text="Change log folder",command=self.handle_log_folder_clicked).grid(in_=options_frame,row=0,column=1,pady=5,padx=5)

        
        # Log data
        tk.Label(options_frame,text="Log folder:").grid(in_=options_frame,row=1,column=0,pady=5,padx=5)

        save_folder_message = tk.Entry(options_frame,textvariable=self.save_folder,state='readonly')
        save_folder_message.grid(in_=options_frame,row=1,column=1,sticky=tk.W)
        
        
        #Last received:
        tk.Label(options_frame,text="Last received:").grid(in_=options_frame,row=2,column=0,pady=5,padx=5)
        
        self.last_received=tk.StringVar()
        self.last_received.set('Never')
        self.last_received_message = tk.Entry(options_frame,textvariable=self.last_received,state='readonly')
        self.last_received_message.grid(in_=options_frame,row=2,column=1,sticky=tk.W)

    
    def create_text_areas(self):
        self.data_list=[]
        for i in range(self.num_items):
            tk.Label(self.data_frame,text=self.labels[i],width=20).grid(in_=self.data_frame,column=0,row=i+2)
            self.data_list.append(tk.StringVar())
            
            tk.Entry(self.data_frame,textvariable=self.data_list[i],state='readonly',readonlybackground='white').grid(in_=self.data_frame,column=1,row=i+2)

    def save_data(self,data):
        new_line=''
        for item in data:
            if(isinstance(item,float) or isinstance(item,int)):
                item = float(item)
            new_line+=str(item)+','
        new_line = new_line[:-1] #remove trailing comma
        
        now = datetime.fromtimestamp(time.time())
        fname = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+'.txt'
        os.chdir(self.save_folder.get())
        if not os.path.isfile(fname): 
            filepath = os.path.join(fname)
            print('created file '+fname)
        else: filepath = fname
        fp = open(filepath, 'a+')
        fp.write(new_line+'\n')
        fp.close()
        #print('saved data '+data+' to '+fname)
    
    def refresh_data(self):
        try:        
            
            new_data = self.grabber.grabData()
            if(new_data is not ''):
                
                if isinstance(new_data,bytes): new_data = new_data.decode().split(',')
                else: new_data = new_data.split(',')
                
                datetime_object = datetime.fromtimestamp(float(new_data[1])) #convert the float unix time to a datetime object
                readable_time = str(datetime_object.strftime("%m/%d/%Y, %H:%M:%S"))
                self.last_received_message.configure(fg='green')
                self.last_received.set(readable_time) #updates the text in the time field
                

                
    
                for i in range(self.num_items):
                    val = new_data[i+2] #start from the third value - the first two are topic and time
                    try:
                        val = float(val)
                        self.data_list[i].set("%.3f"%(val))
                    except:
                        self.data_list[i].set("%s"%(val))
    
                if(self.save_state.get()): #optional saving of data - .get() is tkinter way of checking the bool value                
                    #new_line = str(new_data[1:]).strip('(').strip(')')
                    #self.save_data(new_line)
                    self.save_data(new_data)
                    
                #self.last_received_message.update()
                #self.last_received_message.configure(fg='black')
            else:
                self.last_received_message.configure(fg='black')
        except Exception as e:
            print(e) #useful for debugging
            pass
        
        self.frame.after(self.data_refresh_rate,self.refresh_data)
            
