# kw118-cache-trace

An original COMP 480/580 verifiable systems task by Kaijian Wang (kw118).

## Tools

| Tool/task | Behavior |
|---|---|
| `replay_cache` | Compute the exact typed domain result. |
| `save_result` | Accept a ComputeOutput as result; write result.json and return path plus result. |
| `cache-trace` | Agent task: compute, save, then submit the saved output unchanged. |

### Rules and output semantics

Addresses are nonnegative byte addresses. Sets and block_size are positive powers of two; ways is positive. Start empty. Block = address // block_size; set = block % sets. Fill the lowest numbered empty way. FIFO hits do not change insertion order; LRU hits update recency. Victim is the oldest insertion/access respectively. Output hits and evicted are aligned with input accesses; evicted=-1 means no eviction. lines contains block numbers in physical way order, -1 for empty. hit_count and miss_count count accesses. No writes or timing model.

The input/output field shapes and Enum values are declared in contract.py. Invalid semantic inputs raise ValueError (except malformed packet contents, which the inspection task reports explicitly). No model is used to judge results. The verifier independently recomputes the expected answer, compares every result field, and reads the actual result.json. A matching declaration alone is insufficient. Acceptance is binary; the framework score is 1 for valid and 0 for invalid.

### Example task input

```json
{
  "addresses": [
    0,
    1,
    4,
    0,
    8,
    4
  ],
  "sets": 1,
  "ways": 2,
  "block_size": 4,
  "policy": "lru"
}
```

In RUSH Lab, request the `cache-trace` task with this structured input. The agent calls `replay_cache`, passes its complete output to save_result, and submits the saved output. A model and RUSH Lab access are needed for this step; pytest does not establish agent success.

## Layout

- contract.py: typed tools, task and outputs.
- src/plugin/: MCP server, computation and file saving.
- verifier/: independent deterministic oracle and artifact checks.
- tests/: public pedagogical task inputs and regression checks, not experiment logs.
- ui/ and product/: schema-based result display and marketplace metadata.

## Develop and run

Requires Git, uv and Python 3.12+. From this repository:

```sh
uv sync --frozen --extra dev --no-editable
uv run --frozen --no-editable pytest -q
uv run --frozen --no-editable ruff check .
uv lock --check
```

Normal (non-editable) installation is intentional: it also checks packaged source imports. After editing source, rerun uv sync with --reinstall-package nanoagent-kw118-cache-trace. Do not copy another project's virtual environment.

The manifest's runtime remains the official `[uv, run, --frozen, python, -m, plugin]`. The host supplies NANOAGENT_WORKSPACE. No API keys or plugin network hosts are needed. All writes stay in the workspace. Existing symlink destinations are rejected. Runtime files, logs and the milestone report belong outside this repository.

### Validation and limitations

Tests cover the domain boundaries, wrong results, missing/malformed artifacts, schema failures and symlink protection. Fixtures are intentionally small public teaching inputs representing the actual task contract, not hardware performance samples. Tools and oracle use separate implementations. Local correctness does not establish marketplace installation or model behavior; those require recorded real platform runs.
