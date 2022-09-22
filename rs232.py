import serial

# newprot1919R과 serial 통신을 위한 RS_232 통신 규칙
# 1. ascii
# 2. 명령어의 잡미사 $ 추가
# 3. 명령어의 접두사 /n 추가
# 4. RS232 통신의 경우 접두사 /r 추가


class RS_232:
    def __init__(self, port: str, baudrate: int = 9600, parity: str = "N",
                 bytesize: int = 8, stopbits: serial = serial.STOPBITS_ONE, timeout: int = 1):

        self.ser = serial.Serial(port=port, baudrate=baudrate,
                                 stopbits=stopbits, bytesize=bytesize, timeout=timeout)


    # pyserial이 알아서 /n 넣어줌 필요 x
    def write(self, command: str):
        com = f"${command}\r".encode("ascii")
        self.ser.write(com)

    def read(self):
        res = self.ser.readline().decode("ascii")
        return res

  

    def close(self):
        self.ser.close()


if __name__ == '__main__':
    rs = RS_232(port="COM10", baudrate=19200)
    # rs.setWaveLength(650)
    rs.write("WN 2")
    res =rs.read()
    print(res)
    rs.close()
