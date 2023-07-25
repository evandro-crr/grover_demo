from math import pi, sqrt
import cmath
from ket import *


def grover(n, oracle, m=1):
    qubits = quant(n)
    H(qubits)
    d = [dump(qubits)]
    for _ in range(int((pi / 4) * sqrt(2**n / m))):
        oracle(qubits)
        with around([H, X], qubits):
            ctrl(qubits[1:], Z, qubits[0])
        d.append(dump(qubits))
    return d


def grover_df(num_qubits, search_for):
    dump_states = grover(num_qubits, phase_on(search_for))
    prob_all = {
        "Estado": [
            s for d in dump_states for s, _ in sorted(d.get_quantum_state().items())
        ],
        "Probabilidade (%)": [
            abs(p) ** 2 * 100
            for d in dump_states
            for _, p in sorted(d.get_quantum_state().items())
        ],
        "Passo": [
            i
            for i, d in enumerate(dump_states)
            for _ in range(len(d.get_quantum_state()))
        ],
    }

    prob_right = {
        "Estado": ["Procurado", "Outros"] * len(dump_states),
        "Probabilidade (%)": [
            p * 100
            for d in dump_states
            for p in [
                abs(d.get_quantum_state()[search_for]) ** 2,
                1 - abs(d.get_quantum_state()[search_for]) ** 2,
            ]
        ],
        "Passo": [i for i in range(len(dump_states)) for _ in range(2)],
    }

    return prob_all, prob_right


def grover_step_by_step(n, oracle, m=1):
    qubits = quant(n)
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

        ctrl(qubits[1:], Z, qubits[0])
        d.append(dump(qubits))

        for q in qubits:
            X(q)
            d.append(dump(qubits))
        for q in qubits:
            H(q)
            d.append(dump(qubits))
    return d


def grover_step_by_step_df(num_qubits, search_for):
    dump_states_step_by_step = grover_step_by_step(num_qubits, phase_on(search_for))
    return {
        "Estado": [s for _ in dump_states_step_by_step for s in range(1 << num_qubits)],
        "Probabilidade": [
            abs(d.get_quantum_state()[s]) if s in d.get_quantum_state() else 0.0
            for d in dump_states_step_by_step
            for s in range(1 << num_qubits)
        ],
        "Operação": [
            i
            for i, _ in enumerate(dump_states_step_by_step)
            for _ in range(1 << num_qubits)
        ],
        "Fase": [
            cmath.phase(complex(d.get_quantum_state()[s]))
            if s in d.get_quantum_state()
            else 0.0
            for d in dump_states_step_by_step
            for s in range(1 << num_qubits)
        ],
    }


# def grover_step_by_step_df(num_qubits, search_for):
#     dump_states_step_by_step = grover_step_by_step(num_qubits, phase_on(search_for))
#     return [
#         {
#             "Estado": [s for s in range(1 << num_qubits)],
#             "Probabilidade (%)": [
#                 abs(d.get_quantum_state()[s]) if s in d.get_quantum_state() else 0.0
#                 for s in range(1 << num_qubits)
#             ],
#             "Passo": [i for _ in range(1 << num_qubits)],
#             "Fase": [
#                 cmath.phase(complex(d.get_quantum_state()[s]))
#                 if s in d.get_quantum_state()
#                 else 0.0
#                 for s in range(1 << num_qubits)
#             ],
#         }
#         for i, d in enumerate(dump_states_step_by_step)
#     ]
