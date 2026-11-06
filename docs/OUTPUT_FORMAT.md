# Output format

JSON output contains three top-level keys:

- `metadata`: caller-supplied configuration metadata.
- `metrics`: summary values for the trajectory.
- `events`: event records with time, altitude, speed, mass, and details.
- `samples`: time histories for the state and principal loads.

CSV output is row-oriented. Each row contains time, position, velocity,
vehicle mass, thrust, drag, dynamic pressure, Mach number, stage index, and
an optional event label. JSON is intended for preserving structured results;
CSV is convenient for spreadsheets and external plotting programs.

All values use SI units. Time is seconds, position is metres, velocity is
metres per second, mass is kilograms, force is newtons, and dynamic pressure
is pascals.
