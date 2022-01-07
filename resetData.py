'''
SFWRENG/COE 3K04 - Software Development - Device Control Monitor - Reset File
Developed By Skip the Beat

Juan D. Molina Calderón - molinacj@mcmaster.ca - 400145924
Jack Wawrychuk - wawrychj@mcmaster.ca - 400145293
Nafia Naowar - naowarn@mcmaster.ca -  400129601
Prathmesh Shetty - shettp1@mcmaster.ca - 400130037

This program is our way of resetting the database when the DCM is resetted - Not available for all user, different file and used in a manual reset option
'''
#Using pickle to encode our file for security purposes
import pickle
PIK = "DONOTTOUCHTHIS.dat"

#Dictionaries to Store User Data
'''
Structure of Our Dictionary
 - {User}{username,password,{aoo{aoo parameters}},{voo{voo parameters}},{aai{aai parameters}},{vvi{vvi parameters},{doo{doo parameters}
                                ,{aoor{aoor parameters},{voor{voor parameters},{aair{aair parameters},{vvir{vvir parameters},{door{door parameters}}}
'''
userData = { 1: {'taken': True,'username': 'admin', 'password': 'admin', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                2: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                3: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                4: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                5: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                6: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                7: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                8: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                9: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    },
                10: {'taken': False,'username': 'empty', 'password': 'empty', 
                    'aoo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0}, 
                    'voo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0},  
                    'aai':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'atrialPulseWidth':0,'atrialSensitivity':0, 'ARP':0}, 
                    'vvi':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'ventriAmp':0, 'ventriPulseWidth':0,'ventriSensitivity':0, 'VRP':0}, 
                    'doo':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'atrialAmp':0, 'ventriAmp':0,'atrialPulseWidth':0, 'ventriPulseWidth':0}, 
                    'aoor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialPulseWidth':0,'atrialAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'voor':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriPulseWidth':0,'ventriAmp':0, 'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'aair':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'atrialAmp':0,'atrialPulseWidth':0, 'atrialSensitivity':0, 'ARP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'vvir':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'ventriAmp':0,'ventriPulseWidth':0, 'ventriSensitivity':0, 'VRP':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'door':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0, 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}, 
                    'dddr':{'lowerRateLimit': 0, 'upperRateLimit': 0, 'maximumSensRate':0, 'fixedAVDelay':0,'dynamicAVDelay':0 , 'atrialAmp':0,'atrialPulseWidth':0, 'ventriAmp':0,'ventriPulseWidth':0,"PVARP":0,'activityThres':0, 'reactTime':0, 'responseFac':0, 'recovTime':0}
                    }
                }

##Resetting the data in the file             
pickle_out = open(PIK,"wb")
pickle.dump(userData, pickle_out)
pickle_out.close()
print("Done Resetting")