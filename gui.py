import streamlit as st
import pandas as pd
from main import create_game, make_move, get_winner
from tree import find_best_move

st.set_page_config(page_title="Skaitļu spēle AI", layout="wide")

# session defaults
defaults = {
    "numbers": [],
    "total": 0,
    "bank": 0,
    "turn": 1,
    "history": [],
    "game_over": False,
    "selected": None,
    "game_count": 0,
    "stats": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def game_over(numbers):
    return len(numbers) == 0

# sidebar
with st.sidebar:
    st.header("Navigācija")
    page = st.radio("Izvēlne:", ["Spēle", "AI Statistika"])
    
    st.write("---")
    # Izvēles paliek šeit
    length = st.slider("Virknes garums", min_value=15, max_value=20, value=15)
    starter = st.radio("Kurš sāk?", ["Spēlētājs", "AI"])
    algorithm = st.radio("Algoritms", ["Minimax", "Alpha-Beta"])
    depth = st.slider("Meklēšanas dziļums", min_value=3, max_value=6, value=3)

    if st.button("Sākt spēli"):
        st.session_state.game_count += 1
        st.session_state.numbers = create_game(length)
        st.session_state.total = 0
        st.session_state.bank = 0
        st.session_state.history = []
        st.session_state.game_over = False
        st.session_state.selected = None
        st.session_state.turn = 1 if starter == "Spēlētājs" else 2
        st.rerun()
    
def highlight_ai(row):
    # Ja kolonnā "Kas" ir vērtība "AI", atgriežam stila iestatījumu rindas fonam
    if row['Kas'] == 'AI':
        return ['background-color: #1A1C23; color: #90D5FF'] * len(row)
    return [''] * len(row)

if page == "Spēle":
    st.title("Spēle ar AI")

    # info (Stāvoklis augšā)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", st.session_state.total)
    with col2:
        st.metric("Banka", st.session_state.bank)

    # beigas
    if st.session_state.game_over:
        st.subheader("Spēle beigusies!")
        st.write("Total:", st.session_state.total)
        st.write("Banka:", st.session_state.bank)

        winner = get_winner(st.session_state.total, st.session_state.bank)
        st.success(winner)


    # skaitļu izvēle
    if st.session_state.numbers:
        st.subheader("Izvēlies skaitli:")
        cols = st.columns(len(st.session_state.numbers))

        h_len = len(st.session_state.history)

        for i, num in enumerate(st.session_state.numbers):
            with cols[i]:

                is_disabled = (st.session_state.turn != 1) or (st.session_state.selected is not None)
        
                if st.button(str(num), key=f"btn_{i}_{h_len}", disabled=is_disabled):
        # uzreiz TAKE
                        if num in [1, 3]:
                            new_numbers, new_total, new_bank = make_move(
                                st.session_state.numbers,
                                num,
                                st.session_state.total,
                                st.session_state.bank,
                                "take"
                            )

                            st.session_state.numbers = new_numbers
                            st.session_state.total = new_total
                            st.session_state.bank = new_bank

                            st.session_state.history.append({
                                "Gājiens": len(st.session_state.history) + 1,
                                "Kas": "Spēlētājs",
                                "Skaitlis": str(num),
                                "Darbība": "Take",
                                "Total": new_total,
                                "Banka": new_bank
                            })
                            st.session_state.selected = None

                            if game_over(new_numbers):
                                st.session_state.game_over = True
                            else:
                                st.session_state.turn = 2

                            st.rerun()

        # izvēle 2 un 4
                        else:
                            st.session_state.selected = num
                            st.rerun()


    # darbības (tikai 2 un 4)
    if st.session_state.selected is not None and st.session_state.turn == 1:

        num = st.session_state.selected
        st.subheader(f"Darbības ar {num}:")

        col1, col2 = st.columns(2)

    # TAKE
        with col1:
            if st.button("Take", key=f"take_{num}_{h_len}"):

                new_numbers, new_total, new_bank = make_move(
                    st.session_state.numbers,
                    num,
                    st.session_state.total,
                    st.session_state.bank,
                    "take"
                )

                st.session_state.numbers = new_numbers
                st.session_state.total = new_total
                st.session_state.bank = new_bank

                st.session_state.history.append({
                    "Gājiens": len(st.session_state.history) + 1,
                    "Kas": "Spēlētājs",
                    "Skaitlis": str(num),
                    "Darbība": "Take",
                    "Total": new_total,
                    "Banka": new_bank
                })
                st.session_state.selected = None

                if game_over(new_numbers):
                    st.session_state.game_over = True
                else:
                    st.session_state.turn = 2

                st.rerun()

    # SPLIT
        with col2:
           if st.button("Split", key=f"split_{num}_{h_len}"):
                
                new_numbers, new_total, new_bank = make_move(
                    st.session_state.numbers,
                    num,
                    st.session_state.total,
                    st.session_state.bank,
                    "split"
                )

                st.session_state.numbers = new_numbers
                st.session_state.total = new_total
                st.session_state.bank = new_bank

                st.session_state.history.append({
                    "Gājiens": len(st.session_state.history) + 1,
                    "Kas": "Spēlētājs",
                    "Skaitlis": str(num),
                    "Darbība": "Split",
                    "Total": new_total,
                    "Banka": new_bank
                })
                st.session_state.selected = None

                if game_over(new_numbers):
                    st.session_state.game_over = True
                else:
                    st.session_state.turn = 2

                st.rerun()
    # history
    st.subheader("Gājienu vēsture:")
    if st.session_state.history:
        df_history = pd.DataFrame(st.session_state.history)
        
        # Nodrošinām datu tipu konsekvenci, lai izvairītos no Arrow kļūdām
        df_history["Skaitlis"] = df_history["Skaitlis"].astype(str)
        
        # Pielietojam stilu: apply(funkcija, axis=1 nozīmē pa rindām)
        styled_df = df_history.style.apply(highlight_ai, axis=1)
        
        # Attēlojam stilizēto tabulu
        st.table(styled_df)
    else:
        st.info("Gājienu vēsture parādīsies šeit.")

# AI  
if st.session_state.turn == 2 and not st.session_state.game_over:
    with st.spinner("AI gājiens..."):

        starter_type = 1 if starter == "Spēlētājs" else 2

        best, nodes_generated, nodes_evaluated, duration = find_best_move(
            st.session_state.numbers,
            st.session_state.total,
            st.session_state.bank,
            algorithm,
            starter_type,
            depth
        )

        if best:

            st.session_state.stats.append({
                        "Spēle #": st.session_state.game_count,
                        "Algoritms": algorithm,
                        "Ģenerētas virsotnes": nodes_generated,
                        "Novērtētas virsotnes": nodes_evaluated,
                        "Laiks (s)": round(duration, 4)
                    })
            
            move_parts = best.move.split()

            st.session_state.numbers = best.numbers
            st.session_state.total = best.total
            st.session_state.bank = best.bank
            st.session_state.history.append({
                "Gājiens": len(st.session_state.history) + 1,
                "Kas": "AI",
                "Skaitlis": str(move_parts[0]),
                "Darbība": "Take" if "take" in best.move else "Split",
                "Total": best.total,
                "Banka": best.bank
            })

            if game_over(best.numbers):
                st.session_state.game_over = True
            else:
                st.session_state.turn = 1

        st.rerun()
            
elif page == "AI Statistika":
    st.title("Statistika")

    if st.session_state.stats:
        df = pd.DataFrame(st.session_state.stats)
        
        # Iegūstam unikālos spēļu numurus dilstošā secībā (jaunākā pirmā)
        game_ids = sorted(df["Spēle #"].unique(), reverse=True)

        for g_id in game_ids:
            with st.expander(f"🎮 Spēle Nr. {g_id}", expanded=(g_id == max(game_ids))):
                # Filtrējam datus tikai šai spēlei
                game_df = df[df["Spēle #"] == g_id].drop(columns=["Spēle #"])
                
                # Parādām kopsavilkumu (metrikas)
                m1, m2 = st.columns(2)
                m1.metric("Kopā gājieni (AI)", len(game_df))
                m2.metric("Vid. laiks (s)", round(game_df["Laiks (s)"].mean(), 4))
                
                # Tabula ar datiem
                st.dataframe(game_df, use_container_width=True, hide_index=True)
                
                # Grafiks katrai spēlei atsevišķi
                st.line_chart(game_df[["Ģenerētas virsotnes", "Novērtētas virsotnes"]])
    else:
        st.info("Statistika būs pieejama pēc pirmajiem AI gājieniem.")
