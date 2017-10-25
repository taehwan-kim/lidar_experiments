===========================================================
Installation instructions:
===========================================================
1. Extract the contents of the CONEX-CC_NSTRUCT_USB_Driver_2.08.02.zip somewhere.
2. Plug in Newport motor controller into USB, windows will complain that no driver is installed
3. Goto the Control Panel->System->Device Manager
4. Right-click on the Newport Conex-CC and select "Update Drivers"
5. Choose to find driver location manually and select the folder you extracted the zip archive to
6. Windows will install the driver for you
7. Next, windows will complain about unable to install the serial port drivers
8. In device manager, right-click on the serial port and select "Update Drivers"
9. Choose to find driver location manually and select the folder you extracted the zip archive to again
10. Windows will install the driver for you and you will be done.

===========================================================
GUI Interface to the laser (requires Java):
===========================================================
Use this to control Jason's ECL laser easily through mouse/keyboard.
Keep the rxtxserial.dll in this folder and run with:

    java -jar eclgui.jar

The default COM Port is 3, if you need to use a different COM port, pass it
in through command line arguments:

    java -jar eclgui.jar -com <COMPORT>

After the GUI starts, press "Connect" to connect to the laser through the COM port
and "Disconnect" to disconnect from the laser through the COM port. "Home" homes
the laser and "Quit" exits the program.

The wavelength that the laser is set to is shown by the "Set: XXXX.XXX nm" label.
The actual laser wavelength, calculated based on the current motor position is
shown by the "Act: XXXX.XX nm" label. Change the set wavelength by pressing the
"^" and "v" buttons, the up/down keys on the keyboard, or by scrolling with the
mouse wheel. Change the step-size (shown by the "St. XX.XXX label") by pressing
the "<" and ">" buttons or the left/right keys on the keyboard.
