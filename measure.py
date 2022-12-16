from rs232 import RS_232
from kinesis import KDC
from origin import OriginPy
import time
import pandas as pd
import os
import numpy as np
import math


def createFolder(abspath: str, folder_path: str = 'result\\') -> None:
    path = abspath+folder_path
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(OSError)


def newPortSettings(newport: RS_232, wL: str) -> None:
    '''
    NewPort Settings

    Parameters:
        newport : RS_232 => RS_232 instance
        wL : str => waveLength

    Returns:
        None
    '''
    print('NewPort Settings...')

    # newport 측적 범위
    ar = [30, 3, 300e-3, 30e-3, 300e-6, 30e-6]
    wn = -1

    # 측정 파장 설정
    newport.write(f'WL {wL}')
    newport.read()
    time.sleep(.25)

    # 측정 범위 Auto 변경
    # newport.write(f'WN {wn}')
    # newport.read()
    # time.sleep(2)

    # # 측정값으로 측정 범위 설정하기
    # newport.write(command="SP")
    # power = float(newport.read().lstrip('*'))

    # for i, e in enumerate(ar):
    #     if power < e:
    #         wn = i
    # time.sleep(.25)

    # newport.write(f'WN {wn}')
    # newport.read()
    # time.sleep(.25)


def main(wL: str, A: str, num: int = 1) -> None:
    '''
    Measure Laser Polarization

    Parameters:
        wL : str => waveLength
        A : str => Laser Power (Supply Power)
        num : int = 1 => Number of Measurements

    Returns:
        None
    '''
    # NewPort Settings-------------
    newport = RS_232(port="COM13", baudrate=19200)
    newPortSettings(newport=newport, wL=wL)

    # KDC Settings-------------------------
    kdc = KDC(serial_num='27257082')
    kdc.setController(step_size=360)
    # kdc.goHome()

    op = OriginPy()
    # Measure-----------------------------
    print('Measure Start')
    start = time.time()
    createFolder(abspath, f'\\result\\{wL}nm\\{A}')
    createFolder(abspath, f'\\result_img\\{wL}nm\\{A}')
    for i in range(num):
        time.sleep(.25)

        kdc.moveForward(time_out=0)
        time.sleep(.25)

        Theta = []
        Power = []
        while kdc.isControllerBusy():
            newport.write(command="SP")
            power = float(newport.read().lstrip('*'))
            posKDC = float(str(kdc.get_position()))
            pos = posKDC - 4 if posKDC -4 > 0 else 356+posKDC
            # pos = posKDC
            print(f'Moter Position : {pos} , Power : {power}')
            Theta.append(pos)
            Power.append(power)
            time.sleep(.1)
        time.sleep(1)
        df = pd.DataFrame({'Theta': Theta, 'Power': Power})

        max_intensity = max(Power)

        result_dir = abspath + \
            f'\\result\\{wL}nm\\{A}'
        
        result_img_dir = abspath + \
            f'\\result_img\\{wL}nm\\{A}'
        

        dirListing = os.listdir(result_dir)
        result_len = len(dirListing)

        file_name = result_dir + f'\{wL}_{A}_{max_intensity}_{str(result_len+1).zfill(2)}.csv'
            

        img_file_name =result_img_dir + f'\{wL}_{A}_{str(result_len+1).zfill(2)}.png'
            


        df.to_csv(file_name, index=False, header=True)
        op.draw_graph(Theta,Power,f'{A}_{str(result_len+1).zfill(2)}',img_file_name)
        
        time.sleep(0.2)

    kdc.close()
    newport.close()
    end = time.time()
    print('Measure End')
    print(f'Time : {end - start} sec')
    print('Device close')
  


if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))
    main(wL='650', A='test', num=1)
