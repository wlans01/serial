import serial


class RS_232:
    def __init__(self, port: str, baudrate: int = 9600, parity: str = "N",
                 bytesize: int = 8, stopbits: serial = serial.STOPBITS_ONE, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.timeout = timeout
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate,
                                 stopbits=self.stopbits, bytesize=self.bytesize, timeout=self.timeout)

    def run(self, command: str):
        self.write(command)
        self.read()

    def write(self, command: str):
        com = f"${command}\r".encode("ascii")
        print(f"command: {com}")
        self.ser.write(com)

    def read(self):
        return self.ser.readlines().decode("ascii")


if __name__ == '__main__':
    rs = RS_232(port="COM8", baudrate=19200)
