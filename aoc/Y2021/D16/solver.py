from typing import Any
from aoc.tools import ABCSolver
import binascii

class Solver(ABCSolver):

    def solve(self, part2: bool = False) -> tuple[Any, str]:

        hex_string = self.data[0]

        lenhex = len(hex_string)

        # Convert the hexadecimal string to an integer using the base 16  
        hex_integer = int(hex_string, 16) 
        # Convert the integer to binary using the bin() function  
        binary_string = bin(hex_integer)  
        # Remove the '0b' prefix from the binary string  
        binary_string = binary_string[2:].zfill(4*lenhex)

        def decode(bits:str)->tuple[int, int, int, str]:
            if bits[3:6] == '100':
                return decode_literal(bits)
            else:
                return decode_operator(bits)

        def decode_literal(literalbits:str)->tuple[int, int, int, str]:
            # print('decodeliteral')
            #Version number 
            version = literalbits[0:3]
            typeID = literalbits[3:6]
            # print(version, typeID, None)

            cursor = 6
            binary_value = ''
            while(True):
                next_bits = literalbits[cursor:cursor+5]
                value = next_bits[1:]
                binary_value += value
                cursor += 5
                if next_bits[0]=='0':
                    break
            
            otherbits = literalbits[cursor:]
            if int(otherbits+'0', 2) == 0 : otherbits == ''
            base10value = int(binary_value, 2)
            underlying_versions = 0
            return int(version, 2), int(typeID, 2), base10value, otherbits, underlying_versions+int(version, 2)

        def decode_operator(operatorbits:str,)->tuple[int, int, int, str]:
            # print('decodeoperator')
            version = operatorbits[0:3]
            typeID = operatorbits[3:6]
            bitlabel = operatorbits[6]
            # print(version, typeID, bitlabel)
            sommeversion = 0
            underlying_values = []

            # si label 0, alors 15 bits
            if bitlabel == '0':
                lengthbits = int(operatorbits[7:7+15], 2)
                bits_to_analyse = operatorbits[22:22+lengthbits]
                rest_to_analyse = operatorbits[22+lengthbits:]
                while len(bits_to_analyse)>0 : 
                    ver, tID, base10value, bits_to_analyse, underlying = decode(bits_to_analyse)
                    underlying_values.append(base10value)
                    sommeversion += underlying

            # Si label 1, alors 11 bits
            elif bitlabel == '1':
                numbits = int(operatorbits[7:7+11], 2)
                bits_to_analyse = operatorbits[18:]
                for iterator in range(numbits):
                    ver, tID, base10value, bits_to_analyse, underlying = decode(bits_to_analyse)
                    sommeversion += underlying
                    underlying_values.append(base10value)
                rest_to_analyse = bits_to_analyse

            if int(rest_to_analyse+'0', 2)==0 : rest_to_analyse = ''

            match typeID : 
                case '000' : 
                    value = sum(underlying_values)
                case '001' : 
                    value = 1
                    for e in underlying_values : value *=e
                case '010' : 
                    value = min(underlying_values)
                case '011' :
                    value = max(underlying_values)
                case '101' :
                    value = int(underlying_values[0]>underlying_values[1])
                case '110':
                    value = int(underlying_values[0]<underlying_values[1])
                case '111':
                    value = int(underlying_values[0]==underlying_values[1])

            return (int(version, 2), int(typeID, 2), value, rest_to_analyse, int(version, 2)+sommeversion)
        
        if not part2 : 
            return 'No structure', decode(binary_string)[-1]
        else:
            return 'No structure', decode(binary_string)[2]
    
    def generate_view(self, structure: Any) -> str:
        return 'No view'