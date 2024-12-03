
def run_ir_simulator(callback, settings, stop_event, IRcommand_event, mess_queue, publish_event):
    while True:

        # if IRcommand_event.is_set():
        #     data = mess_queue.get()
        #     print(data)
        #     callback(publish_event, data, settings)

        if stop_event.is_set():
            break