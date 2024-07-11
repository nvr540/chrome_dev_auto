import os

def get_random_bytes():
    return os.urandom(16)

def generate_uuid():

    random_bytes = list(get_random_bytes())

    random_bytes[6] = random_bytes[6] & 0x0F | 0x40

    random_bytes[8] = random_bytes[8] & 0x3F | 0x80

    def to_hex_string(byte_array):
        return ''.join([f'{b:02x}' for b in byte_array])

    uuid_string = (
        f'{to_hex_string(random_bytes[0:4])}-'
        f'{to_hex_string(random_bytes[4:6])}-'
        f'{to_hex_string(random_bytes[6:8])}-'
        f'{to_hex_string(random_bytes[8:10])}-'
        f'{to_hex_string(random_bytes[10:16])}'
    )

    return uuid_string
if __name__ == '__main__':
    print(generate_uuid())
