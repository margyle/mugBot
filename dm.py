from tweepy import *
import tweepy
import RPi.GPIO as gpio
import pickle as pkl
import time
 
#import RPi.GPIO as gpio
last_id = '0'
ledstat = False
gpio.cleanup()
gpio.setmode(gpio.BOARD)
gpio.setup(13,gpio.OUT)
gpio.output(13,ledstat)
 
def authenticate():
     
    consumer_token = ""#put your credentials here
    consumer_secret = ""#
 
    auth = tweepy.OAuthHandler(consumer_token,consumer_secret)
 
    access_token = ""#
    access_token_secret = ""#
 
    auth.set_access_token(access_token,access_token_secret)
 
    api = tweepy.API(auth)
 
    return api
 
 
def check_new_DM(api):
 
    global last_id
     
    DMstatus = api.direct_messages(since_id = last_id,count = 1)
 
    if len(DMstatus)>0:
         
        last_id = DMstatus[0].id_str
         
        if (DMstatus[0].sender_screen_name == 'io_house'):#replace _______ with the account from which you want to control
            return DMstatus[0]
 
    print "\nNo new DM found"
     
    return None
 
 
def action(api,newDM):
     
    global ledstat
 
    DM = "Hi,\n"
     
    if newDM.text  == "stop":
        if ledstat == False:
            ledstat = True
            gpio.output(13,ledstat)
            DM = DM + "Your coffee is ready, enjoy!\n"#+"DM id : "+newDM.id_str
            print "stopping"
        else:
            DM = DM + "Your coffee is ready, enjoy!\n"#+"DM id : "+newDM.id_str
            print "stopped brewing"
 
    elif newDM.text == "brew":
        if ledstat==True:
            ledstat = False
            gpio.output(13,ledstat)
            DM = DM + "mugBot has started brewing your coffee!\n"#+"DM id : "+newDM.id_str
            print "started brewing"
 
        else:
            DM = DM + "mugBot has started brewing your coffee!\n"#+"DM id : "+newDM.id_str
            print "brewing "
     
    else:
        DM = DM + " Invalid Command : " + newDM.text
         
    return_DM(api,DM)
     
    return None
 
 
def return_DM(api,DM):
 
    api.send_direct_message(user = 'io_house',text = DM) # controlling account screen name as in line 42
    print "DM sent"
    return None
     
 
if __name__ == '__main__':
 
    print "Authenticating ...."
    api = authenticate()
    print "\nComplete."
 
    try:
        while(True):
 
            print "\nChecking for new DM..."
            DMstat = check_new_DM(api)
            if not(DMstat == None) :
                action(api,DMstat)
            for i in range(0,8):
                checktime = 240 - i*30
                print "Checking for new DM in " + str(checktime) + " s....."
                time.sleep(30)
         
    except KeyboardInterrupt:
        gpio.cleanup()
 
    finally:
        gpio.cleanup()
