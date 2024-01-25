import time 

def run_lcd_sim(stop_event, mess_queue, lcd_event):
    while True:
        if lcd_event.is_set():
            data = mess_queue.get()
            print('LCD: Temp: ' + str(data[0]) +'\n' )# display CPU temperature
            print( 'LCD Hum:' + str(data[1]) ) 
            lcd_event.clear()
        time.sleep(1)
        if stop_event.is_set():
            break
