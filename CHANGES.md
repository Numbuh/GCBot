# Changes Summary

## What Changed

This project has been converted from reading Mario Kart Wii ghost files (RKG format) to reading custom script files that you can easily create and modify.

## New Features

### 1. Simple Script Format
- Binary format that's generated from Python
- Easy to create custom controller input sequences
- Frame-precise input control

### 2. Script Generator Tool (`generate_script.py`)
- Generate scripts from command-line with presets
- Edit the file directly to create custom scripts
- Built-in presets: `hold_up_5sec`, `circle_motion`, `button_test`, `wavedash`

### 3. New Files Created

| File | Purpose |
|------|---------|
| `ScriptReader.hpp` | Header for script reading class |
| `ScriptReader.cpp` | Implementation of script reader |
| `generate_script.py` | Python tool to generate script files |
| `hold_up_5sec.bin` | Example: Hold stick up for 5 seconds |
| `circle_motion.bin` | Example: Rotate stick in circle |
| `button_test.bin` | Example: Test all buttons |
| `wavedash.bin` | Example: SSBM wavedash |
| `QUICKSTART.md` | 5-minute getting started guide |
| `SCRIPT_GUIDE.md` | Comprehensive scripting reference |
| `CHANGES.md` | This file |

### 4. Modified Files

| File | Changes |
|------|---------|
| `src/main.cpp` | Now uses `ScriptReader` instead of `RKGReader` |
| `src/file.S` | Now includes `.bin` script file instead of `.rkg` |
| `CMakeLists.txt` | Builds `ScriptReader.cpp` instead of `RKGReader.cpp` |
| `README.md` | Complete rewrite for new script system |

### 5. Files No Longer Used

The following files are still in the project but no longer used:
- `RKGReader.hpp` - Replaced by `ScriptReader.hpp`
- `RKGReader.cpp` - Replaced by `ScriptReader.cpp`
- `LC_Demo.rkg` - Replaced by `.bin` script files

## Key Differences from RKG System

### Before (RKG)
- Complex binary format from Mario Kart Wii
- YAZ1 compression
- Specific to Mario Kart Wii ghosts
- Difficult to create custom sequences
- Required hex editing or ghost extraction

### After (Script)
- Simple binary format
- No compression
- Universal GameCube controller inputs
- Easy Python-based generation
- Human-readable source format

## Script Format Details

### Binary Structure
```
[2 bytes] Number of commands (big endian)
For each command:
  [2 bytes] Duration in frames (big endian)
  [8 bytes] GCPadStatus structure
```

### GCPadStatus Structure
```
Byte 0: Button bits (A, B, X, Y, START)
Byte 1: Button bits (D-pad, Z, R, L)
Byte 2: Left stick X (0-255)
Byte 3: Left stick Y (0-255)
Byte 4: C-stick X (0-255)
Byte 5: C-stick Y (0-255)
Byte 6: L trigger analog (0-255)
Byte 7: R trigger analog (0-255)
```

## Usage Example

### Create a Script
```bash
python3 generate_script.py my_script.bin --preset hold_up_5sec
```

### Or Edit generate_script.py
```python
commands = [
    # Hold up for 5 seconds
    (300, "", 128, 205, 128, 128, 0, 0),
    # Press A
    (60, "A", 128, 128, 128, 128, 0, 0),
]
```

### Update src/file.S
```asm
.incbin "../my_script.bin"
```

### Build
```bash
cd build && make
```

### Flash
Copy `pico_tas_playback.uf2` to your Pico in BOOTSEL mode.

## Compatibility

- Works with any GameCube-compatible console (GameCube, Wii)
- Works with any game that accepts GameCube controller input
- Frame-perfect accuracy maintained from original project
- Same hardware setup as before

## Performance

- No performance impact compared to RKG reader
- Actually slightly faster due to simpler parsing
- Same 59.94 fps frame timing
- Same 283-frame reconnection delay

## Future Enhancements

Possible future improvements:
- Text-based script format (CSV or JSON)
- Real-time script editing via serial
- Multiple script files with switching
- Looping support in binary format
- Script recording mode

## Migration Guide

If you were using this project with RKG files:

1. Your hardware setup stays the same
2. The Pico wiring stays the same
3. You just need to:
   - Generate new `.bin` files instead of using `.rkg` files
   - Update `src/file.S` to reference your `.bin` file
   - Rebuild and reflash

## Credits

Original RKG reading logic by the original author, adapted for custom scripts.
Script system designed for ease of use and flexibility.

## License

Same license as the original pico-rectangle project.

