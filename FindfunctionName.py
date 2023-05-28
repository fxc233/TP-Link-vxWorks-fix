# IDApython >= 7.5

import ida_kernwin
import idautils
import idc
import idaapi

BinaryPath = ""

BinaryPath = ida_kernwin.ask_file(0, "*", "symbol table file")
if BinaryPath is None:
    exit(0)

symfile_path = ''    
symbols_table_start = 8
strings_table_start = 0x1a728

with open(BinaryPath, 'rb') as f:
    file_contents = f.read()

symbols_table = file_contents[symbols_table_start:strings_table_start]
strings_table = file_contents[strings_table_start:]


def str_to_hex(string):
    hex_string = ''
    byte_string = ''
    for i in string:
        byte_string = hex(i)[2:]
        if len(byte_string) == 1:
            byte_string = '0' + byte_string
        hex_string+= byte_string
    return hex_string


def get_string_by_offset(offset):
    index = 0
    while True:
        if strings_table[offset+index] != 0:
            index += 1
        else:
            break
    return strings_table[offset:offset+index]


def get_symbols_metadata():
    symbols = []
    for offset in range(0, len(symbols_table), 8):
        symbol_item = symbols_table[offset:offset+8]
        flag = symbol_item[0]
        string_offset = int(str_to_hex(symbol_item[1:4]), 16)
        string_name = get_string_by_offset(string_offset)
        target_address = int(str_to_hex(symbol_item[-4:]), 16)
        symbols.append((flag, string_name, target_address))
    return symbols


def add_symbols(symbols_meta_data):
    for flag, string_name, target_address in symbols_meta_data:
        idc.set_name(target_address, string_name.decode(), idaapi.SN_NOWARN)
        if flag == 84 or flag == 116:
            idaapi.add_func(target_address, idaapi.BADADDR)


def main():
    symbols_metadata = get_symbols_metadata()
    # for flag, string_name, target_address in symbols_metadata:
    #    print(hex(target_address) + ":\t" + string_name.decode())
    add_symbols(symbols_metadata)


if __name__ == '__main__':
    main()
   