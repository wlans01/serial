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


class KDC:
    def __init__(self, serial_num: str, device_settings_name: str = 'PRM1-Z8'):
        DeviceManagerCLI.BuildDeviceList()
        self.controller = self.connectDevice(serial_num, device_settings_name)

    def connectDevice(self, serial_num, device_settings_name):
        controller = KCubeDCServo.CreateKCubeDCServo(serial_num)

        if not controller == None:
            controller.Connect(serial_num)

            if not controller.IsSettingsInitialized():
                print('Initializing Moter...')
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

        return controller

    def setController(self, step_size: int = 360, max_velocity: int = 20) -> None:
        self.controller.SetJogStepSize(Decimal(step_size))
        self.controller.SetJogVelocityParams(Decimal(15), Decimal(20))

        print(f'Step Size : {self.controller.GetJogStepSize()}')
        print(
            f'Max Velocity : {self.controller.GetVelocityParams().MaxVelocity}')
        print(
            f'Min Velocity : {self.controller.GetVelocityParams().MinVelocity}')

    def moveForward(self, time_out: int = 60000) -> None:
        print('Moving Moter...')
        self.controller.MoveJog(MotorDirection.Forward, time_out)

    def goHome(self, time_out: int = 60000) -> None:
        print('Homing Moter...')
        self.controller.Home(time_out)

    def get_position(self) -> Decimal:
        pos = self.controller.Position
        return pos

    def move(self, pos, time_out: int = 60000) -> None:
        print('Moving Moter...')
        self.controller.MoveTo(Decimal(pos), time_out)

    def isControllerBusy(self):
        return self.controller.IsDeviceBusy

    def close(self) -> None:
        self.controller.StopPolling()
        self.controller.Disconnect(False)


if __name__ == "__main__":
    # main()
    kdc = KDC(serial_num='27257082')
    kdc.setController()
    kdc.goHome()
    # for i in range(50):
    #     kdc.moveForward()
    #     time.sleep(.1)
    # kdc.goHome()
    # kdc.move(70)
    kdc.moveForward() 
    kdc.close()
