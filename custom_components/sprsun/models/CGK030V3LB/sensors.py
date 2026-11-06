SENSORS = [
    {
        "unique_id": "d07_zaw_3_drog",
        "name": "Zawór trójdrogowy pozycja",
        "register": 5,
        "bit": 6
        "source": "discrete_input",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "C.O.",
            1: "C.W.U.",
        },
        "icon_map": {
            1: "mdi:valve-open",
            2: "mdi:valve-closed",
        },
    },

]

DATA = SENSORS
