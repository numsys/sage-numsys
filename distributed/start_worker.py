from distributed.helpers.worker_handling import run_work, start_processor
from distributed.workers.basic import calculate_basics
from distributed.workers.eigenvalues import calculate_eigenvalues
from distributed.workers.multiplications import generate_multiplications
from distributed.workers.optimize import optimizing
from distributed.workers.signature import calculate_signature
from sage.all import *

if len(sys.argv) == 1:
    print("Need a parameter: basic_calculations")
elif sys.argv[1] == "basic_calculations":
    start_processor(calculate_basics, "basic_calculations", {".dimension": "null"})
elif sys.argv[1] == "signature":
    start_processor(calculate_signature, "progress_signature",
                    {".signature": "null", ".optimized": "0", ".volume": "<1000000"})
elif sys.argv[1] == "optimize":
    start_processor(optimizing, "progress_optimizing",
                    {".optimizedFromWith": "complex", "has_similar_radix_system": 0, ".optimized": "null"})
elif sys.argv[1] == "eigenvalues":
    start_processor(calculate_eigenvalues, "progress_eigenvalues", {".eigenvalueMin": "null"})
elif sys.argv[1] == "generateMultiplications":
    run_work(generate_multiplications, data={".dimension": "2", "group": "<>multiplication"})
else:
    print("Unknown Command")
