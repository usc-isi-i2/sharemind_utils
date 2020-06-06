# PPER - Sharemind

This repository stores all [Sharemind](https://sharemind.cyber.ee/) MPC related scripts and notes.

## Docker

## Emulator argument streaming

Sharemind only allows passing int, uint and bint series data types from command line. `argument-stream-cipher.py` encodes data to file stream and bypasses this restriction. It supports all primitive data types.

```
python argument-stream-cipher.py <quad>*
```

The `<quad>` is formed by name, domain, type, value
The output is byte stream.

Examples:
```
python argument-stream-cipher.py num pd_share3p uint64 100 > input.bin
python argument-stream-cipher.py arr pd_share3p uint64 [1,2] > input.bin
python argument-stream-cipher.py a pd_share3p uint64 [1,2] b pd_share3p uint64 [3,4] > input.bin
```

Then pass the file stream to emulator.
```
sharemind-emulator <compiled_SecreC_program>.sb --cfile=input.bin
```

To decode emulator's output, `argument-stream-decipher.py` can be used.

```
sharemind-emulator <compiled_SecreC_program>.sb <input arguments> | python argument-stream-decipher.py
```

