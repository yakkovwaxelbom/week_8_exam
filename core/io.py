from enum import Enum
import re
import requests


from core.output_string import *

class IoError(Enum):
    SUCCESS = 0
    NOT_FOUR = 1
    NOT_NUM = 2
    NOT_IN_RANGE = 3,
    NOT_VALID_MASK = 4


class Io:

    # ---------------------------------------------------------------
    #                         input segment    
    # ---------------------------------------------------------------

    @staticmethod
    def __validate_and_parse_format(octets: list[str]) -> IoError:

        if len(octets) != 4:
            return IoError.NOT_FOUR

        for i, okta in enumerate(octets):
            if not okta.isdigit():
                return IoError.NOT_NUM
            octets[i] = int(okta)

        for okta in octets:
            if not (0 <= okta <= 255):
                return IoError.NOT_IN_RANGE

        return IoError.SUCCESS
    

    @staticmethod
    def __validate_and_prase_ip(ip: list[str]) -> IoError:
        return Io.__validate_and_parse_format(ip)
    
    @staticmethod
    def __validate_and_prase_mask(mask: list[str]) -> IoError:
        res  = Io.__validate_and_parse_format(mask)

        if res == IoError.SUCCESS:
            pattern = '^1*0*$'
            binary_mask = ''.join(f"{int(o):08b}" for o in mask)

            if re.fullmatch(pattern, binary_mask):
                return IoError.SUCCESS 
                       
        return IoError.NOT_VALID_MASK

    
    @staticmethod
    def __print_error(inp: str,part: str, error: IOError) -> None:
        if error != IoError.SUCCESS:
            print(f'in {part}, {'.'.join(map(str, inp))}:', end=' ')

            if error == IoError.NOT_FOUR:
                print('Please enter input with only 4 octets.')
            elif error == IoError.NOT_NUM:
                print('Please enter only numbers')
            elif error == IoError.NOT_IN_RANGE:
                print('Please enter numbers in the range 0-255')
            elif error == IoError.NOT_IN_RANGE:
                print('Incorrect mask')

    
    @staticmethod
    def get_valid_input() -> tuple[list[int], list[int]]:

        inp_ip = input('Please enter a valid IP address in' 
                        ' the format x.x.x.x ').split('.')
        is_valid_ip = Io.__validate_and_prase_ip(inp_ip)

        while  is_valid_ip != IoError.SUCCESS:
            Io.__print_error(inp_ip, 'ip', is_valid_ip)
            inp_ip = input('Please enter a valid IP address '
                            'in the format x.x.x.x ').split('.')
            is_valid_ip = Io.__validate_and_prase_ip(inp_ip)

        inp_mask = input('Please enter a valid mask in ' \
                        'the format x.x.x.x ').split('.')
        is_valid_mask = Io.__validate_and_prase_mask(inp_mask)

        while is_valid_mask != IoError.SUCCESS:
            Io.__print_error(inp_mask, 'mask', is_valid_mask)
            inp_ip = input('Please enter a valid mask in the ' \
                            'format x.x.x.x ').split('.')
            is_valid_mask = Io.__validate_and_prase_mask(inp_ip)

        return inp_ip, inp_mask
    

    # ---------------------------------------------------------------
    #                         output segment    
    # ---------------------------------------------------------------

    @staticmethod
    def __convert_to_str(word):
        return '.'.join(str((word >> (i * 8)) & 0xFF) for i in range(3, -1, -1))
    

    @staticmethod
    def get_res_format(ip, mask, network_address, cdir, broadcast, range_host):
        classes = {8: 'Class A', 16: "Class B", 24: 'Class C'}
        res_format = []

        str_ip = Io.__convert_to_str(ip)
        res_format.append(format_input_ip(str_ip))

        str_mask = Io.__convert_to_str(mask)
        res_format.append(format_input_ip(str_mask))

        _class = classes.get(cdir, 'Classless')
        res_format.append(format_classful_status(_class))

        network_address_str = Io.__convert_to_str(network_address)
        res_format.append(format_network_address(network_address_str))

        broadcast_str = Io.__convert_to_str(broadcast)
        res_format.append(format_broadcast_address(broadcast_str))

        range_host_str = str(range_host)
        res_format.append(format_num_hosts(range_host_str))

        cdir_str = str(cdir)
        res_format.append(format_cidr_mask(cdir_str))

        return ''.join(res_format)
    
    @staticmethod
    def save_to_file(path: str, data):

        res = True
        try:
            with open(path, 'a') as f:
                f.write(data)

        except Exception as err:
            print(f"Error saving file: {err}")
            res = False

        return res

    # ---------------------------------------------------------------
    #                         caput segment    
    # ---------------------------------------------------------------
    
    @staticmethod
    def get_programming_joke():
        url = "https://sv443.net/jokeapi/v2/joke/Programming"
        response = requests.get(url)
        data = response.json()

        if data.get("error"):
            return 'bla bla There is an error and an error is an unfunny joke.'

        if data["type"] == "single":
            return data["joke"]

        elif data["type"] == "twopart":
            return f"{data['setup']} — {data['delivery']}"


