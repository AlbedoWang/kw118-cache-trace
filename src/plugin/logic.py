from contract import ComputeOutput


def compute(v, workspace):
    if (
        v.sets < 1
        or v.sets & (v.sets - 1)
        or v.ways < 1
        or v.block_size < 1
        or v.block_size & (v.block_size - 1)
        or any(a < 0 for a in v.addresses)
    ):
        raise ValueError("invalid cache dimensions or address")
    lines = [[-1] * v.ways for _ in range(v.sets)]
    ages = [[-1] * v.ways for _ in range(v.sets)]
    hits, evicted = [], []
    for time, address in enumerate(v.addresses):
        block = address // v.block_size
        s = block % v.sets
        hit = block in lines[s]
        old = -1
        if hit:
            i = lines[s].index(block)
        else:
            i = lines[s].index(-1) if -1 in lines[s] else min(range(v.ways), key=lambda j: ages[s][j])
            old, lines[s][i] = lines[s][i], block
        if not hit or v.policy.value == "lru":
            ages[s][i] = time
        hits.append(hit)
        evicted.append(old)
    return ComputeOutput(hits, evicted, lines, sum(hits), len(hits) - sum(hits))
