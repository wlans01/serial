from rs232 import RS_232
from kinesis import KDC
import time
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


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

    # Measure-----------------------------
    print('Measure Start')
    start = time.time()
    createFolder(abspath, f'\\result\\{wL}nm\\{A}')
    for i in range(num):
        time.sleep(.25)

        kdc.moveForward(time_out=0)
        time.sleep(.25)

        Theta = ['theta', '']
        Power = ["mW", f'{A}']
        while kdc.isControllerBusy():
            newport.write(command="SP")
            power = float(newport.read().lstrip('*'))
            pos = kdc.get_position()
            print(f'Moter Position : {pos} , Power : {power}')
            Theta.append(pos)
            Power.append(power)
            time.sleep(.1)
        time.sleep(1)
        df = pd.DataFrame({'Theta': Theta, 'Power': Power})

        result_dir = abspath + \
            f'\\result\\{wL}nm\\{A}'

        dirListing = os.listdir(result_dir)
        result_len = len(dirListing)

        file_name = result_dir + \
            f'\\{wL}_{A}_{str(result_len+1).zfill(3)}.csv'

        df.to_csv(file_name, index=False, header=True)

    kdc.close()
    newport.close()
    end = time.time()
    print('Measure End')
    print(f'Time : {end - start} sec')
    print('Device close')
    # X = [float(i) for i in Theta[2:]]
    # Y = Power[2:]
    # plt.axes(polar=True)
    # plt.plot(X, Y)


if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))
    main(wL='650', A='', num=1)
