#!/usr/local/bin/python
# -*- coding: utf-8 -*-
##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

import epd7in5
import Image
import ImageDraw
import ImageFont
import calendar
import time
import datetime
import requests
import sys  
import urllib, json
import urllib2
import operator
import os 
import random
import threading



reload(sys)  
sys.setdefaultencoding('utf-8')
#import imagedata

EPD_WIDTH = 640
EPD_HEIGHT = 384

black = 0
white = 255

TODOIST_TOKEN = 'f5ab691321455346a27966d56965316cc2e3f8bb'
Weather_APIKEY = '5e7e4c2878e1dcc3c78fbf171fb9a848'
Weather_Country = 'US'
Weather_City = 'Los Angeles'

todolist_items=0;


def main():

        displayTasks()
        wait=60;
        refresh_time=1000
        start_time=time.time()+refresh_time

        while True:
            print('restart  : current time ' + str(time.time()/60) + ' started time ' +str(start_time/60))
            if is_todo_changed():
                start_time=time.time()+refresh_time  # rest refresh time 
                displayTasks()
            elif (time.time()-start_time)>0:
                start_time=time.time()+refresh_time # rest refresh time
                displayTasks()

            time.sleep(wait)
           
    
def is_todo_changed():
    response=requests.get("https://beta.todoist.com/API/v8/tasks", params={"token":TODOIST_TOKEN}).json()
    global todolist_items
    get_todolist_items= len (response)

    if(get_todolist_items!=todolist_items):
        print('items changed')
        return True
        

def restart_program():
    displayTasks()

def choose_random_loading_image():
    images=os.listdir("bmp/")
    loading_image=random.randint(0,len(images)-1)
    print (loading_image)
    return images[loading_image]

def displayTasks():
    epd = epd7in5.EPD()
    epd.init()
    

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    image = Image.open('bmp/'+choose_random_loading_image())
    epd.display_frame(epd.get_frame_buffer(image))


    response=requests.get("https://beta.todoist.com/API/v8/tasks", params={"token":TODOIST_TOKEN}).json()
    data=response
    global todolist_items
    todolist_items=len(data)
    
    
    f = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id=5368361&units=imperial&APPID='+Weather_APIKEY)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['name']
    temp_c = parsed_json['main']['temp']
    print "Current temperature in %s is: %s" % (location, temp_c)
    f.close()


    calendar.setfirstweekday(6)  #set the first day of the week 
    LINEHEIGHT=20

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
    font_cal = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
    font_day = ImageFont.truetype('fonts/Roboto-Black.ttf', 110)
    font_day_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 35)
    font_month_str = ImageFont.truetype('fonts/Roboto-Light.ttf', 25)

    font_weather_degree = ImageFont.truetype('fonts/Roboto-Light.ttf', 25)
    font_tasks_list_title = ImageFont.truetype('fonts/Roboto-Light.ttf',30)
    font_tasks_list = ImageFont.truetype('fonts/Roboto-Bold.ttf',15)
    font_tasks_due_date = ImageFont.truetype('fonts/tahoma.ttf',15)

    #Calendar Strings
    cal_day_str=time.strftime("%A")
    cal_day_number =time.strftime("%d")
    cal_month_str =time.strftime("%B")+' '+ time.strftime("%Y")
    today = datetime.datetime.now()
    cal_month_int = today.month;
    cal_year_int = today.year;

    cal_month_cal=str(calendar.month(cal_year_int,cal_month_int)).replace(time.strftime("%B")+' ' +time.strftime("%Y"),' ')

    cal_width=240

    #this section is to center the calendar text in the middle

    #the Day string "Monday" for Example
    w_day_str,h_day_str=font_day_str.getsize(cal_day_str)
    x_day_str=(cal_width/2)-(w_day_str/2)
    #y_day_str=(epd2in9.EPD_HEIGHT/2)-(h/2)

    #the settings for the Calenday today number
    w_day_num,h_day_num=font_day.getsize(cal_day_number)
    x_day_num=(cal_width/2)-(w_day_num/2)

    #the settings for the Calenday Month String
    w_month_str,h_month_str=font_month_str.getsize(cal_month_str)
    x_month_str=(cal_width/2)-(w_month_str/2)

    draw.rectangle((240,55,635, 384), fill = white)
    
    draw.rectangle((0,0,240, 384), fill = black)
    draw.text((15, 180),cal_month_cal , font =font_cal, fill = white)
    draw.text((x_day_str,25),cal_day_str,font=font_day_str,fill=white)
    draw.text((x_day_num,50),cal_day_number,font=font_day,fill=white)
    draw.text((x_month_str,165),cal_month_str,font=font_month_str,fill=white)

    draw.text((80,340),str(temp_c) + u'°F',font=font_weather_degree,fill=white)
    draw.line((5,320,225,320),fill=white) #weather line
    draw.text((340, 340), 'UCLA History', font=font, fill = black)
    draw.line((250,320,635,320),fill=black) # footer
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    draw.rectangle((240,0, 640, 55), fill = black)
    draw.text((250,10),"Events ",font=font_tasks_list_title,fill=white)
    
    for task in data:
        if (LINEHEIGHT>187):
            break
        item=str(task['content'])
        priority=str(task['priority'])
        draw.arc((247.5,62+LINEHEIGHT, 257.5, 72+LINEHEIGHT), 0, 360, fill = black)
        while(len(item)>35):
            part = item[0:54]
            lws = part.rfind(' ')
            part = item[0:lws]
            draw.text((265,60+LINEHEIGHT),part,font=font_tasks_list,fill=black)
            item=item[lws+1:len(item)]
            LINEHEIGHT +=26
        draw.text((265,60+LINEHEIGHT),item,font=font_tasks_list,fill=black)

        if int(priority)>2:
            draw.chord((246,62+LINEHEIGHT, 256, 72+LINEHEIGHT), 0, 360, fill = black)
            draw.text((250,62+LINEHEIGHT),priority,font=font_tasks_due_date,fill=white)
        
        if 'due' in task:
            draw.rectangle((518,62+LINEHEIGHT, 630, 78+LINEHEIGHT), fill = black)
            due_date_ev = str(task['due']['string'])
            if (int(due_date_ev[11:13])>11):
                lf = "pm"
            else:
                lf = "am"
            due_date_time = str(int(due_date_ev[11:13])%12)+due_date_ev[13:16]
            if (due_date_time[0:1]=="0"):
                due_date_time = "12" + due_date_time[1:4]
            due_date_day = due_date_ev[8:10]
            due_date_month = months[int(due_date_ev[5:7])-1]
            due_date_fin = due_date_month+" "+due_date_day+" " +due_date_time+" "+lf
            draw.text((523,62.5+LINEHEIGHT),due_date_fin,font=font_tasks_due_date,fill=white)
            print (str(task['due']['string']))
        
        draw.line((250,78+LINEHEIGHT,630,78+LINEHEIGHT),fill=black)
        LINEHEIGHT+=30


    epd.display_frame(epd.get_frame_buffer(image))

    # You can get frame buffer from an image or import the buffer directly:
    #epd.display_frame(imagedata.MONOCOLOR_BITMAP)
if __name__ == '__main__':
    main()
