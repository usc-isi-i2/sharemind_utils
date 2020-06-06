import sys
import struct

# struct Argument {
#   uint64_t argumentNameSize;
#   char     argumentName[argumentNameSize];
#   uint64_t protectionDomainNameSize;
#   char     protectionDomainName[protectionDomainNameSize];
#   uint64_t typeNameSize;
#   char     typeName[typeNameSize];
#   uint64_t argumentDataSize;
#   char     argumentData[argumentDataSize];
# } arguments[num_arguments];
# https://github.com/sharemind-sdk/emulator/blob/master/doc/sharemind-emulator.h2m
# https://docs.python.org/3/library/struct.html

def string_to_byte_args(s):
    return tuple([c.encode('utf-8') for c in s])

def encode_argument(name, domain, type_, value):
    """
    enc_t = encode_argument('t', 'pd_shared3p', 'float32', 0.8)
    """
    argumentName = name
    argumentNameSize = len(argumentName)
    protectionDomainName = domain
    protectionDomainNameSize = len(protectionDomainName)
    typeName = type_
    typeNameSize = len(typeName)
    if not isinstance(value, list):
        value = [value]

    if typeName == 'bool':
        argumentDataSize = 1 * len(value)
        argumentData = b''.join([struct.pack('<?', v) for v in value])
    elif typeName == 'float32':
        argumentDataSize = 4 * len(value)
        argumentData = b''.join([struct.pack('<f', v) for v in value])
    elif typeName == 'float64':
        argumentDataSize = 8 * len(value)
        argumentData = b''.join([struct.pack('<d', v) for v in value])
    elif typeName == 'int8':
        argumentDataSize = 1 * len(value)
        argumentData = b''.join([struct.pack('<b', v) for v in value])
    elif typeName == 'int16':
        argumentDataSize = 2 * len(value)
        argumentData = b''.join([struct.pack('<h', v) for v in value])
    elif typeName == 'int32':
        argumentDataSize = 4 * len(value)
        argumentData = b''.join([struct.pack('<l', v) for v in value])
    elif typeName == 'int64':
        argumentDataSize = 8 * len(value)
        argumentData = b''.join([struct.pack('<q', v) for v in value])
    elif typeName == 'uint8':
        argumentDataSize = 1 * len(value)
        argumentData = b''.join([struct.pack('<B', v) for v in value])
    elif typeName == 'uint16':
        argumentDataSize = 2 * len(value)
        argumentData = b''.join([struct.pack('<H', v) for v in value])
    elif typeName == 'uint32':
        argumentDataSize = 4 * len(value)
        argumentData = b''.join([struct.pack('<L', v) for v in value])
    elif typeName == 'uint64':
        argumentDataSize = 8 * len(value)
        argumentData = b''.join([struct.pack('<Q', v) for v in value])
    # elif typeName == 'string':
    #     argumentData = struct.pack('<d', value)

    argument = struct.pack('<Q', argumentNameSize)
    argument += struct.pack('{}c'.format(argumentNameSize), *string_to_byte_args(argumentName))
    argument += struct.pack('<Q', protectionDomainNameSize)
    argument += struct.pack('{}c'.format(protectionDomainNameSize), *string_to_byte_args(protectionDomainName))
    argument += struct.pack('<Q', typeNameSize)
    argument += struct.pack('{}c'.format(typeNameSize), *string_to_byte_args(typeName))
    argument += struct.pack('<Q', argumentDataSize)
    argument += argumentData

    return argument

def recover_type(l, type_):
    if not isinstance(l, list):
        return True

    for i in range(len(l)):
        if recover_type(l[i], type_):
            l[i] = type_(l[i])
    return False

if __name__ == '__main__':
    # every four arguments form a quad
    if (len(sys.argv)-1) % 4 != 0:
        sys.stderr.write('Invalid arguments\n')
        sys.stderr.flush()
        exit(-1)

    i = 1
    while i < len(sys.argv):
        name, domain, type_, value = sys.argv[i : i+4]
        if value[0] == '[' and value[-1] == ']':
            value = eval(value)
        else:
            value = [value]

        py_type = None
        if type_ == 'bool':
            py_type = bool
        elif type_.startswith('float'):
            py_type = float
        elif type_.startswith(('int', 'uint')):
            py_type = int
        recover_type(value, py_type)

        sys.stdout.write(encode_argument(name, domain, type_, value))
        sys.stdout.flush()
        i += 4

