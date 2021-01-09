
from morse_burger_light_base64 import load_image_base64, mos_burger
from tello_manager import *
from multi_tello_test import *

MORSE = '0TQZH5PED006XH'
GREEN_RED = '0TQZH5PED006SS'
CHINESE = '0TQZH5NED005FG'

BATTERY_THRESHOLD = 30

def put_queue_and_wait(action, manager, execution_pools):
    for queue in execution_pools:
        queue.put(action)

    while not all_queue_empty(execution_pools):
        time.sleep(0.5)
    
    time.sleep(1)

    while not all_got_response(manager):
        time.sleep(0.5)

def main(): 
    manager = Tello_Manager()
    manager.find_avaliable_tello(1)
    tello_list = manager.get_tello_list()
    execution_pools = create_execution_pools(1)
    ip_fid_dict = {}
    id_sn_dict = {}
    id_sn_dict[0] = MORSE
    sn_ip_dict = {}

    t = Thread(target=drone_handler, args=(tello_list[0], execution_pools[0]))
    ip_fid_dict[tello_list[0].tello_ip] = 0
    t.daemon = True
    t.start()
    
    # correct ip
    put_queue_and_wait('sn?', manager, execution_pools)

    for tello_log in list(manager.get_log().values()):
        sn = str(tello_log[-1].response)
        tello_ip = str(tello_log[-1].drone_ip)
        sn_ip_dict[sn] = tello_ip

    # battery check
    put_queue_and_wait('battery?', manager, execution_pools)

    for tello_log in list(manager.get_log().values()):
        battery = int(tello_log[-1].response)
        print(('[Battery_Show]show drone battery: %d  ip:%s\n' % (battery,tello_log[-1].drone_ip)))
        if battery < BATTERY_THRESHOLD:
            print(('[Battery_Low]IP:%s  Battery < Threshold. Exiting...\n'%tello_log[-1].drone_ip))
            save_log(manager)
            exit(0)

    # test command
    reflec_ip = sn_ip_dict[MORSE]
    fid = ip_fid_dict[reflec_ip]
    execution_pools[0].put("command")
    time.sleep(10)

if __name__ == "__main__":
    main()
