# Local Unity Environment

Last checked: 2026-06-16 on Windows.

## Installed Editors

- Unity Editor: `D:\Unity\Editor\2022.3.62f3c1\Editor\Unity.exe`
- Product version: `2022.3.62f3c1_1623fc0bbb97`
- File version: `2022.3.62.1451004`
- Unity Hub: `D:\Unity\Unity Hub\Unity Hub.exe`
- Unity Hub version: `3.16.4`

The Unity executable is not on PATH in this environment. Use the full path above or discover it from the Windows uninstall registry.

## Installed Build Modules

Detected under `Editor\Data\PlaybackEngines`:

- `windowsstandalonesupport`

Assume Android, iOS, WebGL, dedicated server, and console modules are unavailable unless a later check finds them.

## Current Workspace Check

The current workspace `D:\心之彼端` was not a Unity project when checked:

- No `ProjectSettings/ProjectVersion.txt`
- No `Packages/manifest.json`
- No `Assets/`

For this workspace, generate portable Unity demo packages under `prototypes/[slug]/UnityDemo/` unless a Unity project is later added or selected.

## CLI Notes

- Registry and file metadata confirm the Editor version.
- `Unity.exe -version` exited successfully but did not print a console version in this environment.
- Only claim CLI or Play Mode verification when a real Unity project exists and the command was actually run against it.
