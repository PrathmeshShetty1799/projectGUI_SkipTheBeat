'''
SFWRENG/COE 3K04 - Software Development - Device Control Monitor
Developed By Skip the Beat

Juan D. Molina Calderón - molinacj@mcmaster.ca - 400145924
Jack Wawrychuk - wawrychj@mcmaster.ca - 400145293
Nafia Naowar - naowarn@mcmaster.ca -  400129601
Prathmesh Shetty - shettp1@mcmaster.ca - 400130037

This program is our way of handling all of the programmmble modes of the PACEMAKER and allow the physician to change within these specific modes
'''

#Import Statements 
#We are using Python's Tkinter Module to develop the GUI 
import tkinter as tk
from tkinter import ttk

#We are using Python's pySerial to communicate with the Shield/Board
#import serial
import struct

#We are using pickle to encode and decode all of the necessary data to add a bit of security to the data of the patients
import pickle
import types

#Private Variables - These variables are the few that are used everywhere in the program and have a significant value at every stage

#GUI
LARGE_FONT = ("Times", 12)

#User Data
currentUser = 1 #Indicates the current user of the DCM, is only changed when the setCurrentUser() function is used

#Necessary Files for the Encoding of the Data
PIK = "DONOTTOUCHTHIS.dat"

#Update UserData Dictionary
pickle_in = open(PIK,"rb")
userData = pickle.load(pickle_in) #Only Changed when updateData() is used


#Serial Communication Setup Variables
#try:
   # ser = serial.Serial(
    #port='COM7',
   # baudrate = 115200,
   # parity=serial.PARITY_NONE,
   # stopbits=serial.STOPBITS_ONE,
   # bytesize=serial.EIGHTBITS,
    #timeout=1)

#except:
    #print("Serial Communication Not Established")

#Private Functions - These functions are used to support the program with information transfer within the module
'''
@function: updateData() - Updates the Stored Data from the Dictionary that stores user info into the external pickle file
@param - None
@return - None
'''

def updateData():
    #Uses Pickle Commands to Open and Store New Data
    pickle_out = open(PIK,"wb")
    pickle.dump(userData, pickle_out)
    pickle_out.close()

'''
@function: setCurrentUser(s) - Sets the current user when the user is logged in
@param - int userNumber
@return - None
'''
def setCurrentUser(userNumber):
   global currentUser
   currentUser = userNumber

'''
@function: getCurrentUser(s) - Gets the current user of the user who is logged in
@param - None
@return - Returns the Current User Number between 1-10
'''
def getCurrentUser():
    return currentUser

'''
@function: addUser(s) - Adds a new user to the database(dictionary) 
@param - controller - Helps Control the Tkinter Frames, Str username - Username of the new user, Str password - Password of the new user
@return - None
'''
def addUser(controller,username, password):

    #Checks for any empty input
    if(len(username) == 0 or len(password)==0):
        controller.show_frame(WelcomeScreenWithInvalidUser)
    
    else:
        #Checks for if maximum number of users are already part of the system
        if(userData[10]['taken']==True):
            controller.show_frame(WelcomeScreenWithMaximumUsers)

        else:
            #Checks for a unique username
            if(checkUniqueUsername(username)==True):
                #Updates the database if the username is unique
                for x in range(1,11):
                    if((userData[x]['taken'])==False):
                        userData[x]['username'] = username 
                        userData[x]['password'] =password
                        userData[x]['taken'] = True
                        updateData()
                        controller.show_frame(WelcomeScreenWithUserAdded)
                        print("User Added")
                        break
            # Has a Message for the User telling about username taken
            else:
                controller.show_frame(WelcomeScreenWithAlreadyAdded)

'''
@function: checkUniqueUsername(s) - Checks if the username is unique
@param -  Str username - Username of the user that is to be checked
@return - Returns True if Unique, False Otherwise
'''
def checkUniqueUsername(username):
    #Goes through the database and checks usernames that are already taken
    for x in range(1,11):
        if(userData[x]['username'] == username):
            return False
    
    return True
        
'''
@function: checkUser(s) - Checks for an existing user in the database(dictionary) 
@param - controller - Helps Control the Tkinter Frames, Str username - Username of the new user, Str password - Password of the new user
@return - None
'''                  
def checkUser(controller,username, password):
    #Checks the database when a user logs in
    for x in range(1,11):
        if((userData[x]['username'] == username) and (userData[x]['password']==password)):
            setCurrentUser(x)
            print("User Checked")
            controller.show_frame(MainPage)
            break
        #If the user is not in the database, an invalid user text appears on the screen
        controller.show_frame(WelcomeScreenWithInvalidUser) #Change the Screen to Invalid input

'''
@function: makeList(s) - Takes in the input and makes a list of the variables 
@param - data - Data that needs to be made into a list
@return - List made of the input variables
''' 
def makeList(data):
    transList = [0]*len(data)
    count = 0
    while(count < len(data)):
        transList[count] = data[count]
        count +=1 
    return transList
#Tkinter Frames Dealing With the Welcome Screen

'''
@class: projectGUI(tk.Tk) - Setups the GUI as Tkinter Frames and uses Tkinter Module in order to display the different screens
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class projectGUI(tk.Tk):

    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, *args, **kwargs
    @return - None
    '''    
    def __init__(self, *args, **kwargs):

        #Setups an instance of Tkinter
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        #Setups Custom Values and Geometry of the Screen
        tk.Tk.wm_title(self, "Skip the Beat")
        container.pack(side = "top", fill = "both", expand =True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        #Setting Up the Frames - Screens to Transistions between
        self.frames = {} # Stores all the frames

        for F in (WelcomeScreen, WelcomeScreenWithInvalidUser, WelcomeScreenWithMaximumUsers,WelcomeScreenWithAlreadyAdded,WelcomeScreenWithUserAdded, MainPage,
                    AOOScreen, AOOScreenInvalidLRL, AOOScreenInvalidURL, AOOScreenInvalidAAmp,AOOScreenInvalidAPW,
                    AAIScreen, AAIScreenInvalidLRL, AAIScreenInvalidURL, AAIScreenInvalidAAmp, AAIScreenInvalidAPW, AAIScreenInvalidASens, AAIScreenInvalidARP, 
                    VOOScreen, VOOScreenInvalidLRL, VOOScreenInvalidURL, VOOScreenInvalidVAmp,VOOScreenInvalidVPW,
                    VVIScreen, VVIScreenInvalidLRL, VVIScreenInvalidURL, VVIScreenInvalidVAmp, VVIScreenInvalidVPW, VVIScreenInvalidVSens, VVIScreenInvalidVRP,
                    DOOScreen, DOOScreenInvalidLRL, DOOScreenInvalidURL, DOOScreenInvalidVAmp, DOOScreenInvalidVPW, DOOScreenInvalidAAmp, DOOScreenInvalidAPW, 
                    AOORScreen, AOORScreenInvalidLRL, AOORScreenInvalidURL, AOORScreenInvalidAAmp, AOORScreenInvalidAPW, AOORScreenInvalidMSR, AOORScreenInvalidActThres, AOORScreenInvalidReactTime, AOORScreenInvalidResponseFac, AOORScreenInvalidRecovTime
                    ,VOORScreen, VOORScreenInvalidLRL, VOORScreenInvalidURL, VOORScreenInvalidVAmp, VOORScreenInvalidVPW, VOORScreenInvalidMSR, VOORScreenInvalidActThres, VOORScreenInvalidReactTime, VOORScreenInvalidResponseFac, VOORScreenInvalidRecovTime
                    ,AAIRScreen, AAIRScreenInvalidLRL, AAIRScreenInvalidURL, AAIRScreenInvalidAAmp, AAIRScreenInvalidAPW, AAIRScreenInvalidASens, AAIRScreenInvalidARP ,AAIRScreenInvalidMSR, AAIRScreenInvalidActThres, AAIRScreenInvalidReactTime, AAIRScreenInvalidResponseFac, AAIRScreenInvalidRecovTime
                    ,VVIRScreen, VVIRScreenInvalidLRL, VVIRScreenInvalidURL, VVIRScreenInvalidVAmp, VVIRScreenInvalidVPW, VVIRScreenInvalidVSens, VVIRScreenInvalidVRP ,VVIRScreenInvalidMSR, VVIRScreenInvalidActThres, VVIRScreenInvalidReactTime, VVIRScreenInvalidResponseFac, VVIRScreenInvalidRecovTime
                    ,DOORScreen, DOORScreenInvalidLRL, DOORScreenInvalidURL, DOORScreenInvalidAAmp, DOORScreenInvalidAPW, DOORScreenInvalidAAmp, DOORScreenInvalidVAmp,DOORScreenInvalidFixedAVDelay, DOORScreenInvalidMSR,DOORScreenInvalidActThres, DOORScreenInvalidReactTime, DOORScreenInvalidResponseFac, DOORScreenInvalidRecovTime
                    ,DDDRScreen, DDDRScreenInvalidLRL, DDDRScreenInvalidURL, DDDRScreenInvalidAAmp, DDDRScreenInvalidAPW, DOORScreenInvalidAAmp, DDDRScreenInvalidVAmp,DDDRScreenInvalidFixedAVDelay, DDDRScreenInvalidMSR,DDDRScreenInvalidActThres, DDDRScreenInvalidReactTime, DDDRScreenInvalidResponseFac, DDDRScreenInvalidRecovTime,DDDRScreenInvalidDynamicAVDelay, DDDRScreenInvalidPVARP):

            frame = F(container, self)
            self.frames[F] = frame #sets the welcomeScreen as the first frame to show
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(WelcomeScreen)

    '''
    @function: show_frame() - Transistions between the different frame by bring them up to the top
    @param -self, cont - Container of all the possible frames
    @return - None
    '''    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

'''
@class: WelcomeScreen(tk.Tk) - Tkinter Frame of the Welcome Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class WelcomeScreen(tk.Frame):

    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):
        #Setting Up The Interactive Options such as Texts, Buttons and Entry Boxes

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to Skip The Beat", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 0, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                                 ", font = LARGE_FONT)
        label.grid(row = 7, column = 0, padx=10, pady=10)

        #Entry Boxes
        label=ttk.Label(self, text="Username",font=LARGE_FONT)
        label.grid(row=1, column = 2, padx=10, pady=10)
        userBox = ttk.Entry(self)
        userBox.grid(row = 2, column=2, padx=10, pady=10)
    
        label=ttk.Label(self, text="Password", font=LARGE_FONT)
        label.grid(row=4, column = 2, padx=10, pady=10)
        passBox = ttk.Entry(self)
        passBox.grid(row=5, column=2, padx=10, pady=10)
        
        #Buttons
        addUserBox = ttk.Button(self, text = "Add User", command =lambda:[f() for f in [addUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        addUserBox.grid(row = 7,column = 1, padx=10, pady=10)

        closeBox = ttk.Button(self, text = "Close", command = quit)
        closeBox.grid(row = 7,column = 2, padx=10, pady=10)

        signInBox = ttk.Button(self, text = "Sign In", command = lambda:[f() for f in [checkUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        signInBox.grid(row = 7,column =3, padx=10, pady=10)

'''
@class: WelcomeScreenWithInvalidUser(tk.Tk) - Tkinter Frame of the Welcome Screen with the "Invalid User" text
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class WelcomeScreenWithInvalidUser(tk.Frame):

    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''    
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to Skip The Beat", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid User - Try Again",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 4, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 0, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                                 ", font = LARGE_FONT)
        label.grid(row = 7, column = 0, padx=10, pady=10)

        #Entry Boxes
        label=ttk.Label(self, text="Username",font=LARGE_FONT)
        label.grid(row=1, column = 2, padx=10, pady=10)
        userBox = ttk.Entry(self)
        userBox.grid(row = 2, column=2, padx=10, pady=10)
    
        label=ttk.Label(self, text="Password", font=LARGE_FONT)
        label.grid(row=4, column = 2, padx=10, pady=10)
        passBox = ttk.Entry(self)
        passBox.grid(row=5, column=2, padx=10, pady=10)
        
        #Buttons
        addUserBox = ttk.Button(self, text = "Add User", command =lambda:[f() for f in [addUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        addUserBox.grid(row = 7,column = 1, padx=10, pady=10)

        closeBox = ttk.Button(self, text = "Close", command = quit)
        closeBox.grid(row = 7,column = 2, padx=10, pady=10)

        signInBox = ttk.Button(self, text = "Sign In", command = lambda:[f() for f in [checkUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        signInBox.grid(row = 7,column =3, padx=10, pady=10)

'''
@class: WelcomeScreenWithMaximumUsers(tk.Tk) - Tkinter Frame of the Welcome Screen with the "Maximums Users" text
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class WelcomeScreenWithMaximumUsers(tk.Frame):
    
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to Skip The Beat", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        label = tk.Label(self, text = "Maximum Users Added",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 4, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 0, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                                 ", font = LARGE_FONT)
        label.grid(row = 7, column = 0, padx=10, pady=10)

        #Entry Boxes
        label=ttk.Label(self, text="Username",font=LARGE_FONT)
        label.grid(row=1, column = 2, padx=10, pady=10)
        userBox = ttk.Entry(self)
        userBox.grid(row = 2, column=2, padx=10, pady=10)
    
        label=ttk.Label(self, text="Password", font=LARGE_FONT)
        label.grid(row=4, column = 2, padx=10, pady=10)
        passBox = ttk.Entry(self)
        passBox.grid(row=5, column=2, padx=10, pady=10)
        
        #Buttons
        addUserBox = ttk.Button(self, text = "Add User", command =lambda:[f() for f in [addUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        addUserBox.grid(row = 7,column = 1, padx=10, pady=10)

        closeBox = ttk.Button(self, text = "Close", command = quit)
        closeBox.grid(row = 7,column = 2, padx=10, pady=10)

        signInBox = ttk.Button(self, text = "Sign In", command = lambda:[f() for f in [checkUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        signInBox.grid(row = 7,column =3, padx=10, pady=10)

'''
@class: WelcomeScreenWithAlreadyAdded(tk.Tk) - Tkinter Frame of the Welcome Screen with the "User Already Added" text
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class WelcomeScreenWithAlreadyAdded(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to Skip The Beat", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        label = tk.Label(self, text = "User Already Added",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 4, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 0, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                                 ", font = LARGE_FONT)
        label.grid(row = 7, column = 0, padx=10, pady=10)

        #Entry Boxes
        label=ttk.Label(self, text="Username",font=LARGE_FONT)
        label.grid(row=1, column = 2, padx=10, pady=10)
        userBox = ttk.Entry(self)
        userBox.grid(row = 2, column=2, padx=10, pady=10)
    
        label=ttk.Label(self, text="Password", font=LARGE_FONT)
        label.grid(row=4, column = 2, padx=10, pady=10)
        passBox = ttk.Entry(self)
        passBox.grid(row=5, column=2, padx=10, pady=10)
        
        #Buttons
        addUserBox = ttk.Button(self, text = "Add User", command =lambda:[f() for f in [addUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        addUserBox.grid(row = 7,column = 1, padx=10, pady=10)

        closeBox = ttk.Button(self, text = "Close", command = quit)
        closeBox.grid(row = 7,column = 2, padx=10, pady=10)

        signInBox = ttk.Button(self, text = "Sign In", command = lambda:[f() for f in [checkUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        signInBox.grid(row = 7,column =3, padx=10, pady=10)

'''
@class: WelcomeScreenWithAlreadyAdded(tk.Tk) - Tkinter Frame of the Welcome Screen with the "User Already Added" text
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class WelcomeScreenWithUserAdded(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Welcome to Skip The Beat", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        label = tk.Label(self, text = "User Added",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 4, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 0, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                  ", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10, pady=10)

        label = tk.Label(self, text = "                                 ", font = LARGE_FONT)
        label.grid(row = 7, column = 0, padx=10, pady=10)

        #Entry Boxes
        label=ttk.Label(self, text="Username",font=LARGE_FONT)
        label.grid(row=1, column = 2, padx=10, pady=10)
        userBox = ttk.Entry(self)
        userBox.grid(row = 2, column=2, padx=10, pady=10)
    
        label=ttk.Label(self, text="Password", font=LARGE_FONT)
        label.grid(row=4, column = 2, padx=10, pady=10)
        passBox = ttk.Entry(self)
        passBox.grid(row=5, column=2, padx=10, pady=10)
        
        #Buttons
        addUserBox = ttk.Button(self, text = "Add User", command =lambda:[f() for f in [addUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        addUserBox.grid(row = 7,column = 1, padx=10, pady=10)

        closeBox = ttk.Button(self, text = "Close", command = quit)
        closeBox.grid(row = 7,column = 2, padx=10, pady=10)

        signInBox = ttk.Button(self, text = "Sign In", command = lambda:[f() for f in [checkUser(controller,userBox.get(),passBox.get()),userBox.delete(0,100),passBox.delete(0,100)]])
        signInBox.grid(row = 7,column =3, padx=10, pady=10)


#Private Functions - Used to update information of specific PACEMAKER modes
'''
@function: updateAOO - Updates all the parameter values for the AOO Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width
@return - None
''' 
def updateAOO(controller, user, lowerRate, upperRate, atrialAmp, atrialPulseWidth):

    #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(AOOScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(AOOScreenInvalidURL)

        else:
            if(len(atrialAmp) == 0):
                controller.show_frame(AOOScreenInvalidAAmp)

            else:
                if(len(atrialPulseWidth) == 0):
                    controller.show_frame(AOOScreenInvalidAPW)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['aoo']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['aoo']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                            userData[user]['aoo']['atrialAmp'] = float(atrialAmp) 
                            try:
                                if((float(atrialPulseWidth) == 0.05)or(float(atrialPulseWidth)%0.1 == 0.0 and float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                    userData[user]['aoo']['atrialPulseWidth'] = float(atrialPulseWidth)
                                    updateData()# Updates the Local Copy
                                    # Sends the Data to Board (Serial Comm)

                                    try:
                                        #PySerial Sending the Values to the Board as a byte array
                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                            ser.open()

                                        valuesList = [16,55,2]
                                        values = bytearray(valuesList)
                                        ser.write(values)

                                    except:
                                        print("Serial Communication Not Established")

                                    """
                                    #PySerial Sending the Values to the Board as a Struct Pack
                                    if(ser.is_open==False): #Open Serial Port if already not opened
                                        ser.open()

                                    values = struct.pack("<BBBiiiiiiiidiiii",16,55,1,int(lowerRate),int(upperRate),0,200,float(atrialAmp)*1000,int(atrialPulseWidth),0,0,0.0,0,0,0)
                                    valuesList = makeList(values)
                                    print(valuesList)
                                    print(type(valuesList))
                                    ser.write(values)

                                    ser.close()
                                    """
                                    print("User AOO Updated")
                                    print(userData)
                                    #If the inputs are correct
                                    controller.show_frame(MainPage)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(AOOScreenInvalidAPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(AOOScreenInvalidAAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(AOOScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(AOOScreenInvalidLRL)

'''
@function: updateVOO - Updates all the parameter values for the VOO Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width
@return - None
'''
def updateVOO(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth):

  #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(VOOScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(VOOScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(VOOScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(VOOScreenInvalidVPW)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['voo']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['voo']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['voo']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if((float(ventriPulseWidth)==0.05)or(float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['voo']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    updateData()# Updates the Local Copy
                                    # Sends the Data to Board (Serial Comm)
                                    
                                    try:
                                        #PySerial Sending the Values to the Board as a byte array
                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                            ser.open()

                                        valuesList = [16,55,1]
                                        values = bytearray(valuesList)
                                        ser.write(values)
                                    except:
                                        print("Serial Communication Not Established")
                                
                                    print("User VOO Updated")
                                    print(userData)
                                    #If the inputs are correct
                                    controller.show_frame(MainPage)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(VOOScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(VOOScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(VOOScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(VOOScreenInvalidLRL)
    
'''
@function: updateAAI - Updates all the parameter values for the AAI Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width, atrialSensitivity - Atrial Sensitivity, aRP - ARP
@return - None
'''
def updateAAI(controller, user, lowerRate, upperRate, atrialAmp, atrialPulseWidth, atrialSensitivity, aRP):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(AAIScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(AAIScreenInvalidURL)
        else:
            if(len(atrialAmp) == 0):
                controller.show_frame(AAIScreenInvalidAAmp)
            else:
                if(len(atrialPulseWidth) == 0):
                    controller.show_frame(AAIScreenInvalidAPW)
                else:
                    if(len(atrialSensitivity) == 0):
                        controller.show_frame(AAIScreenInvalidASens)
                    else:
                        if(len(aRP) == 0):
                            controller.show_frame(AAIScreenInvalidARP)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['aai']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['aai']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                            userData[user]['aai']['atrialAmp'] = float(atrialAmp) 
                            try:
                                if(float(atrialPulseWidth)==0.05 or(float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                    userData[user]['aai']['atrialPulseWidth'] = float(atrialPulseWidth)
                                    try:
                                        if((float(atrialSensitivity)%0.25 == 0.0 and float(atrialSensitivity)>=0.25 and float(atrialSensitivity)<=0.75)or(float(atrialSensitivity)%0.5 == 0.0 and float(atrialSensitivity)>=1.0 and float(atrialSensitivity)<=10.0)):
                                            userData[user]['aai']['atrialSensitivity'] = float(atrialSensitivity)
                                            try:
                                                if(int(aRP)%10== 0 and int(aRP)>=150 and int(aRP)<=500):
                                                    userData[user]['aai']['ARP'] = int(aRP)
                                                    updateData()# Updates the Local Copy
                                                    
                                                    #PySerial Sending the Values to the Board as a byte array
                                                    try:
                                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                                            ser.open()

                                                        valuesList = [16,55,4]
                                                        values = bytearray(valuesList)
                                                        ser.write(values)
                                                    except:
                                                        print("Serial Communication Not Established")
                                                    
                                                    print("User AAI Updated")
                                                    print(userData)
                                                    #If the inputs are correct
                                                    controller.show_frame(MainPage)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(AAIScreenInvalidARP)
                                        else:
                                            raise ValueError
                                    except:
                                        controller.show_frame(AAIScreenInvalidASens)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(AAIScreenInvalidAPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(AAIScreenInvalidAAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(AAIScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(AAIScreenInvalidLRL)

'''
@function: updateVVI - Updates all the parameter values for the VVI Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, ventriSensitivity - Ventri Sensitivity, vRP - VRP
@return - None
'''
def updateVVI(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, ventriSensitivity, VRP):
    
 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(VVIScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(VVIScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(VVIScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(VVIScreenInvalidVPW)
                else:
                    if(len(ventriSensitivity) == 0):
                        controller.show_frame(VVIScreenInvalidVSens)
                    else:
                        if(len(VRP) == 0):
                            controller.show_frame(VVIScreenInvalidVRP)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['vvi']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['vvi']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['vvi']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if((float(ventriPulseWidth)==0.05)or(float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['vvi']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if((float(ventriSensitivity)%0.25 == 0.0 and float(ventriSensitivity)>=0.25 and float(ventriSensitivity)<=0.75)or(float(ventriSensitivity)%0.5 == 0.0 and float(ventriSensitivity)>=1.0 and float(ventriSensitivity)<=10.0)):
                                            userData[user]['vvi']['ventriSensitivity'] = float(ventriSensitivity)
                                            try:
                                                if(int(VRP)%10== 0 and int(VRP)>=150 and int(VRP)<=500):
                                                    userData[user]['vvi']['VRP'] = int(vRP)
                                                    updateData()# Updates the Local Copy
                                                    # Sends the Data to Board (Serial Comm)

                                                    try:
                                                        #PySerial Sending the Values to the Board as a byte array
                                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                                            ser.open()

                                                        valuesList = [16,55,3]
                                                        values = bytearray(valuesList)
                                                        ser.write(values)
                                                    except:
                                                        print("Serial Communication Not Established")
                                                    
                                                    print("User VVI Updated")
                                                    print(userData)
                                                    #If the inputs are correct
                                                    controller.show_frame(MainPage)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(VVIScreenInvalidVRP)
                                        else:
                                            raise ValueError
                                    except:
                                        controller.show_frame(VVIScreenInvalidVSens)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(VVIScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(VVIScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(VVIScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(VVIScreenInvalidLRL)

'''
@function: updateDOO - Updates all the parameter values for the DOO Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width
@return - None
'''
def updateDOO(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, atrialAmp, atrialPulseWidth):
    
 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(DOOScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(DOOScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(DOOScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(DOOScreenInvalidVPW)
                else:
                    if(len(atrialAmp) == 0):
                        controller.show_frame(DOOScreenInvalidAAmp)
                    else:
                        if(len(atrialPulseWidth) == 0):
                            controller.show_frame(DOOScreenInvalidAPW)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['doo']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['doo']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['doo']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if(float(ventriPulseWidth)==0.05 or(float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['doo']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                                            userData[user]['doo']['atrialAmp'] = float(atrialAmp) 
                                            try:
                                                if(float(atrialPulseWidth)==0.0 or(float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                                    userData[user]['doo']['atrialPulseWidth'] = float(atrialPulseWidth)
                                                    updateData()# Updates the Local Copy
                                                    # Sends the Data to Board (Serial Comm)
                                                    try:
                                                        #PySerial Sending the Values to the Board as a byte array
                                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                                            ser.open()

                                                        valuesList = [16,55,5]
                                                        values = bytearray(valuesList)
                                                        ser.write(values)
                                                    except:
                                                        print("Serial Communication Not Established")

                                                    
                                                    print("User DOO Updated")
                                                    print(userData)
                                                    #If the inputs are correct
                                                    controller.show_frame(MainPage)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(DOOScreenInvalidAPW)
                                        else:
                                            raise ValueError
                                    except:
                                        controller.show_frame(DOOScreenInvalidAAmp)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(DOOScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(DOOScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(DOOScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(DOOScreenInvalidLRL)

'''
@function: updateAOOR - Updates all the parameter values for the AOOR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time
                    
@return - None
'''
def updateAOOR(controller, user, lowerRate, upperRate, atrialAmp, atrialPulseWidth, mSR, actThres, reactTime, responseFac, recovTime):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(AOORScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(AOORScreenInvalidURL)
        else:
            if(len(atrialAmp) == 0):
                controller.show_frame(AOORScreenInvalidAAmp)
            else:
                if(len(atrialPulseWidth) == 0):
                    controller.show_frame(AOORScreenInvalidAPW)
                else:
                    if(len(mSR) == 0):
                        controller.show_frame(AOORScreenInvalidMSR)
                    else:
                        if(len(actThres) == 0):
                            controller.show_frame(AOORScreenInvalidActThres)
                        else:
                            if(len(reactTime) == 0):
                                controller.show_frame(AOORScreenInvalidReactTime)
                            else:
                                if(len(responseFac) == 0):
                                    controller.show_frame(AOORScreenInvalidResponseFac)    
                                else:
                                    if(len(recovTime) == 0):
                                        controller.show_frame(AOORScreenInvalidRecovTime)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['aoor']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['aoor']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                            userData[user]['aoor']['atrialAmp'] = float(atrialAmp) 
                            try:
                                if(float(atrialPulseWidth)==0.05 or(float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                    userData[user]['aoor']['atrialPulseWidth'] = float(atrialPulseWidth)
                                    try:
                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                            userData[user]['aoor']['maximumSensRate'] = int(mSR)
                                            try:
                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                    userData[user]['aoor']['activityThres'] = actThres
                                                    try:
                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                            userData[user]['aoor']['reactTime'] = int(reactTime)
                                                            try:
                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                    userData[user]['aoor']['responseFac'] = int(responseFac)
                                                                    try:
                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                            userData[user]['aoor']['recovTime'] = int(recovTime)
                                                                            updateData()# Updates the Local Copy
                                                                            # Sends the Data to Board (Serial Comm)

                                                                            try:
                                                                                #PySerial Sending the Values to the Board as a byte array
                                                                                if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                    ser.open()

                                                                                valuesList = [16,55,7]
                                                                                values = bytearray(valuesList)
                                                                                ser.write(values)

                                                                            except:
                                                                                print("Serial Communication Not Established")

                                                                            print("User AOOR Updated")
                                                                            print(userData)
                                                                            #If the inputs are correct
                                                                            controller.show_frame(MainPage)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(AOORScreenInvalidRecovTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(AOORScreenInvalidResponseFac)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(AOORScreenInvalidReactTime)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(AOORScreenInvalidActThres)
                                        else:
                                            raise ValueError
                                    except:
                                        controller.show_frame(AOORScreenInvalidMSR)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(AOORScreenInvalidAPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(AOORScreenInvalidAAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(AOORScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(AOORScreenInvalidLRL)

'''
@function: updateVOOR - Updates all the parameter values for the VOOR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time
                    
@return - None
'''
def updateVOOR(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, mSR, actThres, reactTime, responseFac, recovTime):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(VOORScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(VOORScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(VOORScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(VOORScreenInvalidVPW)
                else:
                    if(len(mSR) == 0):
                        controller.show_frame(VOORScreenInvalidMSR)
                    else:
                        if(len(actThres) == 0):
                            controller.show_frame(VOORScreenInvalidActThres)
                        else:
                            if(len(reactTime) == 0):
                                controller.show_frame(VOORScreenInvalidReactTime)
                            else:
                                if(len(responseFac) == 0):
                                    controller.show_frame(VOORScreenInvalidResponseFac)    
                                else:
                                    if(len(recovTime) == 0):
                                        controller.show_frame(VOORScreenInvalidRecovTime)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['voor']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['voor']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['voor']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if(float(ventriPulseWidth)==0.05 or(float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['voor']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                            userData[user]['voor']['maximumSensRate'] = int(mSR)
                                            try:
                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                    userData[user]['voor']['activityThres'] = actThres
                                                    try:
                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                            userData[user]['voor']['reactTime'] = int(reactTime)
                                                            try:
                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                    userData[user]['voor']['responseFac'] = int(responseFac)
                                                                    try:
                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                            userData[user]['voor']['recovTime'] = int(recovTime)
                                                                            updateData()# Updates the Local Copy
                                                                            # Sends the Data to Board (Serial Comm)

                                                                            try:
                                                                                #PySerial Sending the Values to the Board as a byte array
                                                                                if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                    ser.open()

                                                                                valuesList = [16,55,6]
                                                                                values = bytearray(valuesList)
                                                                                ser.write(values)

                                                                            except:
                                                                                print("Serial Communication Not Established")

                                                                            print("User VOOR Updated")
                                                                            print(userData)
                                                                            #If the inputs are correct
                                                                            controller.show_frame(MainPage)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(VOORScreenInvalidRecovTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(VOORScreenInvalidResponseFac)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(VOORScreenInvalidReactTime)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(VOORScreenInvalidActThres)
                                        else:
                                            raise ValueError
                                    except:
                                        controller.show_frame(VOORScreenInvalidMSR)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(VOORScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(VOORScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(VOORScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(VOORScreenInvalidLRL)

'''
@function: updateAAIR - Updates all the parameter values for the AAIR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width, atrialSensitivity - Atrial Sensitivity, ARP - Atrial Refractory Period, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time
                    
@return - None
'''
def updateAAIR(controller, user, lowerRate, upperRate, atrialAmp, atrialPulseWidth, atrialSensitivity, aRP , mSR, actThres, reactTime, responseFac, recovTime):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(AAIRScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(AAIRScreenInvalidURL)
        else:
            if(len(atrialAmp) == 0):
                controller.show_frame(AAIRScreenInvalidAAmp)
            else:
                if(len(atrialPulseWidth) == 0):
                    controller.show_frame(AAIRScreenInvalidAPW)
                else:
                    if(len(atrialSensitivity) == 0):
                        controller.show_frame(AAIRScreenInvalidASens)
                    else:
                        if(len(aRP) == 0):
                            controller.show_frame(AAIRScreenInvalidARP)
                        else:
                            if(len(mSR) == 0):
                                controller.show_frame(AAIRScreenInvalidMSR)
                            else:
                                if(len(actThres) == 0):
                                    controller.show_frame(AAIRScreenInvalidActThres)
                                else:
                                    if(len(reactTime) == 0):
                                        controller.show_frame(AAIRScreenInvalidReactTime)
                                    else:
                                        if(len(responseFac) == 0):
                                            controller.show_frame(AAIRScreenInvalidResponseFac)    
                                        else:
                                            if(len(recovTime) == 0):
                                                controller.show_frame(AAIRScreenInvalidRecovTime)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['aair']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['aair']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                            userData[user]['aair']['atrialAmp'] = float(atrialAmp) 
                            try:
                                if(float(atrialPulseWidth)==0.05 or (float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                    userData[user]['aair']['atrialPulseWidth'] = float(atrialPulseWidth)
                                    try:
                                        if(float(atrialSensitivity)==0.25 or float(atrialSensitivity)==0.5 or float(atrialSensitivity)==0.75  or(float(atrialSensitivity)%0.5 == 0.0 and float(atrialSensitivity)>=1.0 and float(atrialSensitivity)<=10.0)):
                                            userData[user]['aair']['atrialSensitivity'] = float(atrialSensitivity)
                                            try:
                                                if(int(aRP)%10== 0 and int(aRP)>=150 and int(aRP)<=500):
                                                    userData[user]['aair']['ARP'] = int(aRP)
                                                    try:
                                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                                            userData[user]['aair']['maximumSensRate'] = int(mSR)
                                                            try:
                                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                                    userData[user]['aair']['activityThres'] = actThres
                                                                    try:
                                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                                            userData[user]['aair']['reactTime'] = int(reactTime)
                                                                            try:
                                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                                    userData[user]['aair']['responseFac'] = int(responseFac)
                                                                                    try:
                                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                                            userData[user]['aair']['recovTime'] = int(recovTime)
                                                                                            updateData()# Updates the Local Copy
                                                                                            # Sends the Data to Board (Serial Comm)

                                                                                            try:
                                                                                                #PySerial Sending the Values to the Board as a byte array
                                                                                                if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                                    ser.open()

                                                                                                valuesList = [16,55,9]
                                                                                                values = bytearray(valuesList)
                                                                                                ser.write(values)

                                                                                            except:
                                                                                                print("Serial Communication Not Established")

                                                                                            print("User AAIR Updated")
                                                                                            print(userData)
                                                                                            #If the inputs are correct
                                                                                            controller.show_frame(MainPage)
                                                                                        else:
                                                                                            raise ValueError
                                                                                    except:
                                                                                        controller.show_frame(AAIRScreenInvalidRecovTime)
                                                                                else:
                                                                                    raise ValueError
                                                                            except:
                                                                                controller.show_frame(AAIRScreenInvalidResponseFac)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(AAIRScreenInvalidReactTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(AAIRScreenInvalidActThres)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(AAIRScreenInvalidMSR)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(AAIRScreenInvalidARP)
                                        else:
                                            raise ValueError
                                    except:
                                            controller.show_frame(AAIRScreenInvalidASens)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(AAIRScreenInvalidAPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(AAIRScreenInvalidAAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(AAIRScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(AAIRScreenInvalidLRL)

'''
@function: updateVVIR - Updates all the parameter values for the VVIR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, ventriSensitivity - Ventricular Sensitivity, VRP - Ventricular Refractory Period, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time
                    
@return - None
'''
def updateVVIR(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, ventriSensitivity, vRP , mSR, actThres, reactTime, responseFac, recovTime):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(VVIRScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(VVIRScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(VVIRScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(VVIRScreenInvalidVPW)
                else:
                    if(len(ventriSensitivity) == 0):
                        controller.show_frame(VVIRScreenInvalidVSens)
                    else:
                        if(len(vRP) == 0):
                            controller.show_frame(VVIRScreenInvalidVRP)
                        else:
                            if(len(mSR) == 0):
                                controller.show_frame(VVIRScreenInvalidMSR)
                            else:
                                if(len(actThres) == 0):
                                    controller.show_frame(VVIRScreenInvalidActThres)
                                else:
                                    if(len(reactTime) == 0):
                                        controller.show_frame(VVIRScreenInvalidReactTime)
                                    else:
                                        if(len(responseFac) == 0):
                                            controller.show_frame(VVIRScreenInvalidResponseFac)    
                                        else:
                                            if(len(recovTime) == 0):
                                                controller.show_frame(VVIRScreenInvalidRecovTime)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['vvir']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['vvir']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['vvir']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if(float(ventriPulseWidth)==0.05 or (float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['vvir']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if(float(ventriSensitivity)==0.25 or float(ventriSensitivity)==0.5 or float(ventriSensitivity)==0.75  or(float(ventriSensitivity)%0.5 == 0.0 and float(ventriSensitivity)>=1.0 and float(ventriSensitivity)<=10.0)):
                                            userData[user]['vvir']['ventriSensitivity'] = float(ventriSensitivity)
                                            try:
                                                if(int(vRP)%10== 0 and int(vRP)>=150 and int(vRP)<=500):
                                                    userData[user]['vvir']['VRP'] = int(vRP)
                                                    try:
                                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                                            userData[user]['vvir']['maximumSensRate'] = int(mSR)
                                                            try:
                                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                                    userData[user]['vvir']['activityThres'] = actThres
                                                                    try:
                                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                                            userData[user]['vvir']['reactTime'] = int(reactTime)
                                                                            try:
                                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                                    userData[user]['vvir']['responseFac'] = int(responseFac)
                                                                                    try:
                                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                                            userData[user]['vvir']['recovTime'] = int(recovTime)
                                                                                            updateData()# Updates the Local Copy
                                                                                            # Sends the Data to Board (Serial Comm)

                                                                                            try:
                                                                                                #PySerial Sending the Values to the Board as a byte array
                                                                                                if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                                    ser.open()

                                                                                                valuesList = [16,55,8]
                                                                                                values = bytearray(valuesList)
                                                                                                ser.write(values)
                                                                                            except:
                                                                                                print("Serial Communication Not Established")

                                                                        
                                                                                            print("User VVIR Updated")
                                                                                            print(userData)
                                                                                            #If the inputs are correct
                                                                                            controller.show_frame(MainPage)
                                                                                        else:
                                                                                            raise ValueError
                                                                                    except:
                                                                                        controller.show_frame(VVIRScreenInvalidRecovTime)
                                                                                else:
                                                                                    raise ValueError
                                                                            except:
                                                                                controller.show_frame(VVIRScreenInvalidResponseFac)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(VVIRScreenInvalidReactTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(VVIRScreenInvalidActThres)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(VVIRScreenInvalidMSR)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(VVIRScreenInvalidVRP)
                                        else:
                                            raise ValueError
                                    except:
                                            controller.show_frame(VVIRScreenInvalidVSens)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(VVIRScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(VVIRScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(VVIRScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(VVIRScreenInvalidLRL)

'''
@function: updateDOOR - Updates all the parameter values for the DOOR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time, fixedDel - Fixed AV Delay
                    
@return - None
'''
def updateDOOR(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, atrialAmp, atrialPulseWidth, mSR, actThres, reactTime, responseFac, recovTime, fixedDel):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(DOORScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(DOORScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(DOORScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(DOORScreenInvalidVPW)
                else:
                    if(len(atrialAmp) == 0):
                        controller.show_frame(DOORScreenInvalidAAmp)
                    else:
                        if(len(atrialPulseWidth) == 0):
                            controller.show_frame(DOORScreenInvalidAPW)
                        else:
                            if(len(mSR) == 0):
                                controller.show_frame(DOORScreenInvalidMSR)
                            else:
                                if(len(actThres) == 0):
                                    controller.show_frame(DOORScreenInvalidActThres)
                                else:
                                    if(len(reactTime) == 0):
                                        controller.show_frame(DOORScreenInvalidReactTime)
                                    else:
                                        if(len(responseFac) == 0):
                                            controller.show_frame(DOORScreenInvalidResponseFac)    
                                        else:
                                            if(len(recovTime) == 0):
                                                controller.show_frame(DOORScreenInvalidRecovTime)
                                            else:
                                                if(len(fixedDel) == 0):
                                                    controller.show_frame(DOORScreenInvalidFixedAVDelay)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['door']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['door']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['door']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if(float(ventriPulseWidth)==0.05 or (float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['door']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                                            userData[user]['door']['atrialAmp'] = float(atrialAmp)
                                            try:
                                                if(float(atrialPulseWidth)==0.05 or (float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                                    userData[user]['door']['atrialPulseWidth'] = float(atrialPulseWidth)
                                                    try:
                                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                                            userData[user]['door']['maximumSensRate'] = int(mSR)
                                                            try:
                                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                                    userData[user]['door']['activityThres'] = actThres
                                                                    try:
                                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                                            userData[user]['door']['reactTime'] = int(reactTime)
                                                                            try:
                                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                                    userData[user]['door']['responseFac'] = int(responseFac)
                                                                                    try:
                                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                                            userData[user]['door']['recovTime'] = int(recovTime)
                                                                                            try:
                                                                                                if(int(fixedDel)>=70 and int(fixedDel)<=300):
                                                                                                    userData[user]['door']['recovTime'] = int(fixedDel)
                                                                                                    updateData()# Updates the Local Copy
                                                                                                    # Sends the Data to Board (Serial Comm)

                                                                                                    try:
                                                                                                        #PySerial Sending the Values to the Board as a byte array
                                                                                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                                            ser.open()

                                                                                                        valuesList = [16,55,10]
                                                                                                        values = bytearray(valuesList)
                                                                                                        ser.write(values)
                                                                                                    except:
                                                                                                        print("Serial Communication Not Established")

                                                                                                
                                                                                                    print("User DOOR Updated")
                                                                                                    print(userData)
                                                                                                    #If the inputs are correct
                                                                                                    controller.show_frame(MainPage)
                                                                                                else:
                                                                                                    raise ValueError
                                                                                            except:
                                                                                                controller.show_frame(DOORScreenInvalidFixedAVDelay)
                                                                                        else:
                                                                                            raise ValueError
                                                                                    except:
                                                                                        controller.show_frame(DOORScreenInvalidRecovTime)
                                                                                else:
                                                                                    raise ValueError
                                                                            except:
                                                                                controller.show_frame(DOORScreenInvalidResponseFac)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(DOORScreenInvalidReactTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(DOORScreenInvalidActThres)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(DOORScreenInvalidMSR)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(DOORScreenInvalidAPW)
                                        else:
                                            raise ValueError
                                    except:
                                            controller.show_frame(DOORScreenInvalidAAmp)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(DOORScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(DOORScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(DOORScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(DOORScreenInvalidLRL)

'''
@function: updateDDDR - Updates all the parameter values for the DDDR Mode
@param - controller - Used to transition between Tkinter Frames, user - Indicates Current User, lowerRate - lower Rate Limit, , upperRate - upper Rate Limit
                    ventriAmp - Ventricular Amplitude, ventriPulseWidth - Ventricular Pulse Width, atrialAmp - Atrial Amplitude, atrialPulseWidth - Atrial Pulse Width, mSR - Maximum Sensor Rate, actThres - Activity Threshold, 
                    reactTime - Reaction Time, responseFac - Response Factor, recovTime - Recovery Time, fixedDel - Fixed AV Delay, dynamicDel - Dynamic AV Delay, pvARP - Post Ventrical Atrial Refractory Period
                    
@return - None
'''
def updateDDDR(controller, user, lowerRate, upperRate, ventriAmp, ventriPulseWidth, atrialAmp, atrialPulseWidth, mSR, actThres, reactTime, responseFac, recovTime, fixedDel, dynamicDel, pvARP):

 #Checks for any empty input and sends an invaild input message
    if(len(lowerRate) == 0):
        controller.show_frame(DDDRScreenInvalidLRL)
    else:
        if(len(upperRate)==0):
            controller.show_frame(DDDRScreenInvalidURL)
        else:
            if(len(ventriAmp) == 0):
                controller.show_frame(DDDRScreenInvalidVAmp)
            else:
                if(len(ventriPulseWidth) == 0):
                    controller.show_frame(DDDRScreenInvalidVPW)
                else:
                    if(len(atrialAmp) == 0):
                        controller.show_frame(DDDRScreenInvalidAAmp)
                    else:
                        if(len(atrialPulseWidth) == 0):
                            controller.show_frame(DDDRScreenInvalidAPW)
                        else:
                            if(len(mSR) == 0):
                                controller.show_frame(DDDRScreenInvalidMSR)
                            else:
                                if(len(actThres) == 0):
                                    controller.show_frame(DDDRScreenInvalidActThres)
                                else:
                                    if(len(reactTime) == 0):
                                        controller.show_frame(DDDRScreenInvalidReactTime)
                                    else:
                                        if(len(responseFac) == 0):
                                            controller.show_frame(DDDRScreenInvalidResponseFac)    
                                        else:
                                            if(len(recovTime) == 0):
                                                controller.show_frame(DDDRScreenInvalidRecovTime)
                                            else:
                                                if(len(fixedDel) == 0):
                                                    controller.show_frame(DDDRScreenInvalidFixedAVDelay)
                                                else:
                                                    if(len(dynamicDel) == 0):
                                                        controller.show_frame(DDDRScreenInvalidDynamicAVDelay)
                                                    else:
                                                        if(len(pvARP) == 0):
                                                            controller.show_frame(DDDRScreenInvalidPVARP)

    #If the initial checks are passed
    #Checks for appropriate type of input and transfers into the database
    try:
        if(int(lowerRate)%5 ==0 and int(lowerRate)>=30 and int(lowerRate)<=175 and int(lowerRate) < int(upperRate)):
            userData[user]['dddr']['lowerRateLimit'] = int(lowerRate)
            try:
                if(int(upperRate)%5 ==0 and int(upperRate)>= 30 and int(upperRate)<=175):
                    userData[user]['dddr']['upperRateLimit'] = int(upperRate)
                    try:
                        if(float(ventriAmp)%1.25 == 0.0 and float(ventriAmp)>0 and float(ventriAmp)<=5.0):
                            userData[user]['dddr']['ventriAmp'] = float(ventriAmp) 
                            try:
                                if(float(ventriPulseWidth)==0.05 or (float(ventriPulseWidth)>=0.1 and float(ventriPulseWidth)<=1.9)):
                                    userData[user]['dddr']['ventriPulseWidth'] = float(ventriPulseWidth)
                                    try:
                                        if(float(atrialAmp)%1.25 == 0.0 and float(atrialAmp)>0 and float(atrialAmp)<=5.0):
                                            userData[user]['dddr']['atrialAmp'] = float(atrialAmp)
                                            try:
                                                if(float(atrialPulseWidth)==0.05 or (float(atrialPulseWidth)>=0.1 and float(atrialPulseWidth)<=1.9)):
                                                    userData[user]['dddr']['atrialPulseWidth'] = float(atrialPulseWidth)
                                                    try:
                                                        if(int(mSR)%5 ==0 and int(mSR)>= 30 and int(mSR)<=175):
                                                            userData[user]['dddr']['maximumSensRate'] = int(mSR)
                                                            try:
                                                                if(actThres=="vlow" or actThres=="low" or actThres=="medlow" or actThres=="med" or actThres=="medhigh" or actThres=="high" or actThres=="vhigh"):
                                                                    userData[user]['dddr']['activityThres'] = actThres
                                                                    try:
                                                                        if(int(reactTime) >= 10 and int(reactTime) <= 50 and int(reactTime)%10 == 0):
                                                                            userData[user]['dddr']['reactTime'] = int(reactTime)
                                                                            try:
                                                                                if(int(responseFac)>=1 and int(responseFac)<=16):
                                                                                    userData[user]['dddr']['responseFac'] = int(responseFac)
                                                                                    try:
                                                                                        if(int(recovTime)>=2 and int(responseFac)<=16):
                                                                                            userData[user]['dddr']['recovTime'] = int(recovTime)
                                                                                            try:
                                                                                                if(int(fixedDel)>=70 and int(fixedDel)<=300):
                                                                                                    userData[user]['dddr']['recovTime'] = int(fixedDel)
                                                                                                    try:
                                                                                                        if(dynamicDel=="on" or dynamicDel == "off"):
                                                                                                            userData[user]['dddr']['dynamicAVDelay'] = dynamicDel
                                                                                                            try:
                                                                                                                if(int(pvARP)>=150 and int(pvARP)<=500):
                                                                                                                    userData[user]['dddr']['PVARP'] = int(pvARP)
                                                                                                                    updateData()# Updates the Local Copy
                                                                                                                    # Sends the Data to Board (Serial Comm)

                                                                                                                    try:
                                                                                                                        #PySerial Sending the Values to the Board as a byte array
                                                                                                                        if(ser.is_open==False): #Open Serial Port if already not opened
                                                                                                                            ser.open()

                                                                                                                        valuesList = [16,55,11]
                                                                                                                        values = bytearray(valuesList)
                                                                                                                        ser.write(values)
                                                                                                                    except:
                                                                                                                        print("Serial Communication Not Established")

                                                                                                                    
                                                                                                                    print("User DDDR Updated")
                                                                                                                    print(userData)
                                                                                                                    #If the inputs are correct
                                                                                                                    controller.show_frame(MainPage)
                                                                                                                else:
                                                                                                                    raise ValueError
                                                                                                            except:
                                                                                                                controller.show_frame(DDDRScreenInvalidPVARP)
                                                                                                        else:
                                                                                                            raise ValueError
                                                                                                    except:
                                                                                                        controller.show_frame(DDDRScreenInvalidDynamicAVDelay)
                                                                                                else:
                                                                                                    raise ValueError
                                                                                            except:
                                                                                                controller.show_frame(DDDRScreenInvalidFixedAVDelay)
                                                                                        else:
                                                                                            raise ValueError
                                                                                    except:
                                                                                        controller.show_frame(DDDRScreenInvalidRecovTime)
                                                                                else:
                                                                                    raise ValueError
                                                                            except:
                                                                                controller.show_frame(DDDRScreenInvalidResponseFac)
                                                                        else:
                                                                            raise ValueError
                                                                    except:
                                                                        controller.show_frame(DDDRScreenInvalidReactTime)
                                                                else:
                                                                    raise ValueError
                                                            except:
                                                                controller.show_frame(DDDRScreenInvalidActThres)
                                                        else:
                                                            raise ValueError
                                                    except:
                                                        controller.show_frame(DDDRScreenInvalidMSR)
                                                else:
                                                    raise ValueError
                                            except:
                                                controller.show_frame(DDDRScreenInvalidAPW)
                                        else:
                                            raise ValueError
                                    except:
                                            controller.show_frame(DDDRScreenInvalidAAmp)
                                else:
                                    raise ValueError
                            except:
                                controller.show_frame(DDDRScreenInvalidVPW)
                        else:
                            raise ValueError
                    except:
                        controller.show_frame(DDDRScreenInvalidVAmp)
                else:
                    raise ValueError
            except:
                controller.show_frame(DDDRScreenInvalidURL)
        else:
            raise ValueError #Moves to the Other State 
    except:
        controller.show_frame(DDDRScreenInvalidLRL)


#Tkinter Frames Dealing With the Welcome Screen

'''
@class: MainPage(tk.Tk) - Tkinter Frame of the Main Page
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class MainPage(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''     
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "Main Menu - Which Mode Do You Want to Configure?", font = LARGE_FONT)
        label.grid(row = 0, column = 2, padx=10, pady=10)

        #Buttons
        backButton = ttk.Button(self, text = "Go Back To Start", command =lambda: controller.show_frame(WelcomeScreen))
        backButton.grid(row = 4,column = 2, padx=10, pady=10)

        aooButton = ttk.Button(self, text = "AOO", command =lambda: controller.show_frame(AOOScreen))
        aooButton.grid(row = 1,column = 0, padx=10, pady=10)

        vooButton = ttk.Button(self, text = "VOO", command = lambda: controller.show_frame(VOOScreen))
        vooButton.grid(row = 1,column = 1, padx=10, pady=10)

        aaiButton = ttk.Button(self, text = "AAI", command = lambda: controller.show_frame(AAIScreen))
        aaiButton.grid(row = 1,column =3, padx=10, pady=10)

        vviButton = ttk.Button(self, text = "VVI", command = lambda: controller.show_frame(VVIScreen))
        vviButton.grid(row = 1,column =4, padx=10, pady=10)

        dooButton = ttk.Button(self, text = "DOO", command = lambda: controller.show_frame(DOOScreen))
        dooButton.grid(row = 2,column =0, padx=10, pady=10)

        aoorButton = ttk.Button(self, text = "AOOR", command = lambda: controller.show_frame(AOORScreen))
        aoorButton.grid(row = 2,column =1, padx=10, pady=10)

        voorButton = ttk.Button(self, text = "VOOR", command = lambda: controller.show_frame(VOORScreen))
        voorButton.grid(row = 2,column =3, padx=10, pady=10)

        aairButton = ttk.Button(self, text = "AAIR", command = lambda: controller.show_frame(AAIRScreen))
        aairButton.grid(row = 2,column =4, padx=10, pady=10)

        vvirButton = ttk.Button(self, text = "VVIR", command = lambda: controller.show_frame(VVIRScreen))
        vvirButton.grid(row = 3,column =0, padx=10, pady=10)

        doorButton = ttk.Button(self, text = "DOOR", command = lambda: controller.show_frame(DOORScreen))
        doorButton.grid(row = 3,column =1, padx=10, pady=10)

        dddrButton = ttk.Button(self, text = "DDDR", command = lambda: controller.show_frame(DDDRScreen))
        dddrButton.grid(row = 3,column =3, padx=10, pady=10)

'''
@class: AOOScreen(tk.Tk) - Tkinter Frame of the AOO Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOOScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)
        
        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateAOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: AOOScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AOO Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOOScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateAOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: AOOScreenInvalidURL(tk.Tk) - Tkinter Frame of the AOO Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOOScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateAOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)
   
  
'''
@class: AOOScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the AOO Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOOScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateAOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: AOOScreenInvalidAPW(tk.Tk) - Tkinter Frame of the AOO Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOOScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateAOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: AAIScreen(tk.Tk) - Tkinter Frame of the AAI Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AAI Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AAI Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the AOO Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidAPW(tk.Tk) - Tkinter Frame of the AAI Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidASens(tk.Tk) - Tkinter Frame of the AAI Programming Screen with "InvalidInput" text for Atrial Sensitivity
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidASens(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIScreenInvalidARP(tk.Tk) - Tkinter Frame of the AAI Programming Screen with "InvalidInput" text for Atrial Refractory Period
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIScreenInvalidARP(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100), atrSens.delete(0,100), aRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOOScreen(tk.Tk) - Tkinter Frame of the VOO Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOOScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateVOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: VOOScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VOO Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOOScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateVOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)
'''
@class: VOOScreenInvalidURL(tk.Tk) - Tkinter Frame of the VOO Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOOScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateVOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)
'''
@class: VOOScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the VOO Programming Screen with "InvalidInput" text for Ventri Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOOScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateVOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: VOOScreenInvalidAPW(tk.Tk) - Tkinter Frame of the VOO Programming Screen with "InvalidInput" text for Ventri Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOOScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command =lambda: [f() for f in [updateVOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get()), lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100), upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100)]])
        closeBox.grid(row = 4,column = 5, padx=10)

'''
@class: VVIScreen(tk.Tk) - Tkinter Frame of the VVI Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "               ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)


'''
@class: VVIScreenInvalidURL(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3)

        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
    
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column =5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Ventri Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
       #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3)

        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
    
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column =5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIScreenInvalidVPW(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Ventri Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3)

        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
    
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column =5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIScreenInvalidVSens(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Ventri Sensitivity
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidVSens(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3)

        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
    
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column =5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIScreenInvalidVRP(tk.Tk) - Tkinter Frame of the VVI Programming Screen with "InvalidInput" text for Ventri Refractory Period
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIScreenInvalidVRP(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3)

        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column=1, padx=10)
    
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVI(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        createBox.grid(row = 1,column =5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), vtrSens.delete(0,100), vRP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreen(tk.Tk) - Tkinter Frame of the DOO Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "               ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreenInvalidLRL(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreenInvalidURL(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
       #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreenInvalidAPW(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: DOOScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Ventri Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOO Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOOScreenInvalidVPW(tk.Tk) - Tkinter Frame of the DOO Programming Screen with "InvalidInput" text for Ventri Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOOScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVI Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrialAmp = ttk.Entry(self)
        atrialAmp.grid(row = 5, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrialPulseWidth = ttk.Entry(self)
        atrialPulseWidth.grid(row=6, column=1, padx=10)
       
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOO(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrialAmp.get(), atrialPulseWidth.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100), atrialAmp.delete(0,100), atrialPulseWidth.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)


'''
@class: AOORScreen(tk.Tk) - Tkinter Frame of the AOOR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: A00RScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: AOORScreenInvalidAPW(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidMSR(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidActThres(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AOORScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the AOOR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AOORScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreen(tk.Tk) - Tkinter Frame of the VOOR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: V00RScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Ventricular Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: VOORScreenInvalidVPW(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Ventricular Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidMSR(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidActThres(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
       #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VOORScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the VOOR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VOORScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''   
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=7, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=9, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreen(tk.Tk) - Tkinter Frame of the AAIR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
'''
class AAIRScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: AAIRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: AOORScreenInvalidAPW(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidAPW(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Atrial Sensitivity
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidASens(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidARP(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Atrial Refractory Period
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidARP(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidMSR(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidActThres(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: AAIRScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 10, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: AAIRScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the AAIR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class AAIRScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "AAIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 11, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V(1.25V Increments))",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrSens = ttk.Entry(self)
        atrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="ARP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        aRP = ttk.Entry(self)
        aRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateAAIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), atrAmp.get(), atrPulseWidth.get(), atrSens.get(), aRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), atrAmp.delete(0,100), atrPulseWidth.delete(0,100),atrSens.delete(0,100),aRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreen(tk.Tk) - Tkinter Frame of the VVIR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
'''
class VVIRScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
    
'''
@class: VVIRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Ventricular Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: VVIRScreenInvalidAPW(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Ventricular Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidAPW(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Ventricular Sensitivity
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidVSens(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidARP(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Ventricular Refractory Period
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidVRP(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidMSR(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidActThres(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: VVIRScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 10, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: VVIRScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class VVIRScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "VVIR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 11, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Sensitivity(mV)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        vtrSens = ttk.Entry(self)
        vtrSens.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="VRP(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        vRP = ttk.Entry(self)
        vRP.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateVVIR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), vtrSens.get(), vRP.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),vtrSens.delete(0,100),vRP.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreen(tk.Tk) - Tkinter Frame of the DOOR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
'''
class DOORScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
    
'''
@class: DOORScreenInvalidLRL(tk.Tk) - Tkinter Frame of the VVIR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Ventricular Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: DOORScreenInvalidAPW(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Ventricular Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidAPW(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

       #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidMSR(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidActThres(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: DOORScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 10, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DOORScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 11, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
        
'''
@class: DOORScreenInvalidFixedAVDelay(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Fixed AV Delay
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DOORScreenInvalidFixedAVDelay(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DOOR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 12, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDOOR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreen(tk.Tk) - Tkinter Frame of the DDDR Programming Screen
@param - tk.Tk - Tkinter Reference
@return - None
'''
class DDDRScreen(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):

        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        #Padding
        label = tk.Label(self, text = "                  ",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Lower Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidLRL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 1, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
    
'''
@class: DDDRScreenInvalidLRL(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Upper Rate Limit
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidURL(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 2, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidVAmp(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Ventricular Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidVAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 3, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: DDDRScreenInvalidAPW(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Ventricular Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidVPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 4, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidAAmp(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Atrial Amplitude
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidAAmp(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 5, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidAPW(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Atrial Pulse Width
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidAPW(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 6, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidMSR(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Maximum Sensor Rate
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidMSR(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 7, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidActThres(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Activity Threshold
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidActThres(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 8, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidReactTime(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Reaction Time
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidReactTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 9, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
'''
@class: DOORScreenInvalidResponseFac(tk.Tk) - Tkinter Frame of the DOOR Programming Screen with "InvalidInput" text for Response Factor
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidResponseFac(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 10, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidRecovTime(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for RecoveryTime
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidRecovTime(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 11, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)
        
'''
@class: DDDRScreenInvalidFixedAVDelay(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Fixed AV Delay
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidFixedAVDelay(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 12, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidDynamicAVDelay(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for Dynamic AV Delay
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidDynamicAVDelay(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 13, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

'''
@class: DDDRScreenInvalidPVARP(tk.Tk) - Tkinter Frame of the DDDR Programming Screen with "InvalidInput" text for PVARP
@param - tk.Tk - Tkinter Reference
@return - None
''' 
class DDDRScreenInvalidPVARP(tk.Frame):
    '''
    @function: __init__() - Setups the class and its specific paramets
    @param - self, parent, controller - Helps with Frame Transistion
    @return - None
    '''  
    def __init__(self, parent, controller):
        #Text
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "DDDR Values", font = LARGE_FONT)
        label.grid(row = 0, column = 1, padx=10, pady=10)

        label = tk.Label(self, text = "Invalid Input!",fg = "red", font = LARGE_FONT)
        label.grid(row = 14, column = 3, padx=10)

        #Entry Boxes
        label=ttk.Label(self, text="Lower Rate Limit(ppm)",font=LARGE_FONT)
        label.grid(row=1, column = 0, padx=10)
        lowerLimit = ttk.Entry(self)
        lowerLimit.grid(row = 1, column=1, padx=10)
    
        label=ttk.Label(self, text="Upper Rate Limit(ppm)", font=LARGE_FONT)
        label.grid(row=2, column = 0, padx=10)
        upperLimit = ttk.Entry(self)
        upperLimit.grid(row=2, column=1, padx=10)

        label=ttk.Label(self, text="Ventricular Amplitude(V)",font=LARGE_FONT)
        label.grid(row=3, column = 0, padx=10)
        vtrAmp = ttk.Entry(self)
        vtrAmp.grid(row = 3, column=1, padx=10)
    
        label=ttk.Label(self, text="Ventricular Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=4, column = 0, padx=10)
        vtrPulseWidth = ttk.Entry(self)
        vtrPulseWidth.grid(row=4, column=1, padx=10)

        label=ttk.Label(self, text="Atrial Amplitude(V)",font=LARGE_FONT)
        label.grid(row=5, column = 0, padx=10)
        atrAmp = ttk.Entry(self)
        atrAmp.grid(row = 5, column= 1, padx=10)
    
        label=ttk.Label(self, text="Atrial Pulse Width(ms)", font=LARGE_FONT)
        label.grid(row=6, column = 0, padx=10)
        atrPulseWidth = ttk.Entry(self)
        atrPulseWidth.grid(row=6, column= 1, padx=10)

        label=ttk.Label(self, text="Maximum Sensor Rate(ppm)",font=LARGE_FONT)
        label.grid(row=7, column = 0, padx=10)
        mSR = ttk.Entry(self)
        mSR.grid(row = 7, column= 1, padx=10)
    
        label=ttk.Label(self, text="Activity Threshold(Mode)", font=LARGE_FONT)
        label.grid(row=8, column = 0, padx=10)
        actThres = ttk.Entry(self)
        actThres.grid(row=8, column= 1, padx=10)

        label=ttk.Label(self, text="Reaction Time(secs)", font=LARGE_FONT)
        label.grid(row=9, column = 0, padx=10)
        reactTime = ttk.Entry(self)
        reactTime.grid(row=9, column= 1, padx=10)

        label=ttk.Label(self, text="Reponse Factor", font=LARGE_FONT)
        label.grid(row=10, column = 0, padx=10)
        responseFac = ttk.Entry(self)
        responseFac.grid(row=10, column= 1, padx=10)

        label=ttk.Label(self, text="Recovery Time(min)", font=LARGE_FONT)
        label.grid(row=11, column = 0, padx=10)
        recovTime = ttk.Entry(self)
        recovTime.grid(row=11, column= 1, padx=10)

        label=ttk.Label(self, text="Fixed AV Delay(ms)", font=LARGE_FONT)
        label.grid(row=12, column = 0, padx=10)
        fixedDel = ttk.Entry(self)
        fixedDel.grid(row=12, column= 1, padx=10)

        label=ttk.Label(self, text="Dynamic AV Delay(on/off)", font=LARGE_FONT)
        label.grid(row=13, column = 0, padx=10)
        dynamicDel = ttk.Entry(self)
        dynamicDel.grid(row=13, column= 1, padx=10)

        label=ttk.Label(self, text="PVARP(ms)", font=LARGE_FONT)
        label.grid(row=14, column = 0, padx=10)
        pvARP = ttk.Entry(self)
        pvARP.grid(row=14, column= 1, padx=10)
        
        #Buttons
        createBox = ttk.Button(self, text = "Create and Send Signal", command = lambda: [f() for f in [updateDDDR(controller, getCurrentUser(),lowerLimit.get(), upperLimit.get(), vtrAmp.get(), vtrPulseWidth.get(), atrAmp.get(), atrPulseWidth.get(),mSR.get(), actThres.get(),reactTime.get(),responseFac.get(),recovTime.get(),fixedDel.get(), dynamicDel.get(), pvARP.get()),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100),pvARP.delete(0,100)]])
        createBox.grid(row = 1,column = 5, padx=10)

        closeBox = ttk.Button(self, text = "Go Back to Main Page", command = lambda: [f() for f in [controller.show_frame(MainPage),lowerLimit.delete(0,100),upperLimit.delete(0,100), vtrAmp.delete(0,100), vtrPulseWidth.delete(0,100),atrAmp.delete(0,100),atrPulseWidth.delete(0,100),mSR.delete(0,100),actThres.delete(0,100),reactTime.delete(0,100),responseFac.delete(0,100),recovTime.delete(0,100),fixedDel.delete(0,100), dynamicDel.delete(0,100), pvARP.delete(0,100)]])
        closeBox.grid(row = 6,column = 5, padx=10)

#Tkinter Reference Lines - Launching the Applet
app = projectGUI()
app.mainloop()
