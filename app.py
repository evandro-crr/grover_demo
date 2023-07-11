from math import pi, sqrt
import streamlit as st
import plotly.express as px
import grover_app


@st.cache_data
def classical_vs_quantum_df(max_input, classical_speed):
    entradas = list(range(2, max_input))
    return {
        "Tamanho da Entrada": [*entradas, *entradas],
        "Tempo": [
            *[(i / 2) / classical_speed for i in entradas],
            *[sqrt(i) for i in entradas],
        ],
        "Modelo de Computação": [
            *["Clássico"] * len(entradas),
            *["Quântico"] * len(entradas),
        ],
    }


"# Computação Quântica"
"## Algoritmo Quântico de Busca (_Grover_)"

"### Desempenho Clássico Vs. Quântico"

plot_performance = st.container()
classical_speed = st.slider("Computador clássico X vezes mais rápido", 1.0, 15.0, 10.0)
plot_performance.plotly_chart(
    px.line(
        classical_vs_quantum_df(1 << 10, classical_speed),
        x="Tamanho da Entrada",
        y="Tempo",
        color="Modelo de Computação",
    ),
    use_container_width=True,
)


"### Demonstração"

config_columns = st.columns(2)

with config_columns[0]:
    len_itens = st.slider("Numero de itens", 1, (1 << 8) - 1, (1 << 4) - 1)
    num_qubits = len_itens.bit_length()
with config_columns[1]:
    search_for = st.slider("Procurar por", 0, len_itens, len_itens // 2)

f"""
#### Programação Quântica

```py
from math import pi, sqrt
from ket import *

def grover(n, oracle):
    qubits = quant(n)
    H(qubits)
    for _ in range(int((pi / 4) * sqrt(2**n / m))):
        oracle(qubits)
        with around([H, X], qubits):
            ctrl(qubits[1:], Z, qubits[0])
    return measure(qubits)

print("Resultado =", grover(n={num_qubits}, oracle=phase_on({search_for})).value)
# Resultado = {search_for}
```
    """

"#### Execução Quântica"

prob_all, prob_right = grover_app.grover_df(num_qubits, search_for)

"##### Probabilidade a cada passo de computação"

st.plotly_chart(
    px.bar(
        prob_all,
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Passo",
    ),
    use_container_width=True,
)

st.plotly_chart(
    px.bar(
        prob_right,
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Passo",
    ),
    use_container_width=True,
)


"##### Evolução do estado quântico"

st.plotly_chart(
    px.bar(
        grover_app.grover_step_by_step_df(num_qubits, search_for),
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Operação",
        color="Fase",
        range_color=(-pi, pi),
    ),
    use_container_width=True,
)
