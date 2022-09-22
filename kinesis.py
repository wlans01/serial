"""An example that uses the .NET Kinesis Libraries to connect to a KDC."""
import os
import time
import clr
import datetime
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference(
    "C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.DCServoCLI.dll")

from Thorlabs.MotionControl.KCube.DCServoCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.DeviceManagerCLI import *
from System import Decimal

def getDeviceList():
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()

def main():
    """The main entry point for the application"""

    # 모델 번호
    # serial_num = str('27257082')

    DeviceManagerCLI.BuildDeviceList()
    print(f'연결된 장치 : {DeviceManagerCLI.GetDeviceList()}')
    serial_num =str('27257082')
    
    controller = KCubeDCServo.CreateKCubeDCServo(serial_num)
    

    if not controller == None:
        controller.Connect(serial_num)

        if not controller.IsSettingsInitialized():
            controller.WaitForSettingsInitialized(3000)

        controller.StartPolling(50)
        time.sleep(.1)
        controller.EnableDevice()
        time.sleep(.1)

        config = controller.LoadMotorConfiguration(
            serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str('PRM1-Z8')
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)

        print('Homing Moter')
        controller.Home(60000)

        jog_params = controller.GetJogParams()
        jog_params.MaxVelocity = Decimal(20)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        controller.SetJogParams(jog_params)

        print('Moving Motor')
        # controller.MoveJog(MotorDirection.Forward, 60000)
        controller.MoveTo(Decimal(180),0)
        print(controller.Position)

        controller.StopPolling()
        controller.Disconnect(False)
        print("close")

class KDC:
    def __init__(self,serial_num: str,device_settings_name:str ='PRM1-Z8'):
        DeviceManagerCLI.BuildDeviceList()
        self.controller = self.connectDevice(serial_num,device_settings_name)

    


    def connectDevice(self, serial_num,device_settings_name):
        controller = KCubeDCServo.CreateKCubeDCServo(serial_num)

        if not controller == None:
            controller.Connect(serial_num)

            if not controller.IsSettingsInitialized():
                print('Initializing Moter')
                controller.WaitForSettingsInitialized(3000)

            controller.StartPolling(50)
            time.sleep(.1)
            controller.EnableDevice()
            time.sleep(.1)

            config = controller.LoadMotorConfiguration(
            serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
            config.DeviceSettingsName = device_settings_name
            config.UpdateCurrentConfiguration()
            controller.SetSettings(controller.MotorDeviceSettings, True, False)

            print('Homing Moter')
            controller.Home(60000)

        return controller

    def setController(self,step_size : int=  360 ,max_velocity : int=20 ):
        # jog_params = self.controller.GetJogParams()
        # jog_params.SetpSize = Decimal(45)
        # jog_params.MaxVelocity = Decimal(max_velocity)
        # jog_params.JogMode = JogParametersBase.JogModes.SingleStep
        # self.controller.SetJogParams(jog_params)
        self.controller.SetJogStepSize(Decimal(step_size))
        self.controller.SetJogVelocityParams(Decimal(15),Decimal(20))
        print(f'Step Size : {self.controller.GetJogStepSize()}')
        print(f'Max Velocity : {self.controller.GetVelocityParams().MaxVelocity}')
        print(f'Min Velocity : {self.controller.GetVelocityParams().MinVelocity}')

    def goHome(self,time_out :int = 60000):
        self.controller.Home(time_out)

    def move(self,pos, time_out :int = 60000):
        print('Moving Moter...')
        self.controller.MoveTo(Decimal(pos),time_out)


    def moveForward(self,time_out :int = 60000):
        print('Moving Moter...')
        self.controller.MoveJog(MotorDirection.Forward, time_out)

    def isControllerBusy(self):
        return self.controller.IsDeviceBusy

    def position(self):
        pos = self.controller.Position
        return pos

    def close(self):
        self.controller.StopPolling()
        self.controller.Disconnect(False)


if __name__ == "__main__":
    # main()
    kdc = KDC(serial_num='27257082')
    kdc.setController()
    start = datetime.datetime.now()
    kdc.move(time_out=60000)
    end = datetime.datetime.now()
    print(end -start)
    kdc.position()   
    kdc.close() 
