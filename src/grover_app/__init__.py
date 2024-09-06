from math import pi, sqrt
import cmath
from ket import *
from ket.lib import phase_oracle


def grover(n, oracle, m=1):
    p = Process()
    qubits = p.alloc(n)
    H(qubits)
    d = [dump(qubits)]
    for _ in range(int((pi / 4) * sqrt(2**n / m))):
        oracle(qubits)
        with around(cat(H, X), qubits):
            ctrl(qubits[1:], Z)(qubits[0])
        d.append(dump(qubits))
    return d


def grover_df(num_qubits, search_for):
    dump_states = grover(num_qubits, phase_oracle(search_for))
    prob_all = {
        "Estado": [s for d in dump_states for s, _ in sorted(d.get().items())],
        "Probabilidade (%)": [
            abs(p) ** 2 * 100 for d in dump_states for _, p in sorted(d.get().items())
        ],
        "Passo": [i for i, d in enumerate(dump_states) for _ in range(len(d.get()))],
    }

    prob_right = {
        "Estado": ["Procurado", "Outros"] * len(dump_states),
        "Probabilidade (%)": [
            p * 100
            for d in dump_states
            for p in [
                abs(d.get()[search_for]) ** 2,
                1 - abs(d.get()[search_for]) ** 2,
            ]
        ],
        "Passo": [i for i in range(len(dump_states)) for _ in range(2)],
    }

    return prob_all, prob_right


def grover_step_by_step(n, oracle, m=1):
    p = Process()
    qubits = p.alloc(n)
    d = [dump(qubits)]
    for q in qubits:
        H(q)
        d.append(dump(qubits))
    for _ in range(int((pi / 4) * sqrt(2**n / m))):
        oracle(qubits)
        d.append(dump(qubits))
        for q in qubits:
            H(q)
            d.append(dump(qubits))
        for q in qubits:
            X(q)
            d.append(dump(qubits))

        ctrl(qubits[1:], Z)(qubits[0])
        d.append(dump(qubits))

        for q in qubits:
            X(q)
            d.append(dump(qubits))
        for q in qubits:
            H(q)
            d.append(dump(qubits))
    return d


def grover_step_by_step_df(num_qubits, search_for):
    dump_states_step_by_step = grover_step_by_step(num_qubits, phase_oracle(search_for))
    return {
        "Estado": [s for _ in dump_states_step_by_step for s in range(1 << num_qubits)],
        "Probabilidade": [
            abs(d.get()[s]) if s in d.get() else 0.0
            for d in dump_states_step_by_step
            for s in range(1 << num_qubits)
        ],
        "Operação": [
            i
            for i, _ in enumerate(dump_states_step_by_step)
            for _ in range(1 << num_qubits)
        ],
        "Fase": [
            cmath.phase(complex(d.get()[s])) if s in d.get() else 0.0
            for d in dump_states_step_by_step
            for s in range(1 << num_qubits)
        ],
    }


# def grover_step_by_step_df(num_qubits, search_for):
#     dump_states_step_by_step = grover_step_by_step(num_qubits, phase_oracle(search_for))
#     return [
#         {
#             "Estado": [s for s in range(1 << num_qubits)],
#             "Probabilidade (%)": [
#                 abs(d.get()[s]) if s in d.get() else 0.0
#                 for s in range(1 << num_qubits)
#             ],
#             "Passo": [i for _ in range(1 << num_qubits)],
#             "Fase": [
#                 cmath.phase(complex(d.get()[s]))
#                 if s in d.get()
#                 else 0.0
#                 for s in range(1 << num_qubits)
#             ],
#         }
#         for i, d in enumerate(dump_states_step_by_step)
#     ]
