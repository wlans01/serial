import serial

# newprot1919R과 serial 통신을 위한 RS_232 통신 규칙
# 1. ascii
# 2. 명령어의 잡미사 $ 추가
# 3. 명령어의 접두사 /n 추가
# 4. RS232 통신의 경우 접두사 /r 추가


class RS_232:
    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        parity: str = "N",
        bytesize: int = 8,
        stopbits: serial = serial.STOPBITS_ONE,
        timeout: int = 1,
    ):

        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )

    def get_power(self):
        self.write("SP")
        return self.read()

    def write(self, command: str) -> None:
        com = f"${command}\r".encode("ascii")
        self.ser.write(com)

    def read(self) -> str:
        res = self.ser.readline().decode("ascii")
        return res

    def close(self) -> None:
        self.ser.close()


if __name__ == "__main__":
    rs = RS_232(port="COM13", baudrate=19200)
    rs.write(f"WL 650")
    res = rs.read()

    rs.write("WN 3")
    res = rs.read()

    # rs.write('SP')
    # res = rs.read()
    print(res)
    rs.close()
