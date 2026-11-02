from contract import ComputeOutput


def input_problem(v):
    if v.sets <= 0 or v.block_size <= 0 or v.ways <= 0:
        return "cache dimensions must be positive"
    if v.sets & (v.sets - 1) or v.block_size & (v.block_size - 1) or any(a < 0 for a in v.addresses):
        return "power-of-two dimensions and nonnegative addresses required"
    return None


def expected(v):
    rows = [[-1 for _ in range(v.ways)] for _ in range(v.sets)]
    queues = [[] for _ in range(v.sets)]
    hits, victims = [], []
    for address in v.addresses:
        block = address // v.block_size
        s = block % v.sets
        hit = block in rows[s]
        victim = -1
        if hit:
            slot = rows[s].index(block)
            if v.policy.value == "lru":
                queues[s].remove(slot)
                queues[s].append(slot)
        else:
            slot = rows[s].index(-1) if -1 in rows[s] else queues[s].pop(0)
            victim = rows[s][slot]
            rows[s][slot] = block
            queues[s].append(slot)
        hits.append(hit)
        victims.append(victim)
    return ComputeOutput(hits, victims, rows, hits.count(True), hits.count(False))
