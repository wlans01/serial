from rs232 import RS_232
from kinesis import KDC
import time
import pandas as pd

def main():
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
    print('Measure End')
    kdc.close()
    newport.close()
    print('Device close')

    df = pd.DataFrame({'Position':Positin,'Power': Power})
    print(df)
    df.to_csv('result.csv', index=False)



if __name__ == "__main__":
    main()