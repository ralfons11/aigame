import streamlit as st
from main import create_game, make_move, get_winner
from tree import find_best_move

st.set_page_config(page_title="Skaitļu spēle MI", layout="wide")
st.title("🎲 Skaitļu spēle: Minimakss vs Alfa-Beta")

# Inicializējam pastāvīgos sesijas mainīgos
if "experiments" not in st.session_state:
    st.session_state.experiments = []
if "game_counter" not in st.session_state:
    st.session_state.game_counter = 0
if "win_stats" not in st.session_state:
    st.session_state.win_stats = {"Cilvēks": 0, "Dators": 0, "Neizšķirts": 0}
if "winner_logged" not in st.session_state:
    st.session_state.winner_logged = False

# Sānjoslas iestatījumi
with st.sidebar:
    st.header("Iestatījumi")
    length = st.slider("Virknes garums", 15, 20, 15)
    starter = st.selectbox("Kurš sāk?", ["Cilvēks", "Dators"])
    algorithm = st.radio("Algoritms", ["Minimax", "Alpha-Beta"])
    depth = st.slider("AI pārlūkošanas dziļums (n-gājieni)", 2, 6, 3)
    
    st.write("---")
    st.write(f"**Kopējā statistika:**")
    st.write(f"🏆 Cilvēks: {st.session_state.win_stats['Cilvēks']}")
    st.write(f"🤖 Dators: {st.session_state.win_stats['Dators']}")
    st.write(f"🤝 Neizšķirti: {st.session_state.win_stats['Neizšķirts']}")
    
    if st.button("Uzsākt jaunu spēli"):
        st.session_state.game_counter += 1 # Šis nodrošina pareizu spēles ID tabulā
        st.session_state.numbers = create_game(length)
        st.session_state.total = 0
        st.session_state.bank = 0
        st.session_state.turn = 1 if starter == "Cilvēks" else 2
        st.session_state.history = []
        st.session_state.game_over = False
        st.session_state.winner_logged = False
        st.session_state.selected_num = None
        st.rerun()

if "numbers" not in st.session_state:
    st.info("Sānjoslā izvēlieties parametrus un spiediet 'Uzsākt jaunu spēli'.")
    st.stop()

# Galvenais spēles laukums
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Spēle #{st.session_state.game_counter}")
    # Skaitļu pogu ģenerēšana
    cols = st.columns(len(st.session_state.numbers) if st.session_state.numbers else 1)
    for i, num in enumerate(st.session_state.numbers):
        if cols[i].button(str(num), key=f"btn_{i}", disabled=st.session_state.turn == 2 or st.session_state.game_over):
            if num in [2, 4]:
                st.session_state.selected_num = (i, num)
            else:
                n, t, b = make_move(st.session_state.numbers, num, st.session_state.total, st.session_state.bank, "take")
                st.session_state.numbers, st.session_state.total, st.session_state.bank = n, t, b
                st.session_state.history.append(f"Cilvēks: Paņēma {num}")
                st.session_state.turn = 2
            st.rerun()

    # Darbības izvēle skaitļiem 2 un 4
    if st.session_state.selected_num:
        idx, val = st.session_state.selected_num
        st.info(f"Izvēlēts skaitlis **{val}**")
        c1, c2 = st.columns(2)
        if c1.button("Paņemt (Take)"):
            n, t, b = make_move(st.session_state.numbers, val, st.session_state.total, st.session_state.bank, "take")
            st.session_state.numbers, st.session_state.total, st.session_state.bank = n, t, b
            st.session_state.history.append(f"Cilvēks: Paņēma {val}")
            st.session_state.selected_num = None
            st.session_state.turn = 2
            st.rerun()
        if c2.button("Sadalīt (Split)"):
            n, t, b = make_move(st.session_state.numbers, val, st.session_state.total, st.session_state.bank, "split")
            st.session_state.numbers, st.session_state.total, st.session_state.bank = n, t, b
            st.session_state.history.append(f"Cilvēks: Sadalīja {val}")
            st.session_state.selected_num = None
            st.session_state.turn = 2
            st.rerun()

with col2:
    st.metric("Punkti (Total)", st.session_state.total)
    st.metric("Banka", st.session_state.bank)
    st.write("**Gājienu vēsture:**")
    for log in reversed(st.session_state.history[-5:]):
        st.text(log)

# AI Gājiens (Dators)
if st.session_state.turn == 2 and not st.session_state.game_over:
    if not st.session_state.numbers:
        st.session_state.game_over = True
        st.rerun()
        
    with st.spinner("AI domā..."):
        best_node, nodes, duration = find_best_move(
            st.session_state.numbers, st.session_state.total, st.session_state.bank, algorithm, depth
        )
        
        if best_node:
            # Reģistrējam datus eksperimentu tabulai ar korektu Spēles ID
            st.session_state.experiments.append({
                "Spēle": st.session_state.game_counter,
                "Algoritms": algorithm,
                "Virsotnes": nodes,
                "Laiks (s)": round(duration, 5)
            })
            st.session_state.numbers = best_node.numbers
            st.session_state.total = best_node.total
            st.session_state.bank = best_node.bank
            st.session_state.history.append(f"AI: {best_node.move}")
            
        st.session_state.turn = 1
        if not st.session_state.numbers:
            st.session_state.game_over = True
        st.rerun()

# Rezultātu apstrāde spēles beigās
if st.session_state.game_over or not st.session_state.numbers:
    result_text = get_winner(st.session_state.total, st.session_state.bank)
    st.success(result_text)
    
    # Pieskaitām uzvaru attiecīgajam spēlētājam (tikai vienu reizi per spēli)
    if not st.session_state.winner_logged:
        if "Neizšķirts" in result_text:
            st.session_state.win_stats["Neizšķirts"] += 1
        elif "pirmais" in result_text:
            # Uzvarēja tas, kurš sāka
            st.session_state.win_stats[starter] += 1
        else:
            # Uzvarēja otrais spēlētājs
            other = "Dators" if starter == "Cilvēks" else "Cilvēks"
            st.session_state.win_stats[other] += 1
        st.session_state.winner_logged = True

# Eksperimentu datu tabula
if st.session_state.experiments:
    st.divider()
    st.subheader("📊 Eksperimentu dati (Datora veiktspēja)")
    st.table(st.session_state.experiments)