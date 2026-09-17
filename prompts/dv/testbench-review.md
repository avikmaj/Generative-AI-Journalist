# Testbench architecture review

Expected skill: `dv-engineering-suite`. Expected mode: `[DV]`.

```text
Review this testbench for structural and methodology problems.

Code: <PASTE OR ATTACH>
UVM version assumed: <VERSION>
Simulator: <SIMULATOR AND VERSION>

Report as:
- Blocking findings: correctness or methodology violations that will produce wrong results.
- Non-blocking findings: maintainability, reuse, naming.
- For each finding: the file/line, why it is wrong, and the corrected code.
Close with an Engineering VERDICT.

Check specifically: config DB get/set symmetry and null returns, factory registration and override
scope, phase objections raised and dropped on every path, uvm_fatal on randomize failure, m_ prefix
and _h suffix conventions, SVA default clocking and a cover for every assert, and any sequence that
drives signals directly instead of through the driver.
```

## Why it is shaped this way

Naming the simulator and UVM version up front stops the model recalling a version-specific behaviour
as universal. The explicit checklist is the set of failures that silently produce green regressions.
