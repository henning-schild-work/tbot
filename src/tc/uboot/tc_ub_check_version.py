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
# Description:
#
# check if the current running U-Boot vers == tb.uboot_vers
# and SPL vers == tb.spl_vers
#
# End:

from tbotlib import tbot

logging.info("arg: %s %s", tb.uboot_vers, tb.spl_vers)

# set board state for which the tc is valid
tb.set_board_state("u-boot")

# set env var
c = tb.c_con

if tb.uboot_vers != '':
    tmp = 'vers'
    tb.eof_write(c, tmp)
    searchlist = ['U-Boot 20']
    tmp = True
    ret = False
    uvers = 'undef'
    while tmp == True:
        retu = tb.tbot_rup_and_check_strings(c, searchlist)
        if retu == 'prompt':
            tmp = False
        if retu == '0':
            ret = tb.tbot_rup_and_check_strings(c, '\n')
            if ret == 'prompt':
                tb.enc_tc(False)
            tmp = 'U-Boot 20' + tb.buf.replace('\r','')
            uvers = tmp.replace('\n','')
            if uvers == tb.uboot_vers:
                ret = True
            tmp = True

    if ret != True:
        logging.warn("UB Vers differ %s != %s", uvers, tb.uboot_vers)
        tb.end_tc(False)

if tb.spl_vers == '':
    tb.end_tc(True)

tmp = 'res'
tb.c_con.set_check_error(False)
tb.eof_write(c, tmp)
searchlist = ['U-Boot SPL 20']
tmp = True
ret = False
splvers = 'undef'
while tmp == True:
    retu = tb.tbot_rup_and_check_strings(c, searchlist)
    if retu == 'prompt':
        tmp = False
    if retu == '0':
        ret = tb.tbot_rup_and_check_strings(c, '\n')
        if ret == 'prompt':
            tb.enc_tc(False)
        tmp = 'U-Boot SPL 20' + tb.buf.replace('\r','')
        splvers = tmp.replace('\n','')
        if splvers == tb.spl_vers:
            ret = True
        tmp = False

tb.set_board_state("u-boot")
tb.c_con.set_check_error(True)

if ret == False:
    logging.warn("UB SPL Vers differ %s != %s", splvers, tb.spl_vers)


tb.end_tc(ret)
