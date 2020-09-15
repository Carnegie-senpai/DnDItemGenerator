from tkinter import *
from random import randrange
from math import sqrt
#Classes used during city generation
class Point():
    def __init__(self,canvas=None,x=0,y=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.circle = self.canvas.create_oval(x-2,y-2,x+2,y+2,fill="black")

'''BeachFront keeps track of the arcs which make up the beachfront. 
Functionally it is a binary search tree in which:
    the internal nodes define the breakpoints between the arcs
    the leaf nodes define the arcs
Is not a BBST. May change to ensure O(logn) query'''
class BeachFront():
    class Node():
        #data changes depending on if it is an internal or leaf node
        def __init__(self,data,left=None,right=None,parent=None):
            self.data = data
            self.left = left
            self.right = right
            self.parent = parent
    
    def __init__(self,node=Node(None)):
        self.root = node

    '''Searches for value within Beachfront, returns either the node which contains the 
    value searched for or returns None'''
#    def find(value):
#        loc = self.root
#        while (loc != None):
#            if (value < loc.data):
#                loc = loc.left
#            elif (value > loc.data):
#                loc = loc.right
#            else:
#                break
#        return loc



#Code for vornoi diagram generation
'''Calculates the y coordinate of the parabola for a given x coordinate, focus, and directrix
    xf,yf == coordinates of the focus
    yd == directrix line
    O(1)'''
def parabola_y(x,xf,yf,yd):
    return ( ( (x-xf)**2 ) / (2 * (yf-yd)) ) + ( (yf+yd)/2 )

'''Calculates the intersection of two parabolas given their focus points and a diretrix line
    x1,y1 == parabola 1's focus (x,y)
    x2,y2 == parabola 2's focus (x,y)
    yd == directrix line
    returns the x coordinate of the intersection of the two parabolas
    '''
def parabola_intersection(x1,y1,x2,y2,yd):
    a = (y1-yd) - (y2-yd)
    b = (-2 * x2 * (y1-yd)) - (-2 * x1 * (y2-yd))
    c = ((x2**2)*(y1-yd)) - ((x1**2)*(y2-yd)) + ((y2-yd)*(y1-yd)*(y2-y1))
    print("a = {}".format(a))
    print("b = {}".format(b))
    print("c = {}".format(c))

    s = b**2 - 4*a*c
    try:
        result_x1 = (-b + sqrt(s))/(2*a)
    except ZeroDivisionError:
        result_x1 = -100000
    try:
        result_x2 = (-b - sqrt(s))/(2*a)
    except ZeroDivisionError:
        result_x2 = -100000
    if ((x1 < result_x1 < x2) or (x2 < result_x1 < x1) ):
        return result_x1
    return result_x2

def handle_site_event(site):
    print("Handling Site Event")

def handle_edge_event(edge):
    print("Handling Edge Event")

''' Using fortune's algorithm to generate the voronoi graph
    O(nlogn)'''
def generate_voronoi(points):
    events = sorted(points,key = lambda x: x.x)   #ordered queue of site events
    while events != []:
        event = events.pop(0)
        if type(event) == Point:    #Site event
            handle_site_event(event)
        else:                       #Edge event
            handle_edge_event(event)
    #bound voronoi diagram's unclosed cells around perimeter


#Code for the UI
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
        self.set_distance_type = Spinbox(self.master,values=("Euclidean","Manhattan","Minkowski"),state="readonly",wrap=True)
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
        generate_voronoi(self.points)
        x = parabola_intersection(25,100,36,200,300)
        print(parabola_y(x,25,100,300))
        print(parabola_y(x,36,200,300))
        print("Too be implemented")


root = Tk()

app = Application(master=root)
app.mainloop()