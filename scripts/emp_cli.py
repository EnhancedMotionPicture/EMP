#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate(data):
    errors = []
    for key in ["version", "project", "media", "tracks"]:
        if key not in data:
            errors.append(f"Missing top-level key: {key}")
    if "tracks" in data and not isinstance(data["tracks"], list):
        errors.append("tracks must be a list")
    for i, track in enumerate(data.get("tracks", [])):
        for key in ["id", "type", "target", "events"]:
            if key not in track:
                errors.append(f"Track {i} missing key: {key}")
        for j, event in enumerate(track.get("events", [])):
            for key in ["t_ms", "dur_ms", "intensity", "shape"]:
                if key not in event:
                    errors.append(f"Track {i} event {j} missing key: {key}")
    return errors

def cmd_validate(path):
    data = load(path)
    errors = validate(data)
    if errors:
        print("INVALID")
        for e in errors:
            print("-", e)
        sys.exit(1)
    print("VALID")

def cmd_inspect(path):
    data = load(path)
    print("Title:", data.get("project", {}).get("title"))
    print("Media:", data.get("media", {}).get("src"))
    print("Tracks:", len(data.get("tracks", [])))
    for track in data.get("tracks", []):
        print(f"- {track['id']} [{track['type']}] -> {track['target']} ({len(track['events'])} events)")

def cmd_simulate(path):
    data = load(path)
    items = []
    for track in data.get("tracks", []):
        for ev in track.get("events", []):
            items.append((ev["t_ms"], track["type"], track["target"], ev["shape"], ev["intensity"], ev["dur_ms"]))
    items.sort(key=lambda x: x[0])
    for t_ms, typ, target, shape, intensity, dur_ms in items:
        print(f"{t_ms:>6}ms  {typ:<6}  {target:<14}  {shape:<8}  intensity={intensity:.2f} dur={dur_ms}ms")

def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/emp_cli.py [validate|inspect|simulate] <file>")
        sys.exit(2)
    command, path = sys.argv[1], sys.argv[2]
    if command == "validate":
        cmd_validate(path)
    elif command == "inspect":
        cmd_inspect(path)
    elif command == "simulate":
        cmd_simulate(path)
    else:
        print("Unknown command:", command)
        sys.exit(2)

if __name__ == "__main__":
    main()
