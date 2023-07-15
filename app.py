from math import pi, sqrt
import streamlit as st
import plotly.express as px
import grover_app

st.set_page_config(
    page_title="Grupo de Computação Quântica",
    page_icon="logo_gcq.jpeg",
    initial_sidebar_state="expanded"
)


@st.cache_data
def grover_df(*args):
    return grover_app.grover_df(*args)


@st.cache_data
def grover_step_by_step_df(*args):
    return grover_app.grover_step_by_step_df(*args)


@st.cache_data
def classical_vs_quantum_df(max_input, step, classical_speed):
    entradas = list(range(2, max_input, step))
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
st.sidebar.image("logo_gcq.jpeg")
st.sidebar.title("Grupo de Computação Quântica - UFSC")

st.image(
    "https://newsroom.ibm.com/file.php/183868/IBM_SystemOne_Andrew_Lindemann_2-1500.jpg?thumbnail=modal",
    use_column_width=True,
    caption="Fonte: https://newsroom.ibm.com",
)

"# Algoritmo Quântico de Busca (_Algoritmo de Grover_)"
"## Desempenho Clássico Vs. Quântico"

plot_performance = st.container()
classical_speed = st.slider("Performance to computador clássico", 5_000, 15_000, 10_000)
classical_speed_str = f"{classical_speed:,}x".replace(",", ".")
plot_performance.plotly_chart(
    px.line(
        classical_vs_quantum_df(1_000_000_000, 1_000_000, classical_speed),
        x="Tamanho da Entrada",
        y="Tempo",
        color="Modelo de Computação",
        title=f"Tempo de computação com computador clássico {classical_speed_str} mais rápido que o quântico.",
    ),
    use_container_width=True,
)

st.divider()

"# Demonstração"
"Parâmetros da demostração"

config_columns = st.columns(2)
with config_columns[0]:
    len_itens = st.slider("Numero de itens", 1, (1 << 8) - 1, (1 << 4) - 1)
    num_qubits = len_itens.bit_length()
with config_columns[1]:
    search_for = st.slider("Procurar por", 0, len_itens, len_itens // 2)

"## Programação Quântica"

logo, text = st.columns([1, 4])
with logo:
    st.image("https://quantumket.org/_static/ket.svg", use_column_width=True)
with text:
    "### Plataforma de programação quântica desenvolvida no GCQ-UFSC"
"<https://quantumket.org>"


f"""
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

"## Execução Quântica"

prob_all, prob_right = grover_df(num_qubits, search_for)

"### Probabilidade a cada passo de computação"

st.plotly_chart(
    px.bar(
        prob_all,
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Passo",
        title="Probabilidade de medida de cada estado",
    ),
    use_container_width=True,
)

st.plotly_chart(
    px.bar(
        prob_right,
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Passo",
        title="Probabilidade de medida do estado certo",
    ),
    use_container_width=True,
)


"## Evolução do estado quântico (Computação)"

st.plotly_chart(
    px.bar(
        grover_step_by_step_df(num_qubits, search_for),
        x="Estado",
        y="Probabilidade (%)",
        animation_frame="Operação",
        color="Fase",
        range_color=(-pi, pi),
    ),
    use_container_width=True,
)
