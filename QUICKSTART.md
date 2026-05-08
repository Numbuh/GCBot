# Quick Start Guide

Get your custom GameCube controller scripts running in 5 minutes!

## 1. Generate Your Script

Pick a preset or create your own:

```bash
# Try one of these presets:
python3 generate_script.py my_script.bin --preset hold_up_5sec
python3 generate_script.py my_script.bin --preset circle_motion
python3 generate_script.py my_script.bin --preset button_test
python3 generate_script.py my_script.bin --preset wavedash
```

Or create a custom script by editing `generate_script.py`:
```python
commands = [
    # Format: (frames, "buttons", x, y, cx, cy, L, R)
    (300, "", 128, 205, 128, 128, 0, 0),  # Hold up 5 seconds
    (60, "A", 128, 128, 128, 128, 0, 0),  # Press A for 1 second
]
```

## 2. Update the Binary Reference

Edit `src/file.S` and change the filename:

```asm
.section .bindata , "a"
.balign 4
.global g_script
g_script:
.incbin "../my_script.bin"
```

## 3. Build the Firmware

```bash
cd build
make
```

This creates `pico_tas_playback.uf2` - the file you'll flash to your Pico.

## 4. Flash to Pico

1. Unplug your Pico from USB
2. Hold the **BOOTSEL** button on the Pico
3. Plug in the Pico (while still holding BOOTSEL)
4. Release BOOTSEL - the Pico appears as a USB drive
5. Copy `build/pico_tas_playback.uf2` to the Pico
6. The Pico will automatically restart with your script!

## 5. Use It

1. Plug the Pico's GameCube cable into your console
2. Power the Pico (via USB or through the GameCube cable if you wired 3.3V)
3. The script will start playing automatically!

## Example Scripts Included

Already generated and ready to use:

| Script | Description | Duration |
|--------|-------------|----------|
| `hold_up_5sec.bin` | Holds stick up | ~5 seconds |
| `circle_motion.bin` | Rotates stick in circle | ~4.5 seconds |
| `button_test.bin` | Tests all buttons | ~8.8 seconds |
| `wavedash.bin` | SSBM wavedash technique | ~0.6 seconds |

To use any of these, just update `src/file.S` to reference the one you want!

## Common Values

### Analog Stick Positions
- **128** = Neutral (center)
- **59** = Full left or down  
- **205** = Full right or up

### Frame Timing
- **60 frames** ≈ 1 second
- **300 frames** ≈ 5 seconds
- GameCube/Wii runs at 59.94 fps

### Buttons
`A` `B` `X` `Y` `START` `L` `R` `Z` `DUP` `DDOWN` `DLEFT` `DRIGHT`

## Need More Help?

- **Full Documentation**: See `README.md`
- **Script Examples**: See `SCRIPT_GUIDE.md`
- **Hardware Setup**: See README.md "Steps to Assemble" section

## Troubleshooting

**Script doesn't run?**
- Check that `src/file.S` points to your script file
- Rebuild with `cd build && make`
- Reflash the .uf2 to your Pico

**Inputs seem wrong?**
- Verify analog values: use 59 (min), 128 (neutral), 205 (max)
- Check button names are uppercase
- Remember: 60 frames ≈ 1 second

**Build fails?**
- Make sure you have dependencies: `sudo apt-get install build-essential gcc-arm-none-eabi cmake python3 -y`
- Run `cmake ..` from the build directory first

## Creating Your First Custom Script

1. Open `generate_script.py`
2. Find the `main()` function
3. Edit the `commands` list:

```python
commands = [
    # Press A rapidly 10 times
]
for i in range(10):
    commands.append((3, "A", 128, 128, 128, 128, 0, 0))
    commands.append((3, "", 128, 128, 128, 128, 0, 0))
```

4. Run: `python3 generate_script.py my_custom.bin`
5. Update `src/file.S` to include `my_custom.bin`
6. Build and flash!


