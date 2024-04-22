# talking-plant
Final Project for CS437

## connecting a bluetooth speaker to your pi:
https://www.okdo.com/project/set-up-a-bluetooth-speaker-with-a-raspberry-pi/
To get the MAC address of your speaker, you can use your computer (Mac in my case) to scan the BT list with this command:
`system_profiler SPBluetoothDataType`

1. **Enable Bluetooth:** Make sure the Bluetooth service is enabled on your Raspberry Pi. You can do this by running **`sudo systemctl enable bluetooth`** and **`sudo systemctl start bluetooth`** in the terminal.
2. **Install Bluetooth Tools:** If not already installed, you may need to install some tools to help manage Bluetooth devices. You can do this by running **`sudo apt-get install bluez pulseaudio-module-bluetooth`** in the terminal.
3. **Pair the Speaker:** Use the command **`bluetoothctl`** to enter the Bluetooth control interface. Then use the following commands to pair and connect your speaker:
    - **`power on`**: Turns on the Bluetooth controller.
    - **`agent on`**: Enables the Bluetooth agent that will handle authentication.
    - **`default-agent`**: Sets the current agent as the default one.
    - **`scan on`**: Starts scanning for nearby Bluetooth devices.
    - **`pair <MAC_ADDRESS>`**: Replace **`<MAC_ADDRESS>`** with the MAC address of your Bluetooth speaker. This will pair your Raspberry Pi with the speaker.
        - headset (epos 300): 00:16:94:5C:05:E8
    - **`trust <MAC_ADDRESS>`**: This marks the speaker as trusted.
    - **`connect <MAC_ADDRESS>`**: Connects to the speaker.
  
   
If encountering issues with the connection step, make sure you have trusted the device. If it is still not working, try restarting the pulseaudio-module-bluetooth step:
`pulseaudio -k`
`pulseaudio --start`
source: https://unix.stackexchange.com/questions/258074/error-when-trying-to-connect-to-bluetooth-speaker-org-bluez-error-failed
