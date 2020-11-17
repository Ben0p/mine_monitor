from PIL import Image
import numpy as np


def grouper(n, iterable):
    ''' Groups every 2 integers in long tuple array to a list of tuples of 2 integers
        (45, 256, 95, 77) -> ((45, 256),(95, 77))
    '''
    args = [iter(iterable)] * n
    as_list = list(zip(*args))
    return(as_list)


def pack(tup) :
    ''' Combines two uinit8 integers into one uint16 integer
    '''
    sum = 0
    for i in range(len(tup)) :
        sum |= tup[i]<<(8*i)
    return(sum)


def process(thumbnails):
    ''' Converts integer uint8 array into an actual .png
        Saves to ./thumbnails
    '''


    for thumbnail in thumbnails:

        # Remove first four bytes for some reason
        image_bytes = thumbnail['data'][4:]

        # Group into tuples of length 2
        grouped = grouper(2, image_bytes)

        new_array = []
        for group in grouped:
            packed = pack(group)
            new_array.append(packed)
        
        np_array = np.array(new_array)
        np_array = np_array.reshape([320,240])

        ba = bytearray(np_array.astype(np.uint16))
        ba = bytes(ba)

        im = Image.frombuffer('RGB', (320,240), ba, 'raw', 'BGR;16', 0, 1)
        im.save(f"thumbnails/{thumbnail['name']}.png")