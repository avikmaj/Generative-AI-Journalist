# Module 21 — SoC and Subsystem Verification
## Full-Chip Strategy · SW Co-Simulation · Performance · Power

---

## 21.1 Verification Hierarchy

```
IP Block Verification   (UVM env per IP)
        ↓
Subsystem Verification  (cluster of IPs — CPU+NoC+DDR)
        ↓
SoC Verification        (full chip — all subsystems)
        ↓
System Verification     (SoC + board + software)

Key principle: verify correctness at the lowest level possible.
SoC regression validates integration, not re-verifies IP behavior.
```

## 21.2 VIP Promotion Strategy

```
IP-level VIP (fully active):
  Master + Monitor + Sequencer + Scoreboard + Coverage

Subsystem-level promotion:
  IP's own VIP becomes passive (monitor only)
  Adjacent IPs use active VIPs
  Subsystem scoreboard replaces IP scoreboard

SoC-level promotion:
  Most VIPs passive — monitoring only
  Traffic generators replace individual sequencers
  SW co-simulation replaces directed test sequences
  Performance measurement scoreboard added
```

## 21.3 Software Co-Verification

```
HW/SW co-verification approaches:
1. Instruction Set Simulator (ISS) + TB
   - ISS drives CPU behavior
   - TB monitors memory/peripheral side
   - Cycle-accurate or approximate

2. Bare-metal firmware + UVM TB
   - Real firmware runs on simulated CPU
   - UVM TB provides peripheral responses
   - Interrupt handlers verified

3. RTOS + driver stack + UVM TB
   - OS scheduler, driver, HW TB
   - Closest to real deployment scenario
   - Slowest simulation speed

Coverage in HW/SW co-sim:
- SW: code coverage of firmware (gcov)
- HW: functional + code coverage of RTL
- Transaction-level: protocol coverage at all interfaces
```

## 21.4 SoC Performance Verification

```
Performance targets (from architecture spec):
- Memory bandwidth: GB/s per master
- Read/write latency: average and worst-case
- NoC throughput: transactions/second
- DMA throughput: MB/s at each channel

Performance test methodology:
1. Traffic generator: max-rate stimulus per master
2. Performance scoreboard: timestamp at request and response
3. Measurement: compute bandwidth and latency statistics
4. Compare against architecture targets
5. Cover: light load / medium load / saturation / mixed

Performance regression:
- Run nightly: flag regressions vs baseline
- Alert if p99 latency degrades >5%
- Alert if peak bandwidth degrades >2%
```

## 21.5 Full-Chip Regression Strategy

```
Regression tiers:

Tier 1 — Sanity (every commit, ~1 hour):
  - 10–20 tests covering all major functions
  - Single seed per test
  - Gate: must pass before merge

Tier 2 — Nightly (~8 hours):
  - 500–2000 tests
  - 10–20 seeds per test
  - Coverage merge + trend report
  - Gate: pass rate ≥99%, coverage trending up

Tier 3 — Weekly (~24–48 hours):
  - 5000–20000 tests
  - 50+ seeds per test
  - Full coverage merge
  - Gate: coverage targets for milestone

Tier 4 — Pre-signoff (one-time, 72+ hours):
  - Maximum seed count
  - All corner tests
  - Gate: all signoff criteria met
```
