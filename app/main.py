import csv
import datetime as dt
from datetime import datetime
from tkinter import *
from guizero import App, Box, Combo, PushButton, Slider, Text, TextBox, Window
import os
from pathlib import Path
import re
from users import User

### PROGRAM WIDGET FUNCTIONS
##INPUT quintessential data related to WEIGHT
#calculate current & optimal fat level
def calculate_current_fat_lvl():
    global weight
    weight = round(float(opt_fat_lvl_inpu.value), 2)
    global bmr
    bmr = round(weight * 24.2, 2)
    global cal_main_lvl
    cal_main_lvl = round(float(bmr * 1.3), 2)
    global skinfolds_sum
    skinfolds_sum = round(float(cur_fat_lvl_inpu.value), 2)
    if picked_user.sex == "Male":
        body_density = 1.10938 - (0.0008267 * skinfolds_sum) + (0.0000016 * (skinfolds_sum ** 2)) - (0.0002574 * picked_user.age_in_years)
    else:
        body_density = 1.0994921 - (0.0009929 * skinfolds_sum) +  (0.0000023 * (skinfolds_sum ** 2)) - (0.0001392 * picked_user.age_in_years)
    global cur_fat_perc
    cur_fat_perc = round((495 / body_density) - 450, 2)
    global cur_fat_lvl
    cur_fat_lvl = round(weight / 100 * cur_fat_perc, 2)
    global cur_non_fat_perc
    cur_non_fat_perc = round(100 - cur_fat_perc, 2)
    global cur_non_fat_lvl
    cur_non_fat_lvl = round(weight - cur_fat_lvl, 2)
    cur_fat_lvl_disp.value = (f"Your current fat balance is:\n{cur_fat_lvl}kg fat ({cur_fat_perc}%)")
    global min_opt_fat_lvl
    min_opt_fat_lvl = round(weight / 100 * picked_user.minimum_optimal_body_fat_perc, 2)
    global min_opt_non_fat_lvl
    min_opt_non_fat_lvl = round(weight / 100 * (100 - picked_user.maximum_optimal_body_fat_perc), 2)
    global max_opt_fat_lvl
    max_opt_fat_lvl = round(weight / 100 * picked_user.maximum_optimal_body_fat_perc, 2)
    global max_opt_non_fat_lvl
    max_opt_non_fat_lvl = round(weight / 100 * (100 - picked_user.maximum_optimal_body_fat_perc), 2)
    global min_opt_weight
    min_opt_weight = round(((picked_user.height / 100) ** 2) * 18.5, 2)
    global max_opt_weight
    max_opt_weight = round(((picked_user.height / 100) ** 2) * 24.9, 2)
    global nd_weight_loss
    nd_weight_loss = round(float(weight - max_opt_weight), 2)
    global nd_weight_loss_cal
    nd_weight_loss_cal = round(nd_weight_loss * 1000 * 7.716179, 2)
    global nd_fat_loss
    nd_fat_loss = round(cur_fat_lvl - max_opt_fat_lvl, 2)
    opt_fat_lvl_disp.value = (f"Your recommended fat balance range right now is between\n{min_opt_fat_lvl}kg ({round(picked_user.minimum_optimal_body_fat_perc, 2)}%) and\n{max_opt_fat_lvl}kg ({picked_user.maximum_optimal_body_fat_perc}%)\n\n Your optimal weight range (BMI) is between {min_opt_weight} and {max_opt_weight}kg.") 
    #(\nYou would need to lose {nd_fat_loss}kg \nfor a more optimal body fat balance.#)
    bmr_head.value = (f"\n       Without any activity,\nyou should be able to consume up to:\n{cal_main_lvl}kcal\nto preserve your current weight.       ")

##Input Day Activity
def add_activity():
    global activity_vertical_position
    #only once create a textbox with a search command and a desired number of activities
    if not "no_day_activity" in globals():
            global search_textbox
            search_textbox = TextBox(day_activity_box, width=30, command=lambda: text_changed(search_textbox, globals()[f"combo{day_activity_count}"]), grid=[0,vertical1+activity_vertical_position])
            choose_activity_disp = Text(day_activity_box, text="Find and Choose Your Activity:", grid=[0,vertical1+activity_vertical_position-1])
            choose_activity_duration_disp = Text(day_activity_box, text="Enter Activity Duration (in min):", grid=[1,vertical1+activity_vertical_position-1])
    #keep track of how many activities there are
    global day_activity_count
    #You must choose a specific activity, before creating another one & the duration must not be zero
    if day_activity_count > 0:
            if not f"activity{day_activity_count}" in globals() or eval(f"activity_dur{day_activity_count}") == 0:
                no_more_combos_head.value = "You must choose a specific activity\nthat lasts longer than 0 minutes\nbefore adding another one."
                return
            else:
                no_more_combos_head.value = ""
                #disable the previous combo & slider
                globals()[f"slider{day_activity_count+4}"].disable()
    else:
        global no_day_activity
        no_day_activity = False
    #check if there a maximum of 5 activities
    if day_activity_count < 5:  
        #fixing positions of the new activities based on how many there are already
        activity_vertical_position += 2         
        day_activity_count += 1
        globals()[f"combo{day_activity_count}"] = Combo(day_activity_box, options=[], command=lambda var=day_activity_count: item_selected(globals()[f"combo{day_activity_count}"], search_textbox), grid=[0,vertical1+activity_vertical_position+1])
        globals()[f"slider{day_activity_count+4}"] = Slider(day_activity_box, start=0, end=100, grid=[1, vertical1+activity_vertical_position+1], command=lambda: change_passive_to_active_day_activity_ratio(globals()[f"slider{day_activity_count+4}"]))
        globals()[f"activity_dur{day_activity_count}"] = 0
        globals()[f"search_textbox"].enable()
    else: 
        no_more_combos_head.value = "You have reached\n the maximum number of day activities."   

def delete_activity():
    global day_activity_count
    if day_activity_count > 0: 
        global activity_vertical_position
        activity_vertical_position -= 2
        globals()[f"combo{day_activity_count}"].destroy()
        del globals()[f"combo{day_activity_count}"]
        globals()[f"slider{day_activity_count+4}"].destroy()
        del globals()[f"slider{day_activity_count+4}"]
        try:
            del globals()[f"activity{day_activity_count}"]
        except:
            pass
        globals()[f"slider{day_activity_count+3}"].enable()
        day_cal_cons_disp.value = ""
        if day_activity_count == 5:
            no_more_combos_head.value = ""
        day_activity_count -= 1
    elif day_activity_count == 0:    
        del globals()["no_day_activity"]

#calculate the ratio of active vs passive activity time in the day
def change_passive_to_active_day_activity_ratio(slider):
    global passive_time
    global active_time
    #store individual activity duration values under activity_durX
    globals()[f"activity_dur{day_activity_count}"] = slider.value
    #check if one slider is already present (for the slider recalculation of passive_time & active_time)
    if day_activity_count >= 2:
        passive_time = 1440.0 - activity_dur1
        active_time = 0.0 + activity_dur1
        subtract_list = []
        for x in range(1, day_activity_count):
            subtract_list.append(globals()[f"activity_dur{1+x}"])
        for item in subtract_list:
            passive_time -= item
            active_time += item
    else: 
        passive_time = 1440.0
        active_time = 0.0
        passive_time -= globals()[f"activity_dur{day_activity_count}"]
        active_time += globals()[f"activity_dur{day_activity_count}"]

def text_changed(textbox, combo):
    #this populates the combo using a search algorithm; this function will be called when the text in the TextBox changes
    search_term = textbox.value.lower()
    matched_items = {item.lower() for category in met.values() for subcategory in category.values() for item in subcategory if search_term in item.lower()}
    combo.clear()
    for item in sorted(matched_items):
        combo.append(item)

def item_selected(combo, textbox):
    # This function will be called when an item is selected in the Combo
    globals()[f"activity{day_activity_count}"] = combo.value
    print("Selected:", globals()[f"activity{day_activity_count}"])
    globals()[f"combo{day_activity_count}"].disable()
    globals()[f"search_textbox"].disable()
    textbox.clear()

#CALCULATE today's calorie burn
def calculate_day_calorie_burn(): 
    #calculate activity burn of active minutes
    global active_cal_burn
    active_cal_burn = 0
    for x in range(1, day_activity_count+1):
        activity_duration = globals()[f"activity_dur{x}"]
        kind_of_activity = globals()[f"activity{x}"]
        # Find the second layer "met" dictionary key corresponding to the given value
        # Iterate through the dictionary to find the nearest second-layer key for the target value
        activity_met_value = next(
            met_value for met_values_dict in met.values()
            for met_value, activities in met_values_dict.items()
            if kind_of_activity in activities)
        activity_cal_burn = (activity_met_value * 3.5 * weight * activity_duration) / 200
        active_cal_burn += activity_cal_burn
    active_cal_burn = round(active_cal_burn, 2)
    #calculate activity burn of passive minutes
    global passive_cal_burn
    passive_cal_burn = round((1.3 * 3.5 * weight * passive_time) / 200, 2)
    #(=day_cal_main_lvl)
    global total_day_cal_burn
    total_day_cal_burn = round(passive_cal_burn + active_cal_burn, 2)
    #open confirmation info window
    open_info_window1()

def open_info_window1():
    info_window1.show(wait=True)

def info_window1_confirm():
    info_window1.hide()
    globals()[f"slider{day_activity_count+4}"].disable()
    no_more_combos_head.value = (f"With the activity that you performed today,\nyou should be able to consume\nup to {total_day_cal_burn}kcal\nto preserve your current weight.")
    no_more_combos_head.show()

def info_window1_cancel():
    info_window1.hide()
    no_more_combos_head.value = (f"")

#CALCULATE today's calorie deficit
def calculate_day_calorie_deficit():
    #INPUT day calories consumed
    global day_cal_cons
    day_cal_cons = float(day_cal_cons_inpu.value)
    global day_cal_def
    day_cal_def = round(total_day_cal_burn - day_cal_cons, 2)
    global cal_def_dur
    cal_def_dur = abs(round(nd_weight_loss_cal / day_cal_def, 2))
    global nd_day_cal_burn
    nd_day_cal_burn = round(float(abs(day_cal_def) + 200), 2)
    global nd_days_to_opt
    nd_days_to_opt = round(float(nd_weight_loss_cal / 200))
    if day_cal_def <= 0:
        def_or_not = "gained"
        day_encouragement = (f"If you exercise to burn {nd_day_cal_burn} kcal more\n or consume the same amount less tomorrow,\n you can hope to reach your optimal weight in\n {nd_days_to_opt} days.")
    else:
        def_or_not = "burned"
        day_encouragement = (f"If you repeat this every day,\nyou should reach your optimal weight\nin {cal_def_dur} days.")
    day_cal_cons_disp.value = (f"\nToday, you {def_or_not} {abs(day_cal_def)} kcal.\n{day_encouragement}")

##DEVISE AN EXCERCISE PLAN
def recalculate_desired_day_total_calorie_burn():
    global des_day_act_cal_burn
    des_day_act_cal_burn = (slider3.value * 3.5 * weight * slider4.value) / 200
    global des_day_pas_cal_burn
    des_day_pas_cal_burn = (1.3 * 3.5 * weight * (1440 - slider4.value)) / 200
    global des_day_tot_cal_burn
    des_day_tot_cal_burn = des_day_act_cal_burn + des_day_pas_cal_burn

def draft_a_plan():
    try:
        #define necessary variables - desired weight and desired weight loss in calories
        global des_weight
        des_weight = round(float(des_weight_inpu.value), 2)
        global des_weight_loss_cal 
        des_weight_loss_cal = round((weight - des_weight) * 1000 * 7.716179, 2)
        recalculate_desired_day_total_calorie_burn()
        #show sliders 1-4
        items_show(slider1, slider_text1)
        items_show(slider2, slider_text2)
        items_show(slider3, slider_text3)
        items_show(slider4, slider_text4)
        plan_box_complaint.value = (f"")
    except:
        plan_box_complaint.value = (f"You must first calculate\nyour current, optimal fat level\nand enter your desired weight here.")

def report_possibility():
    if slider1.value == 0 or slider2.value == 0:
            extreme_text.value = "Impossible"
    elif slider1.value == 731:
        extreme_text.value = "More than\ntwo years"
    else:
        extreme_text.value = ""
    if slider2.value == 8000:
        extreme_text2.value = "8000 kcal\nor more"
    else:
        extreme_text2.value = ""

def slider1_domino_effect():
    try:
        global des_day_cal_loss
        des_day_cal_loss = round(des_weight_loss_cal / slider1.value, 2)
        global des_day_tot_cal_burn
        slider2.value = des_day_tot_cal_burn - des_day_cal_loss
        report_possibility()
    except:
        extreme_text.value = "Impossible"

def slider2_domino_effect():
    global max_day_cal_cons
    max_day_cal_cons = slider2.value
    global des_day_cal_def
    global des_day_tot_cal_burn
    des_day_cal_def = des_day_tot_cal_burn - max_day_cal_cons
    global des_plan_timespan
    des_plan_timespan = des_weight_loss_cal / des_day_cal_def
    slider1.value = des_plan_timespan
    report_possibility()   

def slider3_domino_effect():
    global des_day_act_cal_burn
    global weight
    try:
        slider4.value = (des_day_act_cal_burn * 200) / (slider3.value * 3.5 * weight)
    except:
        slider4.value = 0

def slider4_domino_effect():
    recalculate_desired_day_total_calorie_burn()
    global des_day_cal_loss
    global des_day_tot_cal_burn
    slider2.value = des_day_tot_cal_burn - des_day_cal_loss
    if slider4.value == 721:
        extreme_text3.value = "More than\n12 hours\nof exercise"
    else:
        extreme_text3.value = ""

##CALCULATE IMPROVEMENT
#CALCULATE improvement from last time
def compare_with_previous():
    file = open(picked_user.csv_file_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    data = []
    one_before_last = None
    last = None
    for line in file:
        one_before_last = last
        last = line
    one_before_last = one_before_last.strip() # strips the line space \n
    one_before_last = one_before_last.split(",") # splits the line at the comma
    data.append(one_before_last)
    last = last.strip() # strips the line space \n
    last = last.split(",") # splits the line at the comma
    data.append(last)
    file.close()
    #check if today's record has been made - necessary precondition
    if todays_date != data[1][0]:
        impr_last_disp.value = (f"You must store today's data first.")
    else:
        #calculate the difference of data between one-before-last record and last record
        #1 Date (DD-MM-YYYY)
        first_date_str = data[0][0]
        first_date_format = '%d-%m-%Y'
        first_date_obj = datetime.strptime(first_date_str, first_date_format)
        day_big_change = abs((today.year - first_date_obj.year) * 365 - (today.month - first_date_obj.month) * 30 - (today.day - first_date_obj.day))
        #2 Weight (in kg)
        weight_big_change = abs(round(float(data[0][1]) - float(data[1][1]), 2))
        if weight_big_change >= 0:
            def_or_not = "lost"
        else:
            def_or_not = "gained"
        #4 Body Fat (in %) & #6 Body Fat (in kg)
        bd_fat_perc_big_change = abs(round(float(data[0][3]) - float(data[1][3]), 2))
        if bd_fat_perc_big_change >= 0:
            drop_or_not = "dropped"
        else:
            drop_or_not = "increased"
        bd_fat_big_change = abs(round(float(data[0][5]) - float(data[1][5]), 2))
        impr_last_disp.value = (f"In {day_big_change} day(s), you have {def_or_not} {weight_big_change}kg.\nYour body fat has {drop_or_not} by {bd_fat_perc_big_change}%,\n         Considering your weight, your fat mass difference\n between today and the day of your last record is {bd_fat_big_change}kg.\n")

#CALCULATE improvement from the beginning
def compare_with_first():
    file = open(picked_user.csv_file_name, "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    data = []
    for line in file:
        line = line.strip() # strips the line space \n
        line = line.split(",") # splits the line at the comma
        data.append(line)
        break
    for line in file:
        pass
    last_line = line
    last_line = last_line.strip() # strips the line space \n
    last_line = last_line.split(",") # splits the line at the comma
    data.append(last_line)
    file.close()
    #check if today's record has been made - necessary precondition
    #formatted_todays_date = todays_date.replace("-", "/")
    if todays_date != data[1][0]:
        impro_first_disp.value = (f"You must store today's data first.")
    else:
        #calculate the difference of data between first record and last record
        #1 Date (DD-MM-YYYY)
        first_date_str = data[0][0]
        first_date_format = '%d-%m-%Y'
        first_date_obj = datetime.strptime(first_date_str, first_date_format)
        day_big_change = abs((today.year - first_date_obj.year) * 365 - (today.month - first_date_obj.month) * 30 - (today.day - first_date_obj.day))
        #2 Weight (in kg)
        weight_big_change = round(float(data[0][1]) - float(data[1][1]), 2)
        if weight_big_change >= 0:
            def_or_not = "lost"
        else:
            def_or_not = "gained"
        weight_big_change = abs(weight_big_change)
        #4 Body Fat (in %) & #6 Body Fat (in kg)
        bd_fat_perc_big_change = round(float(data[0][3]) - float(data[1][3]), 2)
        if bd_fat_perc_big_change >= 0:
            drop_or_not = "dropped"
        else:
            drop_or_not = "increased"
        bd_fat_perc_big_change = abs(bd_fat_perc_big_change)
        bd_fat_big_change = round(float(data[0][5]) - float(data[1][5]), 2)
        bd_fat_big_change = abs(bd_fat_big_change)
        impro_first_disp.value = (f"In {day_big_change} days, you have {def_or_not} {weight_big_change} kg.\nYour body fat has {drop_or_not} by {bd_fat_perc_big_change}%,\n         Considering your weight, your fat mass difference\n between today and the day of your first record is {bd_fat_big_change}kg.\n")

##STORE data in a list, APPEND to CSV
#DATA TO BE STORED
#1 Date (DD-MM-YYYY)
#2 Weight (in kg)
#3 Skinfolds Sum (in mm)
#4 Body Fat (in %)
#5 Fat Free Body Mass (in %)
#6 Body Fat (in kg)
#7 Fat Free Body Mass (in kg)
#8 Actively Burned Day Calories
#9 Passively Burned Day Calories
#10 Total Day Calories Burned
#11 Day Calories Consumed
#12 Day Calorie Deficit

#Check if all calculations have been made
def all_calc_made_or_not():
    try:
        global todays_data_list
        todays_data_list = [str(todays_date),str(weight),str(skinfolds_sum),str(cur_fat_perc),
                str(cur_non_fat_perc),str(cur_fat_lvl),str(cur_non_fat_lvl),
                str(active_cal_burn),str(passive_cal_burn),str(total_day_cal_burn),str(day_cal_cons),str(day_cal_def)]
    except:
        td_data_disp.value = (f"You must first calculate your current & optimal fat level and enter today's activity and calorie consumption.")

def store_todays_data():
    #if clicked upon 2x - do you want to rewrite today's data?
     with open(picked_user.csv_file_name, "r") as file:
        csv_reader = csv.reader(file)
        last_record_date = None
        # Initialize variables for date handling
        # Iterate over the rows to find the last full line
        for line in csv_reader:
            if line:  # Ensure the line is not empty
                last_record_date = line[0][:10]
        if todays_date == last_record_date:
            info_window2.show(wait=True)
        #ONLY IF all values have been assigned
        else:
            store_into_csv()

def store_into_csv():
    all_calc_made_or_not()
    todays_data_var = ",".join(todays_data_list)
    file = open(picked_user.csv_file_name, "a")
    file.write("\n" + todays_data_var)
    file.close()
    td_data_disp.value = (f"Today's data stored.")

def rewrite_todays_data():
    all_calc_made_or_not()
    todays_data_var = ",".join(todays_data_list)
    file = open(picked_user.csv_file_name, "a")
    file.write(todays_data_var)
    file.close()
    td_data_disp.value = (f"Today's data rewriten.")

def rewrite():
    info_window2.hide()
    file = open(picked_user.csv_file_name, "r+")
    lines = file.readlines()
    file.close()
    rewrite = open(picked_user.csv_file_name, 'w')
    for line in lines[:-1]:
        rewrite.writelines(line)
    rewrite.close()
    rewrite_todays_data()

def rewrite_not():
    info_window2.hide()

def items_hide(x, y):
    x.hide()
    y.hide()

def items_show(x, y):
    x.show()
    y.show()

def combo_changed():
    pass

def file_open(file, activity):
    file = open(file, activity)
    return file

def file_close(file): 
    file.close()

def users_load():
    file = file_open("userdata.csv", "r")
    csv_reader = csv.reader(file)
    next(csv_reader)
    for line in csv_reader:
        combo6.append(line[0])
    file_close(file)

def user_pick(): # =user login
    picked_user_str = combo6.value
    file = file_open("userdata.csv", "r")
    csv_reader = csv.reader(file)
    for line in csv_reader:
        if line[0] == picked_user_str:
            global picked_user 
            picked_user = User(line[0], line[1], float(line[2]), line[3])
            print(picked_user.username, picked_user.sex, picked_user.height, picked_user.birthdate, picked_user.age)
            print(picked_user)
            break
    #update window2, store age in years and birthdate
    welcome.value = f"Welcome, {picked_user.username}!"
    # check if a CSV database for the user already exists and if not, create one
    calculations = ["Date (DD/MM/YYYY)", "Weight (in kg)","Skinfolds Sum (in mm)","Body Fat (in %)", 
                    "Fat Free Body Mass (in %)","Body Fat (in kg)","Fat Free Body Mass (in kg)",
                    "Day Activity","BMR","Day Calories Burned","Day Calories Consumed", "Day Fat Burned"
                    ]
    picked_user.check_and_create_csv(calculations)
    #Proceed to the next window/page/box
    window1.hide()
    window2.show()

def user_logout():
    window2.hide()
    window1.show()

def height_chosen():
    pass

#Function to be called when the "Register" button is pressed
def user_register():
    #check existing usernames
    username = textbox1.value
    #if there are not yet in existence & there is no presence of forbidden symbols (ASCII & NO spaces)
    if not username.isalnum() or ' ' in username:
        username_taken_text.value = "Username contains symbols other than numbers or letters (including spaces). Please change it."
        return
    with open("userdata.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            if line:
                if line[0] == username:
                    username_taken_text.value = "This username is already in use.\n Try a different one."
                    return
    #store user data
    day = day_combo.value
    month = month_combo.value
    year = year_combo.value
    dob = f"{day}/{month}/{year}"
    #Create an instance of the User class
    new_user = User(textbox1.value, str(combo7.value), slider10.value, dob)
    # List of attribute names to extract values from the instance
    user_data_list = [new_user.username, new_user.sex, str(new_user.height), new_user.birthdate, str(new_user.age)]
    #Store data under the last record
    new_user_data = "\n" + ",".join(user_data_list)
    file = open("userdata.csv", "a")
    file.write(new_user_data)
    #STORE Alphabetically
        #
        #
    file.close()
    users_load()
    username_taken_text.value = (f"User successfully registered.")
            
##Store variables
todays_date = dt.date.today().strftime("%d-%m-%Y") #this is a string
today = dt.date.today() #this is an object
vertical1 = 0 #grid position1
vertical2 = 11 #grid position2
active_cal_burn = ""
passive_cal_burn = ""
total_day_cal_burn = ""
day_cal_cons = ""
day_cal_def = ""

##Store global lists & dictionaries
#Create MET categories dictionary to calculate active calorie burn
#SEDENTARY <1.6
   #1.0 - sitting quietly, 1.5 - intense brain activity
#LIGHT 1.6-3
    #2.3, 2.5, 2.8, 2.9
#MODERATE 3-6 (up to 60 minutes)
    #3.0, 3.3, 3.5, 3.8, 4.0, 4.3, 4.4, 4.5, 4.8, 5.0, 5.3, 5.5, 5.8, 6.0
#VIGOROUS 6-9 (up to 30 minutes)
    #6.5, 7.0, 8.0, 8.5, 9.0
#HIGH >9 (up to 10 minutes)
    #10.0, 11.0, 12.0, 12.5, 14.0, 16.0, 16.5
met = {
    'sedentary': {
        1.0: ['sitting quietly'],
        1.3: ['moderate brain activity'],
        1.5: ['intensive brain activity']
    },
    'light': {
        2.3: ['light gardening'],
        2.5: ['canoeing leisurely',
               'general cleaning & straightening up',
               'light housework',
               'playing catch',
               'putting away groceries',
               'standing',
               'stretching/yoga',
               'washing dishes & clearing the table'],
        2.8: ['walking at a moderate pace (3.22 km/h)'],
        2.9: ['dancing at a moderate pace']
    },
    'moderate': {
        3.0: ['canoeing at 6.44 km/h',
              'individual bowling'],
        3.3: ['walking at a brisk pace (4.83 km/h)'],
        3.5: ['archery',
              'light/moderate calisthenics',
              'walking and standing'],
        3.8: ['scrubbing the floor'],
        4.0: ['active gardening',
              'gardening',
              'horseback riding',
              'light to moderate gymnastics',
              'raking the lawn',
              'table tennis',
              'Tai chi',
              'weeding'],
        4.3: ['multiple household tasks with vigorous effort'],
        4.5: ['badminton',
              'basketball - shooting baskets',
              'jumping on a minitrampoline',
              'swift dancing',
              'swimming at a slower pace'],
        4.8: ['fast dancing'],
        5.0: ['aerobic dance - low impact',
              'baseball/softball',
              'kayaking',
              'skateboarding',
              'snorkeling',
              'sports fast walking (6.44 km/h)',
              'tennis - doubles (2 vs 2 players)',
              'walking at a moderate pace with 7kg weight'],
        5.3: ['walking uphill (3-5%) at a brisk pace (4.83 km/h)'],
        5.5: ['mowing the lawn'],
        5.8: ['biking/cycling at a pace of 14.5-16 km/h',
              'moving furniture and carrying boxes'],
        6.0: ['chopping wood',
              'downhill skiing',
              'fencing',
              'intensive dancing, aerobic or ballet',
              'moderate judo/karate/wrestling training',
              'shoveling snow',
              'surfing',
              'walking uphill at a very fast pace (6.44 km/h)',
              'water skiing',
              'weight lifting/heavy workout']
    },
    'vigorous': {
        6.5: ['aerobic dance - moderate impact',
              'swimming at a moderate pace'],
        7.0: ['',
              'active ice skating',
              'active roller skating',
              'aerobic dance - high impact',
              'cross country skiing - lightly moderate',
              'football/soccer - moderate',
              'swimming laps - moderate pace',
              'tennis (1 vs 1 player)',
              'walking at a moderate pace (4.83km/h) with a frame backpack of 7kg'],
        8.0: ['a game of basketball',
              'biking/cycling at a pace of 19-21 km/h',
              'cross country skiing - moderate pace',
              'field/ice hockey',
              'heavy calisthenics',
              '(mountain) climbing',
              'lacrosse',
              'logging/felling trees',
              'rope skipping - slow pace',
              'slower jogging - 8 km/h',
              'snowshoeing',
              'team racquetball',
              'ultimate frisbee',
              'walking up stairs',
              'water jogging'],
        8.5: ['aerobic stepping - 15-20 cm'],
        9.0: ['american football - competitive pace',
              'cross country skiing - fast pace (50% race tempo)']
    },
    'high': {
        10.0: ['football/soccer - competitive pace',
               'individual racquetball',
               'intensive judo/karate/wrestling training',
               'running - 9.66 km/h (6 min/km)',
               'swimming laps - fast pace',
               'water polo - competitive pace'],
        11.0: ['running - 10.7 km/h (5.6 min/km)'],
        12.0: ['cross country skiing uphill - 75% tempo',
               'rollerblading - fast pace'
               'rope skipping - fast pace'],
        12.5: ['running - 12 km/h (5 min/km)',
               'skin diving'],
        14.0: ['running - 13.75 km/h (4.35 min/km)'],
        16.0: ['biking/cycling at a pace of 32+ km/h',
               'running - 16 km/h (3.73 min/km)'],
        16.5: ['cross country skiing uphill - race tempo']
    }
}

###MAIN APP GUI
app = App(title="Fat Burner", width=1100, height=830)

####LOGIN WINDOW
window1 = Box(app)
text1 = Text(window1, "Login")
text2 = Text(window1, "Choose user:")
combo6 = Combo(window1, options=[], command=user_pick)
users_load()
text3 = Text(window1, "\n\n\nRegister a new user")
text4 = Text(window1, "Please enter your username:")
textbox1 = TextBox(window1)
text5 = Text(window1, "Please choose your sex:")
combo7 = Combo(window1, options=["Female", "Male"], command=combo_changed)
text6 = Text(window1, "Please choose your height in cm:")
slider10 = Slider(window1, start=0, end=250, command=height_chosen)
# Create text labels and combo boxes for day, month, and year
Text(window1, text="Select your date of birth:")
Text(window1, text="Day:")
day_combo = Combo(window1, options=[str(i) for i in range(1, 32)])
Text(window1, text="Month:")
month_combo = Combo(window1, options=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
Text(window1, text="Year:")
year_combo = Combo(window1, options=[str(i) for i in range(1900, 2024)])
# Create a submit button
submit_button = PushButton(window1, text="Register", command=user_register)
username_taken_text = Text(window1, text="")

###MAIN WINDOW
window2 = Box(app, visible=False)

##WELCOME BOX
welcome_box = Box(window2, width="fill", align="top")
welcome = Text(welcome_box, text=(f""))

##STORE DATA BOX
store_data_box = Box(window2, align="bottom")
button = PushButton(store_data_box, command=store_todays_data, text="Store Today's Data")
info_window2 = Window(store_data_box, title="Attenzione", width=300, height=200)
info_window2.hide()
info_text = Text(info_window2, text="      Today's record has already been made.\nDo you want to rewrite today's data?", align="top")
button = PushButton(info_window2, command=rewrite, text="      Yes      ", align="left")
button = PushButton(info_window2, command=rewrite_not, text="      No      ", align="right")
td_data_disp = Text(store_data_box, text ="")
button = PushButton(store_data_box, command=user_logout, text="      Change User      ", align="bottom")

##PLAN BOX
bottom_functions_box = Box(window2, width="fill", align="bottom")
plan_box = Box(bottom_functions_box, align="left", layout="grid", border=True)
plan_box_complaint = Text(plan_box, "", grid=[2, 3])
plan_box_text = Text(plan_box, "Enter your desired weight in kg:", grid=[2, 4], align="right")
des_weight_inpu = TextBox(plan_box, grid=[3, 4])
button = PushButton(plan_box, command=draft_a_plan, text="Draft My Weight Change Plan", grid=[4, 4])
slider_text1 = Text(plan_box, "Length of Weight Change Plan in Days", grid=[2, 5])
extreme_text = Text(plan_box, "", grid=[3, 6])
slider1 = Slider(plan_box, start=0, end=731, grid=[2, 6], command=slider1_domino_effect)
items_hide(slider1, slider_text1)
extreme_text2 = Text(plan_box, "", grid=[3, 8])
slider_text2 = Text(plan_box, "Maximum Daily Calorie Consumption", grid=[2, 7])
slider2 = Slider(plan_box, start=0, end=8000, grid=[2, 8], command=slider2_domino_effect)
items_hide(slider2, slider_text2)
slider_text3 = Text(plan_box, "Daily Exercise Intensity (MET)", grid=[4, 5])
slider3 = Slider(plan_box, start=0, end=17, grid=[4, 6], command=slider3_domino_effect)
items_hide(slider3, slider_text3)
extreme_text3 = Text(plan_box, "", grid=[3, 10])
slider_text4 = Text(plan_box, "Daily Exercise Length in Minutes", grid=[4, 7])
slider4 = Slider(plan_box, start=0, end=721, grid=[4, 8], command=slider4_domino_effect)
items_hide(slider4, slider_text4)

##BASIC DATA BOX
skinfold_weight_box = Box(window2, height="fill", align="left", layout="grid", border=True)
cur_fat_lvl_head = Text(skinfold_weight_box, text=(f"        Please enter the sum of your three skinfold areas in milimeters (mm):"), grid=[0,vertical1])
cur_fat_lvl_inpu = TextBox(skinfold_weight_box, grid=[0,vertical1+1])
opt_fat_lvl_head = Text(skinfold_weight_box, text=(f"Please enter your weight in kilograms (kg):"), grid=[0,vertical1+2])
opt_fat_lvl_inpu = TextBox(skinfold_weight_box, grid=[0,vertical1+3])
button = PushButton(skinfold_weight_box, command=calculate_current_fat_lvl, text="Calculate My Current & Optimal Fat Level", grid=[0,vertical1+4])
cur_fat_lvl_disp = Text(skinfold_weight_box, text ="", grid=[0,vertical1+5])
opt_fat_lvl_disp = Text(skinfold_weight_box, text ="", grid=[0,vertical1+6])
bmr_head = Text(skinfold_weight_box, text="", grid=[0,vertical1+7])

##DAY ACTIVITY BOX
day_activity_box = Box(window2, layout="grid", height="fill", align="right", border=True)
combo1_head = Text(day_activity_box, text=(f"Please list all activities you did today:"), grid=[0,vertical1])
button = PushButton(day_activity_box, command=add_activity, text="Add an activity", grid=[0,vertical1+1])
button = PushButton(day_activity_box, command=delete_activity, text="Delete an activity", grid=[1,vertical1+1])
day_activity_count = 0
activity_vertical_position = 3
no_more_combos_head = Text(day_activity_box, text="", grid=[0,vertical1+activity_vertical_position+22])
day_cal_burn_button = PushButton(day_activity_box, command=calculate_day_calorie_burn, text="Calculate Your\nCalorie Burn for Today", grid=[1,vertical1+activity_vertical_position+22])
passive_time = 1440.0
active_time = 0.0
info_window1= Window(day_activity_box, title="Attenzione", width=300, height=200)
info_window1.hide()
info_text = Text(info_window1, text="      Are you sure\nyou have included\nall today's activities?", align="top")
button = PushButton(info_window1, command=info_window1_confirm, text="      Yes      ", align="left")
button = PushButton(info_window1, command=info_window1_cancel, text="      No      ", align="right")
day_cal_cons_head2 = Text(day_activity_box, text="\n Please enter the number of kcal\n you consumed today:", grid=[0,vertical1+26])
day_cal_cons_disp = Text(day_activity_box, text="", grid=[1,vertical1+26])
day_cal_cons_inpu = TextBox(day_activity_box, grid=[0,vertical1+27])
button = PushButton(day_activity_box, command=calculate_day_calorie_deficit, text="Calculate Today's\nCalorie Deficit", grid=[0,vertical1+28])

##IMPROVEMENT BOX
improv_box = Box(bottom_functions_box, layout="grid", border=True, align="right")
invisible_head = Text(improv_box, text=(f"                          "), grid=[0,vertical2])
button = PushButton(improv_box, command=compare_with_previous, text="      Calculate My Improvement from Last Time       ", grid=[0,vertical2+1])
impr_last_disp = Text(improv_box, text ="", grid=[0,vertical2+2])
button = PushButton(improv_box, command=compare_with_first, text="      Calculate My Overall Improvement      ", grid=[0,vertical2+3])
impro_first_disp = Text(improv_box, text ="", grid=[0,vertical2+4])
window2.hide()

app.display()

