import struct

def read_event_name(filename):
    with open(filename, 'rb') as f:
        # First is junk
        f.read(36)
        bytes = f.read(4)
        length = struct.unpack('>I', bytes)[0]
        s = struct.unpack('<%ds' % length, f.read(length))
        s = s[0].strip().decode('ascii')
    return s
