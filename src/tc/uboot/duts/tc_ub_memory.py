# This file is part of tbot.  tbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# start with
# python2.7 src/common/tbot.py -c tbot.cfg -t tc_ub_memory.py
# convert duts tests from:
# http://git.denx.de/?p=duts.git;a=blob;f=testsystems/dulg/testcases/10_UBootMemory.tc;h=f5fb055499db17c322859215ab489cefb063ac47;hb=101ddd5dbd547d5046363358d560149d873b238a
from tbotlib import tbot

logging.info("args: %s %s", tb.tc_ub_memory_ram_ws_base, tb.tc_ub_memory_ram_ws_base_alt)

#set board state for which the tc is valid
tb.set_board_state("u-boot")

def tbot_send_wait(tb, cmd):
    tb.eof_write_con(cmd)
    tb.eof_read_end_state_con(1);

def tbot_send_check(tb, cmd, string):
    tb.eof_write_con(cmd)
    searchlist = [string]
    tmp = True
    cmd_nok = True
    while tmp == True:
        tmp = tb.readline_and_search_strings(tb.channel_con, searchlist)
        if tmp == 0:
            cmd_nok = False
            tmp = True
        elif tmp == 'prompt':
            tmp = False
        else:
            #endless loop
            tmp = True
    if cmd_nok == True:
        tb.end_tc(False)

def tbot_send_check_ret(tb, cmd, string):
    tb.eof_write_con(cmd)
    searchlist = [string]
    tmp = True
    cmd_ok = True
    while tmp == True:
        tmp = tb.readline_and_search_strings(tb.channel_con, searchlist)
        if tmp == 0:
            cmd_ok = False
            tmp = True
        elif tmp == 'prompt':
            tmp = False
        else:
            #endless loop
            tmp = True
    return cmd_ok

basecmdlist = [
"base",
"md 0 0xc",
"base " + tb.tc_ub_memory_ram_ws_base,
"md 0 0xc",
"md 0 0x40",
"base 0",
]

tbot_send_wait(tb, "help base")

for tmp_cmd in basecmdlist:
    tbot_send_wait(tb, tmp_cmd)

tmp = int(tb.tc_ub_memory_ram_ws_base, 16)
tmp += 4
tmp = hex(tmp)
tbot_send_wait(tb, "crc " + tmp + " 0x3fc")

tbot_send_wait(tb, "crc " + tmp + " 0x3fc" + " " + tb.tc_ub_memory_ram_ws_base)
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 4")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x40")

# crc check
tbot_send_wait(tb, "mw " + tb.tc_ub_memory_ram_ws_base + " 0xc0cac01a 0x100")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x100")
tbot_send_check(tb, "crc " + tmp + " 0x3fc", "5db8222f")
tbot_send_wait(tb, "mw " + tb.tc_ub_memory_ram_ws_base + " 0x00c0ffee 0x100")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x100")
tbot_send_check(tb, "crc " + tmp + " 0x3fc", "de3ac1b8")

# cmp
tbot_send_wait(tb, "help cmp")

#generate random file, and tftp it twice
tb.wordfd = tb.channel_ctrl
tb.tc_workfd_generate_random_file_name = tb.tc_ub_tftp_path + "random"
tb.tc_workfd_generate_random_file_length = '1048576'
tb.eof_call_tc("tc_workfd_generate_random_file.py")
tb.tc_ub_tftp_file_addr = tb.tc_ub_memory_ram_ws_base
tb.tc_ub_tftp_file_name = tb.tc_workfd_generate_random_file_name
tb.eof_call_tc("tc_ub_tftp_file.py")
tb.tc_ub_tftp_file_addr = tb.tc_ub_memory_ram_ws_base_alt
tb.eof_call_tc("tc_ub_tftp_file.py")

# compare
tbot_send_check(tb, "cmp " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 40000", "same")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0xc")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base_alt + " 0xc")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x40")

tbot_send_check(tb, "cmp.l " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 40000", "same")
tbot_send_check(tb, "cmp.w " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 80000", "same")
tbot_send_check(tb, "cmp.b " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 100000", "same")

# cp
tbot_send_wait(tb, "help cp")
tbot_send_wait(tb, "cp " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 10000")

tbot_send_wait(tb, "cp.l " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 10000")
tbot_send_wait(tb, "cp.w " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 20000")
tbot_send_wait(tb, "cp.b " + tb.tc_ub_memory_ram_ws_base + " " + tb.tc_ub_memory_ram_ws_base_alt + " 40000")

# md
tbot_send_wait(tb, "help md")
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base)

tbot_send_wait(tb, "md.w " + tb.tc_ub_memory_ram_ws_base)
tbot_send_wait(tb, "md.b " + tb.tc_ub_memory_ram_ws_base)

tbot_send_wait(tb, "md.b " + tb.tc_ub_memory_ram_ws_base + " 0x20")
tbot_send_wait(tb, "md.w " + tb.tc_ub_memory_ram_ws_base)
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base)

tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x40")

# mm
tbot_send_wait(tb, "help mm")

def tbot_read_write(tb, string, cmd):
    searchlist = [string]
    tmp = True
    cmd_ok = False
    while tmp == True:
        tmp = tb.readline_and_search_strings(tb.channel_con, searchlist)
        if tmp == 0:
            tb.eof_write_con(cmd)
            cmd_ok = True
            tmp = False
        elif tmp == 'prompt':
            tmp = False
        else:
            #endless loop
            tmp = True
    return cmd_ok

def tbot_send_list(tb, mm_list):
    for cmd in mm_list:
        string = raw("?")
        searchlist = [string]
        tmp = True
        cmd_ok = False
        while tmp == True:
            tmp = tb.readline_and_search_strings(tb.channel_con, searchlist)
            if tmp == 0:
                tb.eof_write_con(cmd)
                cmd_ok = True
                tmp = False
            elif tmp == 'prompt':
                tmp = False
            else:
                #endless loop
                tmp = True
        if cmd_ok != True:
            tb.send_ctrl_c(tb.channel_con)
            tb.eof_read_end_state_con(1);
            tb.end_tc(False)

mm_list = [
"0", "0xaabbccdd", "0x01234567"
]
tb.eof_write_con("mm " +  tb.tc_ub_memory_ram_ws_base)
tbot_send_list(tb, mm_list)
tb.send_ctrl_c(tb.channel_con)
tb.eof_read_end_state_con(1);
tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 10")

mm_list = [
"0x0101", "0x0202", "0x4321", "0x8765"
]
tb.eof_write_con("mm.w " +  tb.tc_ub_memory_ram_ws_base)
tbot_send_list(tb, mm_list)
tb.send_ctrl_c(tb.channel_con)
tb.eof_read_end_state_con(1);

tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 10")

mm_list = [
"0x48", "0x65", "0x6c", "0x6c", "0x6f", "0x20", "0x20",  "0x20",
]
tb.eof_write_con("mm.b " +  tb.tc_ub_memory_ram_ws_base)
tbot_send_list(tb, mm_list)
tb.send_ctrl_c(tb.channel_con)
tb.eof_read_end_state_con(1);

tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 10")

#mtest
ret = tbot_send_check_ret(tb, "help mtest", "Unknown command")
if ret:
    sz = int(tb.tc_ub_memory_ram_ws_base, 16)
    sz += 1024 * 1024
    sz = hex(sz)
    tbot_send_check(tb, "mtest " + tb.tc_ub_memory_ram_ws_base + " " + sz, "0000000f")
    tb.send_ctrl_c(tb.channel_con)
    tb.eof_read_end_state_con(1);

# mw
ret = tbot_send_check_ret(tb, "help mw", "Unknown command")
if ret:
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x10")
    tbot_send_wait(tb, "mw " + tb.tc_ub_memory_ram_ws_base + " 0xaabbccdd")
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x10")
    tbot_send_wait(tb, "mw " + tb.tc_ub_memory_ram_ws_base + " 0 6")
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x10")
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x40")

    tbot_send_wait(tb, "mw.w " + tmp + " 0x1155 6")
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x10")
    tmp = int(tb.tc_ub_memory_ram_ws_base, 16)
    tmp += 7
    tmp = hex(tmp)
    tbot_send_wait(tb, "mw.b " + tmp + " 0xff 7")
    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x10")

    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 0x40")

#nm
ret = tbot_send_check_ret(tb, "help nm", "Unknown command")
if ret:
    nm_list = [
    "0x48", "0x65", "0x6c", "0x6c", "0x6f"
    ]
    tb.eof_write_con("nm " +  tb.tc_ub_memory_ram_ws_base)
    tbot_send_list(tb, nm_list)
    tb.send_ctrl_c(tb.channel_con)
    tb.eof_read_end_state_con(1);

    tbot_send_wait(tb, "md " + tb.tc_ub_memory_ram_ws_base + " 10")

ret = tbot_send_check_ret(tb, "help loop", "Unknown command")

tb.end_tc(True)