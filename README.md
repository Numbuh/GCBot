# Raspberry Pi Pico GameCube Controller Script Player

This software allows for the playback of custom GameCube controller input scripts on console using a Raspberry Pi Pico. Connect an exposed GameCube cable dataline to a Wii or GameCube console for perfect precision playback of custom button sequences and analog stick movements.

This project is forked from [pico-rectangle](https://github.com/JulienBernard3383279/pico-rectangle) as data encoding and transmission timings are already handled.

Please consult the [Legal information and license](https://github.com/JulienBernard3383279/pico-rectangle#legalInformationAndLicense) section in the upstream repository before using this firmware.

## Hardware Required

In order to achieve playback, you'll need:
- [Raspberry Pi Pico](https://a.co/d/1lbuRqZ)
- [2x 20-pin headers](https://a.co/d/4R5S7OQ)
- [Breadboard kit](https://a.co/d/5nFPmrP)
- [Soldering iron + solder](https://a.co/d/6OQDzBK)
- [Gamecube cable](https://a.co/d/5JQs53b)
- [28 gauge wire stripper](https://a.co/d/e9WKf9y)
- [2.54mm Dupont connector kit](https://a.co/d/8zIctFd)
- [SN-28B Crimper](https://a.co/d/5cAGSTc)

#### Improvements to Hardware Required

I bought stuff before I had an actual game plan, so I didn't consider that the Pico didn't come with header pins already. You can find these pre-soldered online for near the same price, if you don't have your own soldering kit. If you DO have your own soldering kit, then you can probably skip purchasing the breadboard kit, the Dupont connectors, and the crimper. For the Gamecube cables, you could also just sacrifice an old controller.

## Steps to Assemble

1. Solder the Pico to header pins. Unlike other Raspberry Pis, the Pico does not come with headers pre-soldered. Connect Pico headers to breadboard kit.
2. Cut off the end of the Gamecube cable that does **NOT** plug into the console. Strip the housing off with something like an exacto knife.
3. Locate the data wire. On OEM cables this is the red one, but if using a third-party controller, you should determine the cable by opening the housing on both ends and comparing with a diagram of the pins in the controller port.
4. Crimp the data wire to a Dupont connector. Plug the data wire into the GP28 pin on the breadboard kit.
5. (Optional) Locate the 3.3V wire. Crimp that as well and plug into VSYS. Alternatively, you can skip this step if you plan to power the Pico via USB. NOTE: **If you do this step, do NOT have this board plugged via USB and via its Gamecube port at the same time. This would feed the USB 5v to the 3v line of the console and likely damage it.**

## Install Dependencies

For easiest install, I suggest using a Unix environment since that's what I used. Specifically, I just used Ubuntu running through `wsl`.
- `sudo apt-get install build-essential gcc-arm-none-eabi cmake python3 -y`

## Creating Custom Scripts

Scripts are created using the `generate_script.py` Python tool. This tool converts human-readable script commands into binary files that the Pico can read.

### Script Format

The script generator takes a list of commands, where each command has:
- **duration**: Number of frames (at 59.94 fps, so 60 frames ≈ 1 second)
- **buttons**: Space-separated list of buttons to press: `A B X Y START L R Z DUP DDOWN DLEFT DRIGHT`
- **stick_x**: Left analog X position (0-255, 128 is neutral, 0 is left, 255 is right)
- **stick_y**: Left analog Y position (0-255, 128 is neutral, 0 is down, 255 is up)
- **c_stick_x**: C-stick X position (0-255)
- **c_stick_y**: C-stick Y position (0-255)
- **analog_l**: L trigger analog pressure (0-255)
- **analog_r**: R trigger analog pressure (0-255)

### Example: Creating a Custom Script

Edit `generate_script.py` and modify the `commands` list. For example:

```python
commands = [
    # Hold up for 5 seconds (300 frames)
    (300, "", 128, 205, 128, 128, 0, 0),
    
    # Press A while holding neutral stick for 60 frames (1 second)
    (60, "A", 128, 128, 128, 128, 0, 0),
    
    # Hold right + B for 120 frames (2 seconds)
    (120, "B", 205, 128, 128, 128, 0, 0),
    
    # Press A+B+START for 10 frames
    (10, "A B START", 128, 128, 128, 128, 0, 0),
]
```

### Useful Analog Stick Values

For precise movement, here are the main stick positions:
- **Neutral**: `128`
- **Full left/down**: `59`
- **Full right/up**: `205`
- **Slight movements**: Values between 59-128 (left/down) or 128-205 (right/up)

### Running the Script Generator

```bash
python3 generate_script.py output_filename.bin
```

This will create a binary file ready to be used by the Pico.

## How to Build and Run

1. Clone repo.
2. Create your custom script by editing `generate_script.py` and running it to generate a `.bin` file:
   ```bash
   python3 generate_script.py my_script.bin
   ```
3. Edit `src/file.S` and change the `.incbin` line to point to your script file:
   ```asm
   .incbin "../my_script.bin"
   ```
4. Starting from the root directory, run the following:
   ```bash
   mkdir -p build
   cd build
   cmake ..
   make
   ```
5. With the Pico USB disconnected, hold down the BOOTSEL button on-board the Pico, and plug the Pico into your computer.
6. Copy the `pico_tas_playback.uf2` file from the build directory to the Pico which should appear as a new drive.
7. Disconnect the Pico from your computer.
8. Plug the Pico's Gamecube wire into the console. If you skipped step 5 of assembly, plug the Pico back into your computer for power.
9. The Pico will now play your custom script!

## Example Scripts Included

- **hold_up_5sec.bin**: Holds the analog stick up for 5 seconds (300 frames)

## Controller Input Specifications

The GameCube controller sends 8 bytes of data per poll:

```
Byte 0-1: Button states
Byte 2: Left analog stick X (0-255, 128 neutral)
Byte 3: Left analog stick Y (0-255, 128 neutral)
Byte 4: C-stick X (0-255, 128 neutral)
Byte 5: C-stick Y (0-255, 128 neutral)
Byte 6: L trigger analog (0-255)
Byte 7: R trigger analog (0-255)
```

## Technical Details

- **Frame Rate**: 59.94 fps (used by GameCube/Wii)
- **Reconnection Delay**: 283 frames (~4.7 seconds) to account for controller reconnect screen
- **Data Pin**: GP28 on Raspberry Pi Pico
- **Communication Protocol**: Uses PIO (Programmable I/O) for precise timing

## Advanced: Creating Complex Scripts

You can create sophisticated scripts by chaining multiple commands. For example, a Super Smash Bros. Melee combo:

```python
commands = [
    # Short hop (3 frame jump press)
    (3, "X", 128, 128, 128, 128, 0, 0),
    # Release jump
    (7, "", 128, 128, 128, 128, 0, 0),
    # Forward aerial during jump
    (4, "A", 205, 128, 128, 128, 0, 0),
    # Wait to land
    (30, "", 128, 128, 128, 128, 0, 0),
]
```

## Troubleshooting

- **Script doesn't play**: Make sure you've updated `src/file.S` to point to your new script file
- **Inputs seem delayed**: This is normal - there's a 283 frame reconnection period
- **Analog stick not reaching edges**: Use values 59 (min) and 205 (max) for full range
- **Need to test quickly**: Build time is about 30 seconds, and flashing takes a few seconds

## License

See the upstream [pico-rectangle](https://github.com/JulienBernard3383279/pico-rectangle) repository for license information.
