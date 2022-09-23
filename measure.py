from rs232 import RS_232
from kinesis import KDC
import time
import pandas as pd
import os



def createFolder(abspath: str,folder_path : str ='result\\'):
    path =abspath+folder_path
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(OSError)

def main(num :int =1,file_name :str ='file_name'):
    #NewPort Settings-------------
    print('NewPort Settings...')
    newport = RS_232(port="COM10", baudrate=19200)
    newport.write('WN 2')
    newport.read()
    time.sleep(.25)
    newport.write('WL 650')
    newport.read()
    time.sleep(.25)

    #KDC Settings-------------------------
    kdc = KDC(serial_num='27257082')
    kdc.setController(step_size=360)   
    

    # Measure-----------------------------
    print('Measure Start')
    start = time.time()
    createFolder(abspath,f'result\\{file_name}')
    for i in range(num):
        kdc.goHome()
        time.sleep(.25)

        kdc.moveForward(time_out=0)
        time.sleep(.25)

        Positin =[]
        Power = []
        while kdc.isControllerBusy():
            newport.write(command="SP")
            power =float(newport.read().lstrip('*'))
            pos = kdc.position()
            print(f'Moter Position : {pos} , Power : {power}')
            Positin.append(pos)
            Power.append(power)        
            time.sleep(.1)
       

        df = pd.DataFrame({'Position':Positin,'Power': Power})
        df.to_csv(f'\\result\\{file_name}\\{file_name}_result{str(i+1).zfill(len(str(num)))}.csv', index=False)

    kdc.close()
    newport.close()
    end = time.time()
    print('Measure End')
    print(f'Time : {end - start}sec')
    print('Device close')
    

if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))
    main(num=15,file_name='650nm')