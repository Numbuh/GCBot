#!/usr/bin/env python3
"""
GameCube Controller Script Generator
Creates binary script files for the Pico TAS playback project.
"""

import struct
import argparse
import sys

# GCPadStatus structure (8 bytes)
# Bytes 0-1: Button bits
# Byte 2: Left stick X (0-255, 128 = neutral)
# Byte 3: Left stick Y (0-255, 128 = neutral)
# Byte 4: C-stick X (0-255, 128 = neutral)
# Byte 5: C-stick Y (0-255, 128 = neutral)
# Byte 6: L trigger analog (0-255)
# Byte 7: R trigger analog (0-255)

# Button bit mapping:
# Byte 0: a, b, x, y, start (bits 0-4)
# Byte 1: dLeft, dRight, dDown, dUp, z, r, l (bits 0-6)

BUTTON_BITS = {
    'A': (0, 0),
    'B': (0, 1),
    'X': (0, 2),
    'Y': (0, 3),
    'START': (0, 4),
    'DLEFT': (1, 0),
    'DRIGHT': (1, 1),
    'DDOWN': (1, 2),
    'DUP': (1, 3),
    'Z': (1, 4),
    'R': (1, 5),
    'L': (1, 6),
}

def create_pad_status(buttons_str, stick_x, stick_y, c_stick_x, c_stick_y, analog_l, analog_r):
    """Create a GCPadStatus byte array from parameters."""
    button_bytes = [0, 0]
    
    if buttons_str:
        for button in buttons_str.upper().split():
            if button in BUTTON_BITS:
                byte_idx, bit = BUTTON_BITS[button]
                button_bytes[byte_idx] |= (1 << bit)
    
    # Pack as: byte0, byte1, xStick, yStick, cxStick, cyStick, analogL, analogR
    # Note: pad1 bit should be set (bit 7 of byte 1) for proper controller detection
    button_bytes[1] |= 0x80  # Set pad1 bit
    
    return struct.pack('BBBBBBBB',
        button_bytes[0],
        button_bytes[1],
        stick_x & 0xFF,
        stick_y & 0xFF,
        c_stick_x & 0xFF,
        c_stick_y & 0xFF,
        analog_l & 0xFF,
        analog_r & 0xFF
    )

def create_script(commands, output_file):
    """Create a binary script file from a list of commands."""
    if len(commands) > 65535:
        print(f"Error: Too many commands ({len(commands)}). Maximum is 65535.", file=sys.stderr)
        sys.exit(1)
    
    with open(output_file, 'wb') as f:
        # Write command count (big endian)
        f.write(struct.pack('>H', len(commands)))
        
        # Write each command
        for duration, buttons, sx, sy, cx, cy, al, ar in commands:
            if duration < 1 or duration > 65535:
                print(f"Warning: Duration {duration} is out of range. Clamping to 1-65535.", file=sys.stderr)
                duration = max(1, min(65535, duration))
            
            # Write duration (big endian)
            f.write(struct.pack('>H', duration))
            
            # Write pad status
            pad_status = create_pad_status(buttons, sx, sy, cx, cy, al, ar)
            f.write(pad_status)
    
    print(f"✓ Created script: {output_file}")
    print(f"  Commands: {len(commands)}")
    total_frames = sum(cmd[0] for cmd in commands)
    print(f"  Total frames: {total_frames} (~{total_frames/60:.1f} seconds)")

# Preset scripts
def get_hold_up_5sec():
    """Hold analog stick up for 5 seconds (300 frames)."""
    return [
        (300, "", 128, 205, 128, 128, 0, 0),
    ]

def get_zone_reset():
    """
    Zone reset script: move up, hit A, move up, hit Start, hit A twice.
    Loops forever in C++ code (single iteration here).
    """
    commands = [
        (20, "", 128, 128, 128, 128, 0, 0),   # Neutral state at start (ensures clean loop restart)
        (90, "B", 128, 205, 128, 128, 0, 0),  # Move up + B for 1.5 sec
        (80, "", 128, 128, 128, 128, 0, 0),   # Buffer
        (5, "A", 128, 128, 128, 128, 0, 0),   # Press A
        (150, "", 128, 128, 128, 128, 0, 0),  # Buffer for loading screen
        (20, "START", 128, 128, 128, 128, 0, 0),  # Press Start (longer press - some games need longer)
        (40, "", 128, 128, 128, 128, 0, 0),   # Buffer after Start
        (5, "A", 128, 128, 128, 128, 0, 0),   # Press A
        (40, "", 128, 128, 128, 128, 0, 0),   # Buffer between A presses
        (5, "A", 128, 128, 128, 128, 0, 0),   # Press A again
        (180, "", 128, 128, 128, 128, 0, 0),  # Buffer before loop
    ]
    return commands

def get_bench_reset():
    """Bench reset: hold down, hit A five times, pause 15 seconds."""
    return [
        (30, "", 128, 59, 128, 128, 0, 0),    # Hold down
        (5, "A", 128, 128, 128, 128, 0, 0),
        (5, "A", 128, 128, 128, 128, 0, 0),
        (5, "A", 128, 128, 128, 128, 0, 0),
        (5, "A", 128, 128, 128, 128, 0, 0),
        (5, "A", 128, 128, 128, 128, 0, 0),
        (900, "", 128, 128, 128, 128, 0, 0),  # 15 sec pause
    ]

def get_circle_motion():
    """Rotate analog stick in a circle through 8 positions."""
    commands = []
    positions = [
        (205, 128),  # Right
        (205, 205),  # Up-Right
        (128, 205),  # Up
        (59, 205),   # Up-Left
        (59, 128),   # Left
        (59, 59),    # Down-Left
        (128, 59),   # Down
        (205, 59),   # Down-Right
    ]
    for x, y in positions:
        commands.append((60, "", x, y, 128, 128, 0, 0))
    return commands

def get_button_test():
    """Test all buttons sequentially."""
    buttons = ['A', 'B', 'X', 'Y', 'START', 'Z', 'L', 'R', 'DUP', 'DDOWN', 'DLEFT', 'DRIGHT']
    commands = []
    for button in buttons:
        commands.append((5, button, 128, 128, 128, 128, 0, 0))
        commands.append((30, "", 128, 128, 128, 128, 0, 0))
    return commands

def get_wavedash():
    """Super Smash Bros. Melee wavedash example."""
    return [
        (3, "X", 128, 128, 128, 128, 0, 0),      # Jump
        (1, "", 128, 128, 128, 128, 0, 0),       # Wait
        (4, "L", 179, 68, 128, 128, 255, 0),     # Airdodge down-right
        (20, "", 128, 128, 128, 128, 0, 0),      # Recover
    ]

def main():
    parser = argparse.ArgumentParser(description='Generate GameCube controller script files')
    parser.add_argument('output', help='Output binary file path')
    parser.add_argument('--preset', choices=['hold_up_5sec', 'zone_reset', 'bench_reset', 
                                            'circle_motion', 'button_test', 'wavedash'],
                       help='Use a preset script')
    
    args = parser.parse_args()
    
    if args.preset:
        preset_map = {
            'hold_up_5sec': get_hold_up_5sec,
            'zone_reset': get_zone_reset,
            'bench_reset': get_bench_reset,
            'circle_motion': get_circle_motion,
            'button_test': get_button_test,
            'wavedash': get_wavedash,
        }
        commands = preset_map[args.preset]()
    else:
        # Default: zone_reset (most commonly used)
        print("No preset specified. Using 'zone_reset' as default.", file=sys.stderr)
        commands = get_zone_reset()
    
    create_script(commands, args.output)

if __name__ == '__main__':
    main()

