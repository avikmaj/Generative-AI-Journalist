# Module 19 — Regression Automation
## Farm · Jenkins/LSF · Seed Management · CI/CD · Python · Reporting

---

## 19.1 Regression Infrastructure Architecture

```
Git/Perforce commit
      ↓
CI Trigger (Jenkins/GitLab CI/GitHub Actions)
      ↓
Build Stage: compile + elaborate
      ↓
Regression Dispatch: farm job submission (LSF/Slurm)
      ↓
Parallel Simulation: N jobs × M seeds
      ↓
Log Collection + Pass/Fail
      ↓
Coverage Merge (URG/IMC)
      ↓
Failure Clustering (Agent 6)
      ↓
Dashboard Update (Agent 11)
      ↓
Notification (email/Slack/Jira)
```

---

## 19.2 Regression Configuration Schema

```yaml
# regression_config.yaml
regression:
  name: <regression_name>
  dut: <dut_name>
  rtl_version: <tag>
  simulator: VCS           # VCS | Xcelium | Questa

  compile:
    top: tb_top
    filelist: filelist.f
    flags:
      - "-cm line+cond+tgl+fsm+branch+assert"
      - "-sverilog"
      - "-ntb_opts uvm-1.2"
      - "+incdir+$UVM_HOME/src"
      - "-debug_acc+pp+dmptf"
    output: simv

  tests:
    - test: axi_write_base_test
      weight: 10
      seeds: random
      num_seeds: 20
      timeout_min: 30
      plusargs: ["+UVM_VERBOSITY=UVM_MEDIUM"]

    - test: axi_wrap_255_test
      weight: 5
      seeds: [1, 2, 3, 42, 137]
      timeout_min: 60
      plusargs: ["+UVM_VERBOSITY=UVM_HIGH"]

    - test: axi_backpressure_test
      weight: 8
      seeds: random
      num_seeds: 15
      timeout_min: 45

  farm:
    backend: LSF             # LSF | Slurm | local
    queue: dv_normal
    parallel_jobs: 100
    memory_mb: 4096
    retry_on_timeout: true
    max_retries: 2
    retry_on_crash: true

  coverage:
    enabled: true
    merge_dir: ./coverage_db
    report_dir: ./urg_report
    targets:
      functional_pct: 95
      code_stmt_pct:  90

  notification:
    on_complete: true
    on_failure: true
    channels: [email, slack]
    jira_create_on_new_cluster: true
```

---

## 19.3 LSF Job Management

```bash
# Submit single simulation job
bsub -q dv_normal \
     -n 4 \
     -R "rusage[mem=4096]" \
     -J "axi_test_seed42" \
     -o logs/axi_test_seed42.log \
     "./simv +UVM_TESTNAME=axi_write_base_test \
             +ntb_random_seed=42 \
             +UVM_VERBOSITY=UVM_MEDIUM \
             -cm_dir coverage_db/seed42"

# Submit regression array (100 parallel jobs)
bsub -q dv_normal \
     -n 4 \
     -R "rusage[mem=4096]" \
     -J "regression[1-100]" \
     -o logs/reg_%I.log \
     "run_single_test.sh \$LSB_JOBINDEX"

# Monitor jobs
bjobs -J "regression*"

# Kill all regression jobs
bkill -J "regression*"

# Check job completion
bhist -l -J "regression[1-100]" | grep "DONE\|EXIT" | wc -l
```

---

## 19.4 Python Regression Manager

```python
#!/usr/bin/env python3
"""
DV Regression Manager
Grounded in DV Engineering Bible Vol I — Chapter 37
"""

import subprocess
import yaml
import os
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

class RegressionManager:
    """Manages full regression lifecycle: submit → monitor → collect → report"""

    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.cfg = yaml.safe_load(f)['regression']
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = []

    def compile(self) -> bool:
        """Compile and elaborate the testbench"""
        cmd = ['vcs'] + self.cfg['compile']['flags'] + \
              [f'-f {self.cfg["compile"]["filelist"]}',
               f'-o {self.cfg["compile"]["output"]}']
        print(f"[COMPILE] Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[COMPILE FAILED]\n{result.stderr}")
            return False
        print("[COMPILE] SUCCESS")
        return True

    def generate_jobs(self) -> list:
        """Generate list of (test, seed) job tuples"""
        jobs = []
        for test_cfg in self.cfg['tests']:
            test_name = test_cfg['test']
            if test_cfg['seeds'] == 'random':
                seeds = [random.randint(1, 2**31) for _ in range(test_cfg['num_seeds'])]
            else:
                seeds = test_cfg['seeds']
            for seed in seeds:
                jobs.append({
                    'test': test_name,
                    'seed': seed,
                    'timeout': test_cfg.get('timeout_min', 30),
                    'plusargs': test_cfg.get('plusargs', [])
                })
        return jobs

    def run_job(self, job: dict) -> dict:
        """Run a single simulation job"""
        test, seed = job['test'], job['seed']
        log_path = Path(f"logs/{test}_seed{seed}.log")
        log_path.parent.mkdir(exist_ok=True)
        cov_dir  = f"coverage_db/{test}_seed{seed}"

        cmd = [
            f"./{self.cfg['compile']['output']}",
            f"+UVM_TESTNAME={test}",
            f"+ntb_random_seed={seed}",
            f"-cm_dir {cov_dir}",
        ] + job['plusargs']

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=job['timeout'] * 60
            )
            log_path.write_text(result.stdout + result.stderr)
            passed = self._check_pass(result.stdout + result.stderr)
            return {'test': test, 'seed': seed, 'status': 'PASS' if passed else 'FAIL',
                    'log': str(log_path), 'cov_dir': cov_dir}
        except subprocess.TimeoutExpired:
            return {'test': test, 'seed': seed, 'status': 'TIMEOUT',
                    'log': str(log_path), 'cov_dir': None}

    def _check_pass(self, log: str) -> bool:
        """Canonical pass check: no UVM_FATAL, no UVM_ERROR (count check)"""
        if 'UVM_FATAL' in log:
            return False
        # Extract UVM error count
        for line in log.split('\n'):
            if 'UVM_ERROR' in line and 'UVM_ERROR :    0' not in line:
                if 'Report counts' in log:
                    if 'UVM_ERROR :    0' not in log:
                        return False
        return 'UVM_ERROR :    0' in log and 'UVM_FATAL :    0' in log

    def run_regression(self, max_workers: int = 20) -> dict:
        """Run full regression in parallel"""
        jobs = self.generate_jobs()
        print(f"[REGRESSION] Submitting {len(jobs)} jobs, {max_workers} parallel")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.run_job, job): job for job in jobs}
            for future in as_completed(futures):
                result = future.result()
                self.results.append(result)
                status_char = '✓' if result['status'] == 'PASS' else '✗'
                print(f"  [{status_char}] {result['test']} seed={result['seed']}: {result['status']}")

        return self._generate_report()

    def _generate_report(self) -> dict:
        total  = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        timeout = sum(1 for r in self.results if r['status'] == 'TIMEOUT')

        report = {
            'timestamp': self.timestamp,
            'total': total, 'passed': passed, 'failed': failed, 'timeout': timeout,
            'pass_pct': round(100 * passed / total, 1) if total else 0,
            'failures': [r for r in self.results if r['status'] != 'PASS']
        }
        with open(f'regression_report_{self.timestamp}.json', 'w') as f:
            json.dump(report, f, indent=2)
        self._print_summary(report)
        return report

    def _print_summary(self, report: dict):
        print(f"""
╔══════════════════════════════════════════╗
║         REGRESSION SUMMARY              ║
╠══════════════════════════════════════════╣
║  Total   : {report['total']:>6}                      ║
║  PASS    : {report['passed']:>6}  ({report['pass_pct']:>5.1f}%)            ║
║  FAIL    : {report['failed']:>6}                      ║
║  TIMEOUT : {report['timeout']:>6}                      ║
╚══════════════════════════════════════════╝
""")

if __name__ == '__main__':
    mgr = RegressionManager('regression_config.yaml')
    if mgr.compile():
        mgr.run_regression(max_workers=50)
```

---

## 19.5 CI/CD Pipeline — Jenkins

```groovy
// Jenkinsfile — DV Regression Pipeline
pipeline {
    agent { label 'dv_farm' }

    parameters {
        string(name: 'RTL_VERSION', defaultValue: 'main', description: 'RTL branch/tag')
        choice(name: 'REGRESSION_TYPE', choices: ['nightly', 'full', 'quick'], description: 'Regression tier')
        string(name: 'SEED_COUNT', defaultValue: '20', description: 'Seeds per test')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: params.RTL_VERSION, url: 'ssh://git/rtl_repo'
            }
        }

        stage('Compile') {
            steps {
                sh '''
                    vcs -sverilog -ntb_opts uvm-1.2 \
                        -cm line+cond+tgl+fsm+branch+assert \
                        -f filelist.f -o simv
                '''
            }
        }

        stage('Run Regression') {
            steps {
                sh """
                    python3 regression_manager.py \
                        --config regression_config.yaml \
                        --type ${params.REGRESSION_TYPE} \
                        --seeds ${params.SEED_COUNT}
                """
            }
        }

        stage('Coverage Merge') {
            steps {
                sh 'urg -dir coverage_db -report urg_report -format both'
                publishHTML(target: [
                    reportDir: 'urg_report',
                    reportFiles: 'dashboard.html',
                    reportName: 'Coverage Report'
                ])
            }
        }

        stage('Report') {
            steps {
                sh 'python3 generate_dashboard.py --report regression_report_*.json'
                emailext(
                    to: 'dv-team@company.com',
                    subject: "DV Regression: ${currentBuild.currentResult}",
                    body: '${FILE, path="regression_summary.txt"}'
                )
            }
        }
    }

    post {
        failure {
            sh 'python3 create_jira_ticket.py --regression regression_report_*.json'
        }
    }
}
```

---

## 19.6 Seed Management Strategy

```python
# Seed management best practices

# 1. Deterministic seeds for critical tests
CRITICAL_SEEDS = [1, 2, 3, 42, 137, 999, 12345, 98765]

# 2. Random seeds for coverage exploration
import random
RANDOM_SEEDS = [random.randint(1, 2**31-1) for _ in range(100)]

# 3. Coverage-guided seeds (target uncovered bins)
# Analyze which seeds hit specific coverage bins → prioritize those seeds
def coverage_guided_seeds(coverage_report, target_bin):
    """Find seeds that historically hit the target bin"""
    seeds_hitting_bin = []
    for run in coverage_report['runs']:
        if target_bin in run['covered_bins']:
            seeds_hitting_bin.append(run['seed'])
    return seeds_hitting_bin

# 4. Regression seed rotation
# Nightly: fixed set of 50 seeds (stable baseline)
# Weekly: 500 random seeds (exploration)
# Pre-signoff: 5000 seeds (final confidence)
```

---

## 19.7 Pass/Fail Criteria Reference

| Simulator | Pass Indicator | Fail Indicator |
|---|---|---|
| VCS | `UVM_ERROR : 0`, `UVM_FATAL : 0` | `UVM_ERROR : N>0` or `UVM_FATAL : N>0` |
| Xcelium | Same UVM report counts | Same |
| Questa | Same UVM report counts | Same |

**Never use simulation exit code alone** — a sim can exit 0 with UVM errors.
Always parse the UVM report summary line:
```
grep "UVM_ERROR\|UVM_FATAL" sim.log | grep "Report" | tail -5
```

---

## 19.8 Regression Health Metrics

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Pass rate | ≥ 99% | 95–99% | < 95% |
| Flaky rate | < 1% | 1–3% | > 3% |
| Timeout rate | < 0.5% | 0.5–2% | > 2% |
| Coverage delta/week | > +2% | +0.5–2% | < +0.5% or declining |
| New clusters/week | Decreasing | Flat | Increasing |
| Compile time | < 30min | 30–60min | > 60min |
