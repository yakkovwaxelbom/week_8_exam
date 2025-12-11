class AnalysisIp:
    def __init__(self, ip: list[int], mask : list[int]):
        self.__ip = self.__convert_to_word(ip)
        self.__mask = self.__convert_to_word(mask)
        self.__network_address = None
        self.__cdir = None
        self.__broadcast = None
        self.__range_host = None

        self.__analysis()

    def __convert_to_word(self, octets: list[int]):
        word = 0
        for byte in octets:
            word = (word << 8) | byte
        return word

    def __calculation_network_address(self):
        self.__network_address = self.__ip & self.__mask

    def __calculation_cdir(self):
        self.__cdir = bin(self.__mask).count('1') 

    def __calculation_broadcast(self):
        self.__broadcast = self.__network_address | (2**(32 - self.__cdir)  - 1)
        
    def __calculation_range_host(self):
        self.__range_host = 2**(32 - self.__cdir) - 2

    def __analysis(self):
        self.__calculation_network_address()
        self.__calculation_cdir()
        self.__calculation_broadcast()
        self.__calculation_range_host()

    def export_res(self):
        return self.__ip, self.__mask, self.__network_address,self.__cdir,\
               self.__broadcast, self.__range_host
  
