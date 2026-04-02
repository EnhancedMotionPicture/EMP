# EMP

EMP is an open ecosystem for synchronizing video with haptic, air, and light cues.

## What is included
- Open `.emp.json` sidecar schema
- Example EMP file
- Simple Python CLI for validate / inspect / simulate
- Browser-based web player mockup
- Documentation and GitHub upload notes

## Quick start

### Validate an EMP file
```bash
python scripts/emp_cli.py validate examples/chase-scene.emp.json
```

### Inspect an EMP file
```bash
python scripts/emp_cli.py inspect examples/chase-scene.emp.json
```

### Simulate playback
```bash
python scripts/emp_cli.py simulate examples/chase-scene.emp.json
```

### Run the web player
```bash
python scripts/serve_web.py
```

Then open:

`http://127.0.0.1:8080`

## License
Recommended: Apache License 2.0
