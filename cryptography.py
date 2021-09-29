from binascii import hexlify

class Converter:
    def Seq_to_binary(self, seq):
        return ' '.join(format(ord(x), 'b') for x in seq)

    def Char_to_hex(self, seq):
        return format(ord(seq), 'x')

    def Decimal_to_binary(self, decimal):
        return bin(int(decimal)).replace("0b", "")

    def Char_to_binary(self, t):
        return Converter.Decimal_to_binary(Converter, int(Converter.Char_to_hex(Converter, t), 16))

    def Binary_to_decimal(self, binary):
        string = int(binary, 2)
        return string

    def Binary_to_seq(self, b):
        str_data = ''
        for i in range(0, len(b), 7):
            temp_data = b[i:i + 7]
            decimal_data = Converter.Binary_to_decimal(Converter, temp_data)
            str_data = str_data + chr(decimal_data)
        return str_data

    def Validate_Binary(self, b):
        if len(b.rstrip()) < 7 and len(b.lstrip()) < 7:
            x = 7 - len(b)
            b = '0' * x + b
        return b

    def XOR(self, t1, t2):
        return Converter.Decimal_to_binary(Converter, int(Converter.Char_to_hex(Converter, t1), 16) ^ int(Converter.Char_to_hex(Converter, t2), 16))

class Encoder:
    def Encode(self, seq):
        b_seq = ''
        i = 0
        k = 1
        n_seq = ''

        for i in range(len(seq)):
            n_seq += Converter.Validate_Binary(Converter, Converter.Seq_to_binary(Converter, seq[i])) + ' '
        
        n_seq = n_seq.rstrip()

        # part 1
        i = 0

        while i < len(seq):
            b = ''
            if i < len(seq) - 1:
                b_seq += Converter.Validate_Binary(Converter, Converter.XOR(Converter, seq[i], seq[i+1])) + ' '
                b = Converter.Validate_Binary(Converter, Converter.XOR(Converter, seq[i], seq[i+1]))
                i += 2
                k += 1
            else:
                if len(seq) % 2 != 0:
                    b_seq += Converter.Validate_Binary(Converter, Converter.XOR(Converter, seq[-1], 'E')) + ' '
                    b = Converter.Validate_Binary(Converter, Converter.XOR(Converter, seq[-1], 'E'))
                break
        
        del b, i, k
        b_seq = b_seq.rstrip()

        # part 2
        n_seq = n_seq.replace(' ', '')
        s_seq = Converter.Validate_Binary(Converter, Converter.Seq_to_binary(Converter, seq))

        if len(seq) % 2 != 0:
            n_seq += Converter.Validate_Binary(Converter, Converter.Char_to_binary(Converter, "E"))
            s_seq = f'{Converter.Validate_Binary(Converter, Converter.Seq_to_binary(Converter, seq))} {Converter.Validate_Binary(Converter, Converter.Char_to_binary(Converter, "E"))}'
        
        s_seq = s_seq.split()
        encoded_seq = Encoder.Encoder_Logic(Encoder, n_seq, b_seq, s_seq)
        
        return encoded_seq
    
    def Encoder_Logic(self, n_seq, b_seq, s_seq):
        t = 0
        i = 0
        k = 0
        end_k = 7

        while t < len(s_seq) - 1:
            if t > 0:
                i += 1
                k += 7
                end_k += 14
            
            if k == len(n_seq):
                break
            
            while i < len(b_seq) + i and k < end_k:
                if b_seq[i] != ' ':
                    if b_seq[i] == '0':
                        if n_seq[k] == '0' and n_seq[k+7] == '0':
                            b_seq = b_seq[:i+1] + '0' + b_seq[i+1:]
                        elif n_seq[k] == '1' and n_seq[k+7] == '1':
                            b_seq = b_seq[:i+1] + '1' + b_seq[i+1:]
                    else:
                        if n_seq[k] == '0' and n_seq[k+7] == '1':
                            b_seq = b_seq[:i+1] + '0' + b_seq[i+1:]
                        elif n_seq[k] == '1' and n_seq[k+7] == '0':
                            b_seq = b_seq[:i+1] + '1' + b_seq[i+1:]
                    i += 2
                    k += 1
                else:
                    break

            t += 1
        
        return b_seq

class Decoder:
    def Decode(self, encoded_seq):
        final_decoded_seq = ''
        decoded_seq = ['', '']
        splited_encoded_seq = encoded_seq.split()
        Decoder.Decoder_Logic(Decoder, splited_encoded_seq, decoded_seq)

        for i in range(len(decoded_seq)):
            final_decoded_seq += decoded_seq[i]

        if decoded_seq[-1] == '1000101' and len(decoded_seq) - 1 % 2 != 0:
            final_decoded_seq = final_decoded_seq[:len(final_decoded_seq) - 7].rstrip()
        
        return Converter.Binary_to_seq(Converter, final_decoded_seq)

    def Add_Space_To_List(self, space_amount, lst):
        j = 0

        while j < space_amount:
                lst += str(lst.append(''))
                lst.pop(-1)
                lst.pop(-1)
                lst.pop(-1)
                lst.pop(-1)
                j += 1

        return lst

    def Decoder_Logic(self, splited_encoded_seq, decoded_seq):
        k = 0
        t = 0

        while k < len(splited_encoded_seq):
            i = 0

            while i < len(splited_encoded_seq[k]) - 1:
                if splited_encoded_seq[k][i] == '0':
                    if splited_encoded_seq[k][i+1] == '1':
                        decoded_seq[t] += '1'
                        decoded_seq[t+1] += '1'
                    else:
                        decoded_seq[t] += '0'
                        decoded_seq[t+1] += '0'
                else:
                    if splited_encoded_seq[k][i+1] == '1':
                        decoded_seq[t] += '1'
                        decoded_seq[t+1] += '0'
                    else:
                        decoded_seq[t] += '0'
                        decoded_seq[t+1] += '1'

                i += 2

            if k < len(splited_encoded_seq) - 1:
                Decoder.Add_Space_To_List(Decoder, 2, decoded_seq)
            
            k += 1
            t += 2

def encrypt_file(filepath: str):
    seq = str(hexlify(open(filepath, 'rb').read()))
    encrypted_file = str(Encoder.Encode(Encoder, seq))
    
    return encrypted_file

def encrypt(seq: str):
    encrypted_file = str(Encoder.Encode(Encoder, seq))
    
    return encrypted_file

def decrypt(encrypted_file: str):
    return str(Decoder.Decode(Decoder, encrypted_file))

def list_to_str(lst):
    stri = ''

    for item in lst:
        stri += item + ' '
    
    return stri

def contiguous_decrypt(encoded_seq: str, times: int):
    for i in range(0, times):
        if i > 0:
            decoded_seq = Decoder.Decode(Decoder, decoded_seq)
        
        decoded_seq = Decoder.Decode(Decoder, encoded_seq)

    return decoded_seq

def contiguous_encrypt(seq: str, times: int):
    for i in range(0, times):
        if i > 0:
            encoded_seq = Encoder.Encode(Encoder, list_to_str(encoded_seq))
        
        encoded_seq = Encoder.Encode(Encoder, seq)
    
    return encoded_seq
