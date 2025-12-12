import time
import argparse
import subprocess
import os
import aoc_day12 as m


def detect_cpu_cores() -> dict:
    """Retourne un dict avec hw.physicalcpu et hw.logicalcpu (int)."""
    info = {'physical': None, 'logical': None}
    try:
        p = subprocess.run(['sysctl', '-n', 'hw.physicalcpu'], capture_output=True, text=True)
        if p.returncode == 0:
            info['physical'] = int(p.stdout.strip())
    except Exception:
        pass
    try:
        p = subprocess.run(['sysctl', '-n', 'hw.logicalcpu'], capture_output=True, text=True)
        if p.returncode == 0:
            info['logical'] = int(p.stdout.strip())
    except Exception:
        pass
    # fallback to os.cpu_count
    if info['logical'] is None:
        info['logical'] = os.cpu_count() or 1
    if info['physical'] is None:
        # approximate physical as logical//2 if hyperthreading likely
        info['physical'] = max(1, info['logical'] // 2)
    return info


def choose_workers(mode: str, requested: int | None) -> int:
    """Calcule le nombre de workers à utiliser selon le mode ou valeur demandée.

    mode:
      - 'auto' : logical - 1 (laisse un coeur libre) mais au moins 1
      - 'physical' : physical cores
      - 'logical' : logical cores
      - 'half' : max(1, logical // 2)
      - 'none' or 0 : returns 1 (séquentiel)
    requested explicit (int) overrides mode if > 0.
    """
    cores = detect_cpu_cores()
    logical = cores['logical']
    physical = cores['physical']
    if requested is not None and requested > 0:
        return int(requested)
    if mode == 'physical':
        return max(1, int(physical))
    if mode == 'logical':
        return max(1, int(logical))
    if mode == 'half':
        return max(1, int(max(1, logical // 2)))
    # auto
    # choose logical - 1 to leave interactive core, but at least 1
    return max(1, logical - 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run day12 example with worker selection')
    parser.add_argument('--workers', '-w', type=int, default=None,
                        help='Number of workers to use (overrides --mode). Use 1 for sequential.')
    parser.add_argument('--mode', choices=['auto', 'physical', 'logical', 'half'], default='auto',
                        help="Worker selection mode if --workers not provided: auto=logical-1, physical=physical cores, logical=logical cores, half=logical//2")
    parser.add_argument('--input', '-i', default='input.txt', help='Input file to use (relative to this script)')
    args = parser.parse_args()

    shapes, grids = m.process_file(args.input)

    cores = detect_cpu_cores()
    print(f"Detected CPU: physical={cores['physical']} cores, logical={cores['logical']} threads")
    workers = choose_workers(args.mode, args.workers)
    print(f"Using workers={workers} (mode={args.mode}, requested={args.workers})")

    print('--- sequential run (workers=1) ---')
    t0 = time.time()
    res1 = m.part_1(shapes, grids, workers=1)
    t1 = time.time()
    print('result seq', res1, 'time', t1 - t0)

    print('\n--- parallel run (workers={} ) ---'.format(workers))
    t0 = time.time()
    res2 = m.part_1(shapes, grids, workers=workers)
    t1 = time.time()
    print('result par', res2, 'time', t1 - t0)
