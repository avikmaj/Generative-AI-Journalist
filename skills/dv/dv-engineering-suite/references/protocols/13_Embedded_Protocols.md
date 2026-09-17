# Module 13 — Embedded Protocols
## SPI · I2C · I3C · UART · CAN · JTAG · MIPI

---

## 13.1 SPI Verification

```
SPI modes (CPOL/CPHA): 0/0, 0/1, 1/0, 1/1
Verify all four mode combinations.

Key checks:
- CS# assertion to first SCK edge timing (tCSS)
- Last SCK edge to CS# de-assertion (tCSH)
- SCK frequency vs spec
- MOSI setup/hold relative to SCK
- MISO capture timing
- Full-duplex simultaneous TX/RX
- Multi-slave CS# routing

Coverage: all 4 modes × byte values × burst lengths
```

## 13.2 I2C Verification

```
I2C transaction phases: START, ADDRESS+R/W, ACK, DATA, ACK, STOP

Key checks:
- START condition: SDA falls while SCL HIGH
- STOP condition: SDA rises while SCL HIGH
- Address ACK/NAK (7-bit and 10-bit)
- Clock stretching (slave holds SCL low)
- Repeated START (no STOP between transactions)
- Arbitration (multi-master)
- Bus timeout on SCL stuck low

Speeds: Standard (100kHz), Fast (400kHz), Fast+ (1MHz), High-speed (3.4MHz)
```

## 13.3 JTAG / RISC-V Debug

```
JTAG TAP states: Reset → Idle → DR/IR scan chain

Key checks:
- TAP state machine transitions (all 16 states)
- Instruction register (IR) encoding
- Boundary scan: BYPASS, EXTEST, PRELOAD, SAMPLE
- RISC-V Debug: DMI access via JTAG DTM
- Halt/resume processor via DM
- Register access (GPR, CSR) via abstract commands
- System bus access (SBA)

Coverage: all IR codes × DR lengths × bypass chain depth
```
