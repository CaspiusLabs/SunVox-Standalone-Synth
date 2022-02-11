# Sunvox Standalone DIY Synth
## Make your own portable Raspberry Pi synth!
https://www.caspiuslabs.com/portfolio/sunvox-standalone-synth/

## Installation instructions:

> CONFIG EDIT

    sudo nano /boot/config.txt

    disable_splash=1
    disable_overscan=1
    hdmi_force_hotplug=0
    hdmi_ignore_edid_audio=1

    dtparam=audio=on
    audio_pwm_mode=2

    dtoverlay=pi3-disable-bt
    dtoverlay=gpio-shutdown

> COMMANDS

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get dist-upgrade
    sudo apt-get install libsdl2-2.0-0 python-uinput

    wget -c http://warmplace.ru/soft/sunvox/sunvox-1.9.6c.zip
    unzip -p sunvox-1.9.6c.zip sunvox/sunvox/linux_arm_armhf_raspberry_pi/sunvox > /home/pi/sunvox

    chmod +x /home/pi/sunvox
    chmod +x /home/pi/encoder.py
    sudo mv sunvox /usr/bin/sunvox
    sudo mv encoder.py /usr/bin/encoder.py
    sudo chown root /usr/bin/sunvox
    sudo chown root /usr/bin/encoder.py

> cmdline.txt EDIT

    sudo nano /boot/cmdline.txt

    console=tty3 loglevel=3 rd.udev.log_priority=3 splash quiet plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0

> /etc/modules EDIT

    sudo nano /etc/modules

    # /etc/modules: kernel modules to load at boot time.
    #
    # This file contains the names of kernel modules that should be loaded
    # at boot time, one per line. Lines beginning with "#" are ignored.

    uinput

> Services EDIT

    sudo nano /lib/systemd/system/sunvox.service

    [Unit]
    Description=SunVox
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=/usr/bin/sunvox

    [Install]
    WantedBy=multi-user.target

    sudo nano /lib/systemd/system/encoder.service

    [Unit]
    Description=Encoder
    After=multi-user.target

    [Service]
    Type=idle
    ExecStart=sudo python /usr/bin/encoder.py

    [Install]
    WantedBy=multi-user.target

> COMMANDS

    sudo chmod 644 /lib/systemd/system/encoder.service
    sudo chmod 644 /lib/systemd/system/sunvox.service
    sudo systemctl daemon-reload
    sudo systemctl enable encoder.service
    sudo systemctl enable sunvox.service

    alsamixer
    sudo reboot

> Sunvox config file EDIT

    sudo nano /sunvox_config.ini

    startmsg 1
    audiodriver alsa
    audiodevice hw:0,0
    audiodevice_in hw:0,0
    frequency 96000
    midi_kbd "USB Midi MIDI 1"
    midi_kbd_ch 1
    hdiv1_y 40
    hdiv2_y 432
    vdiv1_x 99
    width 800
    height 600
    softrender 
    fullscreen 
    maximized 
    nocursor 
    touchcontrol 
    show_virt_kbd 
    auto_session_restore 1
    ppi 110
    scale 350
    fscale 400
    builtin_theme 18
    fpreview_ys 48
    fpreview 1

