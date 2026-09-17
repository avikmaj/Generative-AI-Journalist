# Module 12 — High-Speed Interfaces
## PCIe · CXL · UCIe · DDR/LPDDR/HBM · USB · Ethernet

---

## 12.1 PCIe Verification

```
PCIe layers (verify all):
Physical Layer  → link training, LTSSM, equalization
Data Link Layer → DLLP, ACK/NAK, flow control credits
Transaction Layer → TLP types, ordering, completion timeout

LTSSM states to cover:
Detect → Polling → Configuration → Recovery → L0 → L0s → L1 → L2/L3

TLP types to cover:
MRd  — Memory Read
MWr  — Memory Write
CplD — Completion with Data
Msg  — Message (INTx, PME, error)
AtomicOp — Fetch/Swap/CAS

Corner cases:
- Completion timeout (no response)
- Malformed TLP
- Poisoned TLP
- Unexpected completion
- Flow control credit exhaustion
- Link recovery during traffic
```

## 12.2 DDR5 Verification

```
DDR5 key verification areas:
- Initialization sequence: ZQ calibration, MRS programming
- Read/Write latency: CL, CWL, tRCD, tRAS, tRP
- Burst types: BL8, BC4
- Refresh: tREFI, tRFC, per-bank refresh (PBR)
- Power modes: self-refresh, power-down
- ECC: SECDED, symbol-correct
- On-die ECC: transparent to controller
- Write leveling, read training, command/address training

Coverage model:
- All command types: ACT, RD, WR, REF, PRE, MRS, ZQC
- Bank/bankgroup combinations
- Interleaved bank access
- Refresh during access
- Power-mode transitions
```

## 12.3 USB 3.x Verification

```
USB SuperSpeed (USB 3.x) layers:
Physical layer  → LFPS, SS.Inactive, Polling, U0-U3
Link layer      → Header packets, Link Management Packets
Protocol layer  → Transaction Packets (TP), Data Packets (DP)
USB 2.0 layer   → Backward compatibility (separate D+/D-)

Transaction types:
SETUP, IN, OUT, STATUS, ISOC, INTERRUPT, BULK

Key corner cases:
- SETUP transaction: always ACK required
- SuperSpeed U1/U2 entry/exit
- Link recovery
- Endpoint stall and clear
- Zero-length packet (ZLP)
- Short packet termination
```
