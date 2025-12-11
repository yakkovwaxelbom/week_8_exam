from core.io import Io
from core.utils import AnalysisIp


PATH = 'subnet_info_{}_{}.txt'
ID = 2078164


def main():
    
    while True:
        ip, mask = Io.get_valid_input()
        analysis_ip = AnalysisIp(ip, mask)

        res_analysis_ip = analysis_ip.export_res()

        to_save = Io.get_res_format(*res_analysis_ip)

        path = PATH.format(ID, '.'.join(map(str,ip)))

        is_save = Io.save_to_file(path, to_save)

        if not is_save:
            raise Exception       
        print(joke)
        
        joke = Io.get_programming_joke()
        print(joke)
        

if __name__ == '__main__':
    main()

