==============================
Guide to use tbot with the BBB
==============================

This is a small guide of how to use tbot when starting from scratch.

When reading this section, you get a step by step introduction how to use tbot with a beagleboneblack and a
"Gembird Silver Shield PM power controller" and using kermit for accessing the serial console.

tbot installation
=================

Buy the following hw
--------------------

[1] Beagle Bone Black
    http://beagleboard.org/black

[2] Gembird Silver Shield PM power controller
    https://www.amazon.de/EG-PMS2-programmierbare-Steckdosenleiste-%C3%9Cberspannungsschutz-Schnittstelle/dp/B00BAQZJ4K/ref=sr_1_3?ie=UTF8&qid=1502686146&sr=8-3&keywords=SIS-PMS+Silvershield+Power+Manager

    If you do not get the gembird powercontroller, you can use tbot
    without controlling boards power ... try `interactive power mode`_

    This is also a good startig point for running tbot with another power controller.

    `Using tbot without Gembirds powercontroller`_

[3] USB2serial FTDI
    http://elinux.org/Beagleboard:BeagleBone_Black_Accessories#Serial_Debug_Cables

If you want to switch bootmodes, buy an USB relais

[4] USB Relais
    https://www.sainsmart.com/sainsmart-4-channel-5v-usb-relay-board-module-controller-for-automation-robotics.html

    be sure you get the 5V one, not as I the 12V one. With the 12V one you need
    12V external power ...

Remark: you do not need to use/buy this specific hw, for getting tbot running, but it is used in this example.

[5] Lap and Host PC
    Of course you need a PC with a linux installation.
    I use/used fedora 21, 22, 24, and 25, but all other distros should work too.

For this guide we use first the PC [5] as Host and LapPC.

Later, you can install tbot on another PC and use [5] as LapPC
only.

install paramiko on [5]
-----------------------

you need for running tbot the python paramiko module, see:

http://www.paramiko.org/installing.html

may you face an error:

::

  from tbotlib import tbot
  File "/home/lukma/work/tests/tbot/src/common/tbotlib.py", line 29, in <module>
  from tbot_connection_paramiko import Connection
  File "/home/lukma/work/tests/tbot/src/common/tbot_connection_paramiko.py", line 7, in <module>
  import paramiko
  File "/usr/local/lib/python2.7/dist-packages/paramiko/__init__.py", line 31, in <module>
  from paramiko.transport import SecurityOptions, Transport File "/usr/local/lib/python2.7/dist-packages/paramiko/transport.py", line 57, in <module>
  from paramiko.ed25519key import Ed25519Key File "/usr/local/lib/python2.7/dist-packages/paramiko/ed25519key.py", line 22, in <module>
  import nacl.signing
  ImportError: No module named nacl.signing

http://pynacl.readthedocs.io/en/latest/install

install gembird software
------------------------

http://sispmctl.sourceforge.net/

install kermit
--------------

use a package manager for this job, or download source from here:

http://www.columbia.edu/kermit/ckuins.html


get the tbot source code:
-------------------------

::

  $ git clone https://github.com/hsdenx/tbot.git
  [...]
  $

cd into the tbot directory.

try ssh access to your LabPC
----------------------------

first we test, if we can ssh to our PC [5]. As we use [5] as Host and LabPC
this should work, but we test it. Find out the ip or host name of your machine
and ssh to it, for me this looked like:

.. image:: image/guide/ssh_shell.png

copy some existing lab config to your new config
------------------------------------------------

::

  hs@localhost:tbot  [master] $ cp config/lab_hs_home.py config/lab_hs_laptop.py
  hs@localhost:tbot  [master] $

You can name your new lab config as you want, but I prefer to let it
begin with prefix `lab_`. In the following guide I use for the lab config
the name "lab_hs_laptop" ... please replace this with the name you
defined here!


Adapt the setting for accessing your labPC
------------------------------------------

.. image:: image/guide/guide_ssh.png

If you need a password for ssh to your PC than add it in
the password.py file

.. image:: image/guide/guide_ssh_password.png

If you need a public key, than add it in your password.py

.. image:: image/guide/guide_ssh_public_key.png

If you need to adapt the portnumber for ssh

.. image:: image/guide/guide_ssh_port.png

LabPC specific settings
-----------------------

you may need to set lab specific settings when tbot starts.

For this case you can write a testcase, which setups all things
you need when tbot starts, and add it in your lab config file

.. image:: image/guide/guide_lab_specific.png

In this example, we named the testcase `tc_lab_prepare_laptop_hs.py` and always when tbot opens a connection, the testcase

https://github.com/hsdenx/tbot/blob/master/src/tc/lab/tc_lab_prepare_laptop_hs.py

gets called. In this example case, always a fix ip is set
to the p2p1 interface (I use this for tftp and nfs server)
and rmmod the ftdi_sio module if loaded.

tbot *always* calls the testcase:

https://github.com/hsdenx/tbot/blob/master/src/tc/lab/tc_lab_prepare.py

when opening a connection. As you see in the testcase, tbot always
wants to cd into tbots workdirectory. So you *need* to adapt the config variables:

.. image:: image/guide/guide_demo1_lab_config.png

to the settings on your LabPC! Otherwise tbot fails on startup.

Adapt settings for Gembird Powercontroller
------------------------------------------

connect your USB cable from the Gembirs Powercontroller with an USB port on your PC.

check, if your laptop detected the Powercontroller, with dmesg output.

You should see something like that

::

  [ 2475.394934] usb 1-4: new low-speed USB device number 6 using xhci_hcd
  [ 2475.564195] usb 1-4: New USB device found, idVendor=04b4, idProduct=fd13
  [ 2475.564200] usb 1-4: New USB device strings: Mfr=1, Product=2, SerialNumber=0
  [ 2475.564202] usb 1-4: Product: Gembird Silver Shield PM
  [ 2475.564204] usb 1-4: Manufacturer: Gembird Electronics
  [ 2475.565613] usbhid 1-4:1.0: couldn't find an input interrupt endpoint
  hs@localhost:tbot  [master] $ 


Now, check if the "sispmctl" tool work with your Gembird Powercontroller.

Check version of sispmctl tool

.. image:: image/guide/guide_sispmctl_version.png

Scan for the Powercontroller

.. image:: image/guide/guide_sispmctl_scan.png

Now adapt the tbot settings for your needs:

.. image:: image/guide/guide_sispmctl_explanation.png

This is the setup for powering port 1 on/off of the Gembird controller.

If you need to use another port of the Gembird controller, change the
value in "tb.config.gembird_index" to the appropriate value.

Now it should be possible to switch on/off port 1 on the Gembird
Powercontroller with tbot.

If you can;t wait and want to test this now, we need to supress
tbot to connect to the boards console, as we did not have setup
it up yet:

So add in config/lab_hs_laptop.py the line

::

  do_connect_to_board = False

and start tbot:

.. image:: image/guide/guide_sispmctl_fasttest.png


You should see on the Gembird controller the respective port going
on and off.

Now, we want to setup the console, so remove the line

::

  do_connect_to_board = False

in "config/lab_hs_laptop.py"


Setup the console
-----------------

attach the USB2serial [3] cable to your USB port on [5]

check dmesg output:

::

  [ 7554.706870] usb 1-3: new full-speed USB device number 7 using xhci_hcd
  [ 7554.871691] usb 1-3: New USB device found, idVendor=067b, idProduct=2303
  [ 7554.871696] usb 1-3: New USB device strings: Mfr=1, Product=2, SerialNumber=0
  [ 7554.871698] usb 1-3: Product: USB-Serial Controller
  [ 7554.871700] usb 1-3: Manufacturer: Prolific Technology Inc.
  [ 7556.354720] usbcore: registered new interface driver pl2303
  [ 7556.354741] usbserial: USB Serial support registered for pl2303
  [ 7556.354763] pl2303 1-3:1.0: pl2303 converter detected
  [ 7556.355611] usb 1-3: pl2303 converter now attached to ttyUSB0
  hs@localhost:tbot  [master] $ 

In our case the USB cable is on /dev/ttyUSB0, so add this value in
"config/lab_hs_laptop.py"

.. image:: image/guide/guide_serial_setup_edit.png

Be sure you have installed kermit and have the correct access rights
to access the serial port!

You can test this with:

.. image:: image/guide/guide_kermit_test.png

power on the beaglebone and you should see some output from the beagleboneblack.

Put in the powerplug from the beaglebone in the port 1 of your Gembird Powercontroller
(or the port you defined in step `Adapt settings for Gembird Powercontroller`_.

Try a first small U-Boot testcase. Simply set an U-Boots Environment variable.

.. image:: image/guide/guide_first_run.png

If you want to see, what tbot is doing, enable the verbose "-v" option from tbot.
See also hint `more readable verbose output`_.

Also you can look into the logfile log/tbot.log (filename passed with tbots option "-l")

If you get "set board state failure end" message

.. image:: image/guide/guide_first_run_failure.png

May you have a Beagleboneblack board with a very old U-Boot.

U-Boots prompt changes once from "U-Boot# " to "=> ".

The default value is the new "=> " one ... so, edit the board config
"config/beagleboneblack.py" as follow:

.. image:: image/guide/guide_first_run_fix_prompt.png


Now you can start with writting testcases for the beagleboneblack board,
see `tbot write a testcase`_.

tbot install statistic backend
------------------------------

install gnuplot on your labPC [5]. Installation see

http://www.gnuplot.info/

Used version in for this guide:

.. image:: image/guide/guide_backend_statistic_gnuplotversion.png

Enable the statistic backend in tbot

.. image:: image/guide/guide_backend_statistic_enable.png

run tbot and after tbot finsihed you got in tbot source dir the file
"stat.dat". Simply call now gnuplot:

::

  hs@localhost:tbot  [master] $ gnuplot src/files/balkenplot.sem
  hs@localhost:tbot  [master] $

and find the output.jpg in tbot source dir.

Example output:

.. image:: image/guide/guide_backend_statistic_example.png
   :scale: 40%

tbot install dot backend
------------------------

install dot on your labPC [5]. Installation see

http://www.graphviz.org/Download..php

Used version in for this guide:

.. image:: image/guide/guide_backend_dot_version.png

Enable the dot backend in tbot

.. image:: image/guide/guide_backend_dot_enable.png

Simply run now tbot and after tbot finished you see the file
"tc.dot" in tbot source directory.

Create a png Image with

::

   $ dot -Tpng tc.dot > tc.png

or a ps file with

::

  $ dot -Tps tc.dot > tc.ps

Here an example for a resulting image:

.. image:: image/guide/guide_backend_dot_example.png
   :scale: 70%

What do we see?

Executed testcase files are in black boxes.

Called testcase functions are in blue boxes.

Returning with success is a green arrow.

Returning with failure is a red arrow.



tbot install html backend
-------------------------

Enable the html backend in tbot

.. image:: image/guide/guide_backend_html_enable.png

start tbot and at the end, you have the new file "log/html_log.html"

Simply open this html file with a broswer, and you should see the "nice log".

! The html file needs the css style sheet file "log/multiplexed_tbotlog.css" file

tbot install dashboard
----------------------

Enable dashboard for the bbb:

.. image:: image/guide/guide_backend_dashboard_enable.png

The dashboard backend fills a MySQL database, so you need a MySQL installation
on your host PC.

Example fedora setup
....................

::

  yum install mysql-community-server

Create a database named `tbot_root`:

::

  mysql -u root -p
  CREATE SCHEMA tbot_root;

Create in database tbot_root a table for tbot with

::

  $ mysql tbot_root -u tbot -p  < src/files/mysql/tbot_root.sql
  Enter password: 
  $

Create user "tbot" and grant all privileges on the created database:

::

  CREATE USER 'tbot'@'localhost' IDENTIFIED BY 'tbot';
  GRANT ALL PRIVILEGES ON tbot_root.tbot_results TO 'tbot'@'localhost';
  FLUSH PRIVILEGES;


If you want to use another name for the database, replace "tbot_root"
with the name you use. In this case, also edit

https://github.com/hsdenx/tbot/blob/master/src/common/tbot_event.py

the line:

::

  self.dashboard = dashboard(self.tb, 'localhost', 'tbot', 'tbot', 'tbot_root', 'tbot_results')

replace "tbot_root" with the name you use. Also, if you have other user / password
settings adapt them in this line.

Now you should see after tbot finished a new entry in your database.

Now, as the tbot results are in the database, you may want to setup a webserver
to have the tbot result visible on a webpage, so:

Setting up the Web server
.........................

::

  yum install httpd

Allow the default HTTP and HTTPS ports through the firewall

::

  firewall-cmd --permanent --add-port=80/tcp
  firewall-cmd --permanent --add-port=443/tcp
  firewall-cmd --reload

and start Apache

::

  systemctl start httpd

A simple php script, which you can open in a webbroser:

https://github.com/hsdenx/tbot/blob/master/src/dashboard/read_db.php

edit your database settings in the file:

https://github.com/hsdenx/tbot/blob/master/src/dashboard/konfiguration.php

The dashboard event backend expect the webservers root dir in

"/var/www/html"

If this is not the case for you, edit

https://github.com/hsdenx/tbot/blob/master/src/common/event/dashboard.py

the variable "self.webdir" (and send a patch, which makes this configurable)

Now copy the files from `src/dashboard/` to `/var/www/html` on your host PC, and
open in your browser the following page:

::

  http://localhost/read_db.php

If you want to reset the dashboard:

complete reset

::

  truncate tbot_root.tbot_results;

delete the last XXX entries:

::

  DELETE FROM tbot_root.tbot_results ORDER BY id DESC limit XXX;


tbot install documentation backend
----------------------------------

Enable the documentation backend in tbot

.. image:: image/guide/guide_backend_documentation_enable.png

For getting all logfiles we must get current U-Boot code,
compile and install it on the BeagleoneBlack, see the section:

`tbot compile, install U-Boot on the bbb`_

Also we must create all lofiles for the so called duts testcases:

.. image:: image/guide/guide_backend_documentation_run.png

make sure, you have created the "logfiles" directory in tbots root source, where
the documentation backend saves the logfiles.

After tbot has finsihed, you have a lot of logfiles in "logfiles".

You can use them now, to integrate them into rst files ...

You need also the tool "ansi2txt" for removing ansi escape sequences.

https://sourceforge.net/projects/ansi2txt/files/latest/download

https://sourceforge.net/p/ansi2txt/wiki/Home/

before using the logfiles, remove the escape sequences from some logfiles (yes,
it is not so easy to call ansi2txt for all files, because ansi2txt may removes
to much ... so this is in experimental state) with:

::

  for f in logfiles/*.txt;
  do
    # echo "Processing $f file..";
    # check if it contains escape sequences
    grep -q $'\x1B' $f
    if [ $? -eq 0 ]; then
      echo 'FOUND '$f
      ansi2txt $f > tmp.txt
      mv tmp.txt $f
    fi
  done


I started to documentate U-Boot, so see this as an example:

All files for creating an U-Boot doc are in the directory:

https://github.com/hsdenx/tbot/blob/master/src/documentation

Now copy all files from "logfiles" into "src/documentation/logfiles"

Then goto into src/documentation

and start the "make_doku.sh" script. It does all the needed things
for creating an U-Boot documentation with logs from the BeagleBoneBlack board.


You find the resulting pdf here (work in progress):

https://github.com/hsdenx/tbot/blob/master/src/documentation/pdf/dulg_bbb.pdf

Remark: I try to port the DULG, see

http://www.denx.de/wiki/view/DULG/UBoot

as a first step, then may I extend/rework this.

Help is welcome!


tbot compile, install U-Boot on the bbb
---------------------------------------

This section describes, what you must do, for setting up to start testcase:

https://github.com/hsdenx/tbot/blob/master/src/tc/demo/tc_demo_part1.py

which does:

- get current mainline u-boot code
- configure, compile it for the bbb
- install the resulting binary on the bbb
- do a small u-boot help command test

prerequisite:

- git must be installed on your LabPC
- you need an installed cross toolchain on your LabPC
- running tftp server on your LabPC

setup working directory for tbot on the LabPC:

edit in config/lab_hs_laptop.py

.. image:: image/guide/guide_demo1_lab_config.png

I hope the names are self explaining. Simple set here, which
directories tbot uses on your LabPC.

Edit in this file also the settings for your tftp server and
the ip config in U-Boot for your beagleboneblack:

.. image:: image/guide/guide_demo1_lab_config_tftpserver.png

set the toolchain you want to use for compiling U-Boot.

Edit config/beagleboneblack.py

.. image:: image/guide/guide_demo1_toolchain.png

create in your tftpdirectory a subdirectory "beagleboneblack/tbot"

copy the U-Boot Environment file from 

https://github.com/hsdenx/tbot/blob/master/src/files/uboot_env/beagleboneblack.env

into your tftp directory "beagleboneblack/tbot". May you need to adapt
the values mlofile and ubfile:

.. image:: image/guide/guide_demo1_uboot_env_comment.png


tbot copies the results from the build into it. After a successfull
tbot run, this looks for me:

.. image:: image/guide/guide_demo1_lab_tftpdir_result.png

Now you are ready to start tbot:

.. image:: image/guide/guide_demo1_tbot_run.png

You see the status output, which is default enabled for the
beagleboneblack. If you do not want to see this messages you
can disable them in the file config/beagleboneblack.py

.. image:: image/guide/guide_demo1_disable_statusprintf.png

The messages "ERROR - TC ends without prompt read" you can ignore,
as we issue 2 times a reset to the board. If I find time, I fix this.

tbot switch bootmodes on the beagleboneblack
--------------------------------------------

Buy a relay, for this guide I use [4]

connect the USB relay to your LabPC and check dmesg

::

  [18797.469787] usb 1-4.3: new full-speed USB device number 12 using xhci_hcd
  [18797.549695] usb 1-4.3: New USB device found, idVendor=0403, idProduct=6001
  [18797.549700] usb 1-4.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
  [18797.549703] usb 1-4.3: Product: FT245R USB FIFO
  [18797.549705] usb 1-4.3: Manufacturer: FTDI
  [18797.549707] usb 1-4.3: SerialNumber: AI0537VO
  [18798.736452] usbcore: registered new interface driver ftdi_sio
  [18798.736501] usbserial: USB Serial support registered for FTDI USB Serial Device
  [18798.736622] ftdi_sio 1-4.3:1.0: FTDI USB Serial Device converter detected
  [18798.736722] usb 1-4.3: Detected FT232RL
  [18798.738260] usb 1-4.3: FTDI USB Serial Device converter now attached to ttyUSB1
  hs@localhost:tbot  [master] $


install drivers:

Ok, this relay is very bad. It comes with no documentation at all :-(

First I had to install pyusb:

https://github.com/walac/pyusb

than the pyrelayctl tool from

https://github.com/xypron/pyrelayctl/tree/master

and I can access the relay

list all usb relay devices

.. image:: image/guide/guide_relais_list_devices.png

switch usb relay off

.. image:: image/guide/guide_relais_off.png

switch usb relay on

.. image:: image/guide/guide_relais_on.png


but this does works only with python3
for some reasons on my laptop this will not work ... :-(

Also, there is a jumper on the board, but not connected when I got my relay card.
After attaching a cable

.. image:: image/guide/guide_relais_jumper_small.jpg

the LED is now working, which indicates the state of the
relays ... I can see the led going on/off when issuing the
cmd, but the relays is not really working ... damn ...

Okay, after one more frustrating day, I found the issue ... I have the 12V
one, not the 5V one ... the relays on my board need an external 12V power unit.

After connecting such a 12V power unit it works :-D

Ok, as python3 does not really work on my laptop, try libftdi:

You find my (not very nice) source code for using this relay under linux

https://github.com/hsdenx/tbot/blob/master/src/files/relay/simple.c

This needs libftdi installed:
http://www.ftdichip.com/Drivers/D2XX.htm

and the simple.c code is based on the examples which comes with libftdi.

compile it with:

::

  $ gcc -o simple simple.c -L. -lftd2xx -Wl,-rpath /usr/local/lib
  $

usage:

./simple [state] [mask]

I connected the bootmode selection pins from the bbb to port 1 of the usb relay

.. image:: image/guide/guide_relais_bbb.jpg

Now testing the bootmode with

USB relay off -> boot from internal emmc

::

  [root@localhost simple]# /home/hs/Software/usbrelais/src/simple 0 15
  Device 0 Serial Number - AI0537VO
  state: 0 mask: 15
  [root@localhost simple]#

USB relay on -> boot from SD card

::

  [root@localhost simple]# /home/hs/Software/usbrelais/src/simple 1 15
  Device 0 Serial Number - AI0537VO
  state: 1 mask: 15
  [root@localhost simple]#

Now we can try this with the 

https://github.com/hsdenx/tbot/blob/master/src/tc/linux/relay/tc_linux_relay_set.py

testcase. You need to setup your specific relay settings in

https://github.com/hsdenx/tbot/blob/master/src/tc/linux/relay/tc_linux_relay_get_config.py

.. image:: image/guide/guide_relais_get_config_explained.png

input is state/port, so all your usb relays you use in your vlab, must
have unique port strings! No problem, as you can define them in this file.

In my setting above, I have connected port 1, so I can switch port state
with tbot:

SD

.. image:: image/guide/guide_relais_set_on.png

emmc

.. image:: image/guide/guide_relais_set_off.png

On the console you should see how U-Boot boots from different boot media.

tbot write a testcase
=====================

ToDo

- copy a already existing one
- modify it for your needs

tbot function name glossar
--------------------------

eof_= exit on failure

end tbot when the function ends False. So you save
a lot of

::

  if ret = False:
      tb.end_tc(False)

constructs
              
rup_= read until prompt

This functions reads until prompt. You do not need to
wait for a prompt after this function finished.

Tips
====

interactive power mode
----------------------

If you do not have a power controller handy, or you want to
start fast with tbot, you may interested in powering on/off
the board with your hands ... so there is a testcase for this
usecase:

https://github.com/hsdenx/tbot/blob/master/src/tc/lab/denx/tc_lab_interactive_power.py

Do all the setup steps from `install paramiko on [5]`_ until `copy some existing lab config to your new config`_

Now, simply change in your new lab config file, you created:

.. image:: image/guide/guide_interactive_power.png


and continue with the step `Adapt the setting for accessing your labPC`_

(Of course without step `Adapt settings for Gembird Powercontroller`_)

Here an example gif "video":

.. image:: image/guide/guide_interactive.gif

This is also a good example, how you can use tbot with another power controller, so:

Using tbot without Gembirds powercontroller
-------------------------------------------

You must have the possibility to power on the board through
a cmdline on the LabPC. Then you can write a new tbot testcase, which exactly
does this for you, and simply set the "tc_lab_denx_power_tc" value in your
lab config file to the name of your new testcase.
tbot uses than your testcase for powering on / off the board.

see for example:

`interactive power mode`_

In your new testcase, look at "tb.power_state" to get the info, if
you must power on or off the board.

May you have the possibility to controll more than one board with
your power controller, than you can differ between the different
boards in your power testcase through the config variable:

::

  tb.config.boardlabpowername

If you have the possibility to read back the current state of the
power to your board, you should also write a testcase for this,
and add the name of your new testcase to "tc_lab_denx_get_power_state_tc"

Your new testcase should set

::

        tb.power_state = 'on'

if the power is on
or

::

        tb.power_state = 'off'

if the power is off.

If you cannot read back the state, simply return True, and tbot uses the last
state it set ... not perfect, but better than nothing ...
