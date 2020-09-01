'''Using some nlogn sweepline algorithm to create a diagram based on input points by the used.
Ideally this algorithm will let the user either randomly generate the points or place them themselves.
Also allow the user to select manhattan or euclidean distance.'''
from tkinter import *
from random import randrange

class Point():
    def __init__(self,canvas=None,x=0,y=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.circle = self.canvas.create_oval(x-2,y-2,x+2,y+2,fill="black")

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master#root
        self.points = []#A list of Point objects
        self.w_width = master.winfo_screenwidth()#Window width
        self.w_height = master.winfo_screenheight()-100#Window height
        self.master.geometry(str(self.w_width)+"x"+str(self.w_height)+"+0+0")
        #self.pack_propagate(0)
        self.create_widgets()


    #Creates the widgets that will be in the application at start
    def create_widgets(self):
        #Creates the canvas on which the town will be drawn
        self.c_width = int(.8*self.w_width)
        self.c_height = int(.98*self.w_height)
        self.canvas = Canvas(self.master,bg="red",width = self.c_width,height = self.c_height)
        self.canvas.place(relx =0.01,rely=0.01)

        #Field for number of points to be generated
        self.set_point_number = Spinbox(self.master,values=(3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,100),state="readonly")
        self.set_point_number.place(relx=.85,rely=.15)

        #Button to randomly generate points
        self.random = Button(self.master,text = "Randomly Generate points",command = self.generate_points)
        self.random.place(relx = .85,rely=.1)

        #Button to clear points
        self.clear = Button(self.master,text="Clear points",command = self.clear_points)
        self.clear.place(relx=.85,rely=.05)

        #Field to select distance type
        self.distance_type = "Euclidean"
        self.set_distance_type = Spinbox(self.master,values=("Euclidean","Manhattan"),state="readonly",wrap=True)
        self.set_distance_type.place(relx=.85,rely=.2)

        #Button to generate city
        self.generate = Button(self.master,text = "Generate city based on points",command = self.generate_city)
        self.generate.place(relx=.85,rely=.25)

    def clear_points(self):
        for i in self.points:
            self.canvas.delete(i.circle)
        self.points = []

    def generate_points(self):
        self.clear_points()
        for i in range(0,int(self.set_point_number.get())):
            self.points.append(Point(self.canvas,randrange(1,self.c_width),randrange(1,self.c_height)))
    
    def generate_city(self):
        print("Too be implemented")

root = Tk()

app = Application(master=root)
app.mainloop()