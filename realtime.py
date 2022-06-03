from threading import Thread

from receiver import ProxyReceiver


class Object():

    def __init__(self, id) -> None:
        self.id = id

    def update_last_sendign_time(self, time):
        self.last_sending_time = time


def get_object_ids(data):
    return list(data.keys())[1:]


def get_time(data):
    return data['time']


def on_data_recieved(data):
    if(data):
        init_objects_not_in_list(data)
        update_objects_last_sending_time(data)
        detect_objects_liveliness(get_time(data))


def detect_objects_liveliness(last_time):
    for o in objects:
        time_not_sending = last_time - o.last_sending_time
        if time_not_sending > 10 and time_not_sending < 12:
            print(f"{last_time}  Detected: Object {o.id} not sending data")


def update_objects_last_sending_time(data):
    for object_id in get_object_ids(data):
        o = get_object_by_id(object_id)
        if(o):
            o.update_last_sendign_time(get_time(data))


def init_objects_not_in_list(data):
    for object_id in get_object_ids(data):
        if(not object_in_list(object_id)):
            o = Object(object_id)
            objects.append(o)


def object_in_list(id):
    for o in objects:
        if o.id == id:
            return True


def get_object_by_id(id):
    for o in objects:
        if(o.id == id):
            return o


objects = []


def main():
    receiver = ProxyReceiver()
    Thread(target=receiver.listen, args=(on_data_recieved,)).start()


if __name__ == "__main__":
    main()
