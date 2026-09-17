# VIP kickoff — any protocol

Expected skill: `vip-factory`. Expected mode: `[DV]`.

```text
Start a new VIP.

Protocol: <PROTOCOL AND SPEC VERSION>
Spec source: <ATTACH SPEC OR NAME THE DOCUMENT>
Target tier: <L0-L5>
Deadline / priority: <IF ANY>

Run Gate 0 only. Do not write RTL-facing code yet. Return:
1. Scope statement: what this VIP will and will not cover at the target tier.
2. Whether a methodology module exists for this protocol. If not, follow the spec-derivation
   procedure rather than declining.
3. The FR-### list derived from the spec, each citing a spec section.
4. The proposed directory layout and the /areas/vip-<protocol>.md memory file contents.
5. GAP-### rows for everything the spec does not pin down.

End with the STATUS / EVIDENCE / NEXT block. STATUS must be NOT_VERIFIED at Gate 0.
```

## Why it is shaped this way

Gate 0 is scoping, and letting the model jump to code is how a VIP acquires untraceable features.
The protocol is an input, never a gate — the factory covers the whole portfolio, so the prompt asks
it to derive from the spec when no module exists instead of reporting the protocol as unsupported.
