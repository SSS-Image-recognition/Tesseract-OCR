import struct
from PIL import Image
import os
"""
filename = '/Users/okamotoyuutarou/Downloads/unpack/ETL9B'

for root, dirs, files in os.walk(filename):
    for f in sorted(files):
        filepath = os.path.join(root, f)
        print('root : ',root)
        print('dirs : ',dirs)
        print('f : ',f)
        print('filepath : ',filepath)
        
        #sum_datasets = 40
        sum_datasets = 1
        sum_words = 3036
        record_size = 576

        for ds_idx in range(1, sum_datasets+1):
            for word_idx in range(1, sum_words+1):               
                with open(filepath, 'rb') as f:
                    f.seek(ds_idx * record_size * word_idx)
                    s = f.read(record_size)
                    r = struct.unpack('>2H4s504s64x', s)
                    i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
                    file_name = 'ETL9B_{}_{}_{}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:], ds_idx)
                    dir_name = "../data/ETL9B/{}".format(hex(r[1])[-4:])
                    
                    os.makedirs(dir_name, exist_ok=True)
                    i1.save(os.path.join(dir_name, file_name), 'PNG')

"""


sum_datasets = 40
#sum_datasets = 1
sum_words = 3036
record_size = 576
files = ['/Users/okamotoyuutarou/Downloads/unpack/ETL9B/ETL9B_1',
         '/Users/okamotoyuutarou/Downloads/unpack/ETL9B/ETL9B_2',
         '/Users/okamotoyuutarou/Downloads/unpack/ETL9B/ETL9B_3',
         '/Users/okamotoyuutarou/Downloads/unpack/ETL9B/ETL9B_4',
         '/Users/okamotoyuutarou/Downloads/unpack/ETL9B/ETL9B_5',
         ]

for filepath in files:
    for ds_idx in range(1, sum_datasets+1):
        for word_idx in range(1, sum_words+1):               
            with open(filepath, 'rb') as f:
                f.seek(ds_idx * record_size * word_idx)
                s = f.read(record_size)
                r = struct.unpack('>2H4s504s64x', s)
                i1 = Image.frombytes('1', (64, 63), r[3], 'raw')
                file_name = 'ETL9B_{}_{}_{}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:], ds_idx)
                dir_name = "../data/ETL9B/{}".format(hex(r[1])[-4:])
                
                os.makedirs(dir_name, exist_ok=True)
                print(dir_name)
                i1.save(os.path.join(dir_name, file_name), 'PNG')