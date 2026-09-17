# Module 14 — NoC Verification
## Traffic Matrix · Connectivity · Ordering · Deadlock · Performance

---

## 14.1 NoC Architecture Verification

```
NoC topology types:
- Crossbar: O(N²) resources, low latency, limited scale
- Ring: simple, moderate scale
- Mesh: scalable 2D, multiple paths
- Tree: hierarchical, IP-to-SoC
- Fat-tree: datacenters, load balanced
- Custom: SoC-specific hybrids

Verify per topology:
- Connectivity: every master can reach every permitted slave
- Ordering: rules (AXI ordering: same ID, same address)
- QoS: priority enforcement, bandwidth guarantees
- Deadlock: no circular dependency
- Flow control: back-pressure propagation
- Address decode: correct routing per memory map
```

## 14.2 Connectivity Coverage Matrix

```systemverilog
// N masters x M slaves — all paths must be exercised
covergroup noc_connectivity_cg;
  option.per_instance = 1;

  cp_master: coverpoint master_id {
    bins m[] = {[0:N_MASTERS-1]};
  }
  cp_slave: coverpoint slave_id {
    bins s[] = {[0:N_SLAVES-1]};
  }
  // All valid M×S combinations
  cx_connectivity: cross cp_master, cp_slave {
    // Exclude illegal paths based on memory map
    illegal_bins no_access = ...;
  }
endgroup
```

## 14.3 Deadlock Detection

```
Sufficient conditions for deadlock freedom:
1. No cyclic resource dependency
2. Flow control credit always returns
3. Response channel never filled by requests

SVA liveness property:
property p_no_deadlock;
  req_valid |-> ##[1:MAX_LATENCY] rsp_valid;
endproperty

Formal deadlock check:
- Assume: finite number of in-flight transactions
- Prove: eventually all transactions complete
- Tool: JasperGold Deadlock App
```

## 14.4 NoC Performance Verification

```
Key performance metrics:
- Latency: cycles from request to response
- Bandwidth: GB/s achievable per master/slave pair
- Throughput: transactions/second
- Fairness: no starvation under load

Performance scoreboard:
- Record timestamp at request (AR/AW)
- Record timestamp at response (R/B)
- Compute latency = rsp_time - req_time
- Track per-master, per-slave, per-QoS

Coverage:
- Latency bins: min, nominal, near-limit, timeout
- All-masters-active scenario
- Slave saturation scenario
- Mixed QoS traffic
```
