# Setup
Set up a fresh installation of [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)



### Install WFS remote
1. Connect a keyboard or access the Raspberry PI over SSH using its IP. Default credentials:
   * Username: "pi"  
   * Password: "raspberry"

2. Enter the following commands:

   ```bash
   # Get latest code
   cd /home/pi
   git clone https://github.com/sonovice/wfs.git
   
   # Install dependencies
   sudo apt update && sudo apt install -y \
       python3 \
       python3-pip \
       libsdl2-dev \
       libsdl2-image-dev \
       libsdl2-mixer-dev \
       libsdl2-ttf-dev \
       libportmidi-dev \
       libswscale-dev \
       libavformat-dev \
       libavcodec-dev \
       zlib1g-dev
   pip3 install kivy rpi.gpio mock.gpio

   # Add script to autostart
   sudo sed -i 's|^exit 0|python3 /home/pi/wfs/src/main.py \&\n&|g' /etc/rc.local
   ```
3. Reboot
