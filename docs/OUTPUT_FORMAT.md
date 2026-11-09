# Output format

JSON output contains four top-level keys:

- metadata: caller-supplied configuration metadata.
- wind_profile: the configured east/north/vertical wind table, or null.
- metrics: summary values for the trajectory.
- events: event records with time, altitude, speed, mass, and details.
- samples: time histories for the state and principal loads.

Each JSON sample includes downrange and vertical wind components projected
into the simulation plane and the air-relative speed. CSV output is row-
oriented and includes the same three wind telemetry values. It does not repeat
the full east/north input profile; that profile is stored in JSON.

CSV rows contain time, position, velocity, vehicle mass, thrust, drag,
dynamic pressure, Mach number, stage index, event label, wind components,
and air-relative speed. JSON is intended for preserving structured results;
CSV is convenient for spreadsheets and external plotting programs.

All values use SI units. Time is seconds, position is metres, velocity is
metres per second, mass is kilograms, force is newtons, and dynamic pressure
is pascals.
