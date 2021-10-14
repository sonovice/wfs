# Setup
Set up a fresh installation of [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit)



### Install WFS remote
1. Connect a keyboard or access the Raspberry PI over SSH using its IP. Default credentials:
   * Username: "pi"  
   * Password: "raspberry"

2. Execute the following commands:

   ```bash
   # Install dependencies
   sudo apt update && sudo apt install -y \
       git \
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
   sudo pip3 install kivy rpi.gpio mock.gpio
   
   # Get latest code
   cd /home/pi
   git clone https://github.com/sonovice/wfs.git

   # Set static IP
   echo -e "\nauto eth0\nallow-hotplug eth0\niface eth0 inet static\naddress 192.168.1.99\nnetmask 255.255.255.0\ngateway 192.168.1.254\n" | sudo tee -a /etc/network/interfaces
   
   # Add script to autostart
   sudo sed -i 's|^exit 0|python3 /home/pi/wfs/src/main.py \&\n&|g' /etc/rc.local
   ```
3. Reboot
