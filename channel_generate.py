import random

def generate_uuid():

    random_bytes = bytearray(random.getrandbits(8) for _ in range(16))

    random_bytes[6] = (random_bytes[6] & 0x0F) | 0x40

    random_bytes[8] = (random_bytes[8] & 0x3F) | 0x80

    uuid_str = "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *random_bytes)

    return uuid_str

if __name__ == '__main__':
    uuid = generate_uuid()
    print(uuid)
