actions = ['RGB ON', 'RGB OFF', 'RGB RED', 'RGB BLUE', 'RGB GREEN']

def run_rgb_simulator(callback, settings, stop_event, IRcommand_event, mess_queue, publish_event):
    while True:

        if IRcommand_event.is_set():
            data = mess_queue.get()
            try:
                data = int(data)
                if 0 < data < 6:
                    print(actions[data-1])
                    callback(publish_event, actions[data-1], settings)
                IRcommand_event.clear()
            except:
                pass

        if stop_event.is_set():
            break