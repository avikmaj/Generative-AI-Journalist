# VIP Portfolio — full coverage scope

The factory is **protocol-agnostic**. There is no approved-VIP list and no supported-protocol
restriction. Any protocol below, any protocol not below, and any customer-proprietary interface is in
scope. The lifecycle (Gates 0–11), the regression tiers (L0–L5), the PASS authority policy and the
skeleton are identical for every one of them.

Use this catalogue to size a request, name a VIP directory, and decide which methodology module
carries the protocol depth. Do **not** treat it as a limit.

> Version and generation labels below are as supplied in the portfolio matrix for this factory. Do
> not quote a specific revision, feature or clause of any standard from memory — read the spec, or
> label it `UNVERIFIED`.

## USB

USB4 v2 · USB 4.0 · UAS · USB 4/3/2 HUB · Retimer 4.0/3.2 · 128b/132b · USB 3.2/3.1/3.0 · USB 2.0 ·
USB2 OTG · eUSB2 v1 · eUSB2 v2 · USB PD v3.1 · Type-C v1.3 · xHCI

## Bus / interface / chiplet

UCIe 3.0 · UCIe 2.0 · UCIe with Retimer · BoW · CPRI/eCPRI · JESD204D/C/B · SMBus v3.3.1/3.2 ·
xSPI · AVSBus v2.1/2.0/1.4.1 · SPI/QSPI/OSPI · RTC · PMBus v1.5/1.4 · I2C/I2S/LPC · UART/USART

## MIPI

A-PHY/PAL · MASS · SPMI · I3C v1.2/1.1.1 · CSI-2 v4.0.1 · SWI3S v1.0 · DSI v2.2 · DSI v1.3.2 ·
C-PHY v3.1/2.1 · D-PHY v3.5 · M-PHY v6/5 · UniPro v3/2

## Automotive

Automotive Ethernet · TSN · TSN queueing and forwarding · Qbv · PTP/gPTP · MACsec ·
preemption/PFC · ASA · FlexRay · CAN / CAN FD · CAN XL · CXPI · SENT/LIN

## Memory

DDR6 · DDR5/4/3 · LPDDR6 · LPDDR5/5x · LPDDR4x/4/3 · HBM4 · HBM3E/3/2 · DFI 6.0 ·
DDR5 RDIMM · DDR5 LRDIMM · DDR5 MRDIMM2 · HMC · GDDR6 · GDDR7

## Networking

Ultra Ethernet (UEC) · TCP · 1600G · 800G · 400G/200G · 100G/40G · 50G/25G · 10G/5G · 1G/2.5G ·
1G BASE-T · 100M · 10M · IPsec · Interlaken v1.2

## SoC / avionics / peripheral

PWM · WDT · PIT · GPIO · SGPIO · NFC ISO 14443 · Smart Card ISO 7816 · SpaceWire · ARINC429 ·
ARINC708A · SMPTE SDI · MIL-STD-1553

## PCIe / CXL

PCIe 7 · Gen 6 · Gen 5/4 · Gen 3/2 · CXL 4.0/3.2/3/2 · CXL Switch · PCIe Switch · PIPE 6/5 ·
SR-IOV · ATS

## Storage

NVMe 2.3/2.2 · NVMe 2.0/1.4 · UFS 5/4/3.1 · UHS 3/2/1 · SD Express / SD 9.1 · ONFI 6/5.2 ·
SDUC/SDXC · SDIO/SDHC · SATA 3.3 · eMMC v5.1a · eMMC 5.1/A/B

## AMBA

CHI 5 · AXI 5 / 5-Lite · AXI4 / 4-Lite / 3 · AMBA AXI3 · ACE 4 / 4-Lite · AXI-Stream 5/4 ·
AHB 5 / 3-Lite · AMBA AHB 3-Lite · APB 5/4/3 · ATB 5/4/3 · CXS a/b · CXS c/d/Lite · SWD

## Display

DP 2.1 · DP 2.0/1.4 · DP AE 1.0 · eDP 2.0 · eDP 1.5/1.4b · HDMI 2.1/2.0/1.4 · HDCP 2.4/2.3/1.4 ·
LVDS · LTTPR/MST · V-by-One

## RISC-V and others

UAL · TileLink · RI5CY · FPU · JTAG / cJTAG · PLIC · 8b/10b · 64b/66b · NoC VIP

## Protocol depth routing

The catalogue above says *what* is in scope. Protocol technique lives in the methodology suite:

| Protocol group | Methodology module |
|---|---|
| AMBA — AXI, AHB, APB, CHI, ACE, AXI-Stream, ATB, CXS | `11_AMBA_Protocols.md` |
| High-speed serial and memory — PCIe, CXL, UCIe, DDR/LPDDR/HBM, USB, Ethernet, display, storage | `12_High_Speed_Interfaces.md` |
| Embedded and low-speed — SPI/QSPI, I2C/I3C, UART, CAN/CAN FD/CAN XL, LIN, SENT, JTAG, SPMI, GPIO, PWM, WDT | `13_Embedded_Protocols.md` |
| NoC and interconnect — NoC VIP, TileLink, coherent fabric | `14_NoC_Verification.md` |
| Anything else — avionics, MIPI, automotive TSN, RISC-V, proprietary | No module exists yet |

## When no methodology module covers the protocol

This is the normal case for most of this portfolio, not an exception.

1. **Demand the specification document first.** Never generate a VIP for a protocol from memory of
   the standard.
2. Extract the requirement list from the spec into `FR-###` entries in the testplan.
3. Derive from those requirements: the transaction fields, the legal-space constraints, the
   coverpoints (all encodings, boundaries, legal combinations, `illegal_bins`), the crosses, and the
   protocol invariants that become SVA.
4. Anything in the spec you cannot map is a `GAP-###` and blocks the relevant gate.
5. If the protocol recurs, promote the extracted knowledge into a new methodology module rather than
   re-deriving it per VIP.

Naming: the VIP directory is the lower-case protocol token — `vip/axi4/`, `vip/pcie6/`,
`vip/lpddr5/`, `vip/canxl/`, `vip/csi2/` — and its memory file is `/areas/vip-<token>.md`.
