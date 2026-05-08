# Ready to Use! 🎮

Your complete GameCube controller automation system is ready!

## Quick Start

### 1. Flash the Firmware
```bash
# Copy to your Pico W (hold BOOTSEL, plug in USB)
cp build/pico_tas_playback.uf2 /path/to/pico_drive/
```

### 2. Setup Python Environment
```bash
# From project directory:
source venv/bin/activate
```

### 3. Capture Timer Templates
```bash
python3 capture_timer_templates.py
```
- Press `p` when timer is at PAUSE point
- Press SPACE to capture
- Press `r` when timer is at RESUME point  
- Press SPACE to capture
- Press `q` to quit

This creates `pause_template.png` and `resume_template.png`

### 4. Update IP Address
Find your Pico W's IP (check router admin page or use a network scanner), then edit `pause_controller.py` line 20:
```python
PICO_IP = "192.168.1.XXX"  # Your Pico W's actual IP
```

### 5. Run the Controller
```bash
python3 pause_controller.py
```

Press `q` to quit, `p` for manual pause, `r` for manual resume.

## What's Included

✅ **Firmware** (`build/pico_tas_playback.uf2`)
- WiFi remote control support
- Auto-looping scripts
- Zone reset and bench reset scripts

✅ **PC Tools**
- `capture_timer_templates.py` - Capture timer positions
- `pause_controller.py` - Visual detection + remote control
- `generate_script.py` - Create custom scripts

✅ **Scripts Ready**
- `zone_reset.bin` - Auto-loops zone resets
- `bench_reset.bin` - Auto-loops with 15-sec pauses

## How It Works

1. **Pico W runs your script** (auto-loops forever)
2. **PC watches timer** via Elgato capture
3. **When timer hits transition point** → sends 'P' to pause
4. **Pico stops script** (holds neutral inputs)
5. **When transition completes** → sends 'R' to resume
6. **Pico continues** from where it paused

## Troubleshooting

**Can't connect to Pico W?**
- Check both devices on WiFi "Tardis"
- Find Pico W IP in router admin page
- Make sure Pico W is powered on

**Templates not matching?**
- Lower `MATCH_THRESHOLD` in `pause_controller.py` (line 23) for better sensitivity
- Re-capture templates if lighting/position changes

**Elgato not working?**
- Change `CAPTURE_DEVICE` to 0, 1, or 2 in both Python scripts

## Files Summary

| File | Purpose |
|------|---------|
| `build/pico_tas_playback.uf2` | Flash this to Pico W |
| `capture_timer_templates.py` | Capture timer screenshots |
| `pause_controller.py` | Main PC controller |
| `generate_script.py` | Create custom scripts |
| `zone_reset.bin` / `bench_reset.bin` | Your gameplay scripts |
| `pause_template.png` / `resume_template.png` | Timer images |

Good luck with your shiny hunting! 🌟

