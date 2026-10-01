# ModuDeck
A modular-plane portable computer concept — by Samuele.

## Project
A laptop-style upper PC with a display, a fixed keyboard and foldable touchpad above a small phone, and a phone-style numeric keypad on the right. Current scope: the PC and three empty full-footprint stackable layers, with cable access, side fasteners and connector placeholders. Drone and other expansion electronics are deferred.

**Status: concept.** Preliminary dimensions are 320 × 230 mm. No electronics, charging, radio connectivity, or electrical compatibility has been validated. Electronic part models are currently simple silhouettes.

## Open in 3D
- Open `cad/modudeck.scad` in OpenSCAD.
- Press F5 for preview, F6 for geometry.
- `exploded=false` shows the assembled layers.
- `phone_open=false` closes the touchpad.
- The individual parts are in `cad/parts/`.

## Generate STL files and viewer
With Python 3 and OpenSCAD installed:
```bash
python scripts/build.py
```
Then open `ModuDeck-parts-3D.html`: a menu of all parts, rotation, and zoom. No external web libraries are required.

On GitHub: **Actions → Build 3D models → Run workflow** creates a ZIP with source files, STL models, catalog, and viewer. The workflow is manual; it was not run during the initial upload.

## Documentation
- [Parts catalog](docs/PARTS.md)
- [Decisions still to be made](docs/DESIGN.md)
- [Materials list to complete](BOM.csv)
- [Personal journal](JOURNAL.md)

The concept and initial sources were developed with AI assistance. Record only actual personal work and time in the journal; no funding or completion is declared.
## Earlier concept sketch
This sketch predates the simplification; drone and populated expansion floors are deferred. 
<img width="1536" height="1024" alt="blueprint2" src="https://github.com/user-attachments/assets/1667dc44-f59c-4911-91a6-c5c131656df9" />
