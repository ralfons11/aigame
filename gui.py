import streamlit as st
from main import create_game, make_move, get_winner
from tree import find_best_move

st.title("Spēle ar AI")

# --- session defaults ---
defaults = {
    "numbers": [],
    "total": 0,
    "bank": 0,
    "turn": 1,
    "history": [],
    "game_over": False,
    "selected": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def game_over(numbers):
    return len(numbers) == 0


# --- izvēles ---
length = st.number_input("Garums", 15, 20, 15)
starter = st.radio("Kurš sāk?", ["Spēlētājs", "AI"])
algorithm = st.radio("Algoritms", ["Minimax", "Alpha-Beta"])


# --- start ---
if st.button("Sākt spēli"):
    st.session_state.numbers = create_game(length)
    st.session_state.total = 0
    st.session_state.bank = 0
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.selected = None

    st.session_state.turn = 1 if starter == "Spēlētājs" else 2

    st.rerun()


# --- vēsture ---
st.subheader("Gājienu vēsture:")
for h in st.session_state.history:
    st.write(h)


# --- beigas ---
if st.session_state.game_over:
    st.subheader("Spēle beigusies!")
    st.write("Total:", st.session_state.total)
    st.write("Banka:", st.session_state.bank)

    winner = get_winner(st.session_state.total, st.session_state.bank)
    st.success(winner)
    st.stop()


# --- skaitļu izvēle ---
if st.session_state.numbers:

    st.subheader("Izvēlies skaitli:")

    cols = st.columns(len(st.session_state.numbers))

    for i, num in enumerate(st.session_state.numbers):
        with cols[i]:
            if st.button(str(num), key=f"num_{i}"):

                if st.session_state.turn != 1:
                    st.rerun()

                # 🔥 1 un 3 → uzreiz TAKE
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

                    st.session_state.history.append(f"Spēlētājs: {num}")
                    st.session_state.selected = None

                    if game_over(new_numbers):
                        st.session_state.game_over = True
                    else:
                        st.session_state.turn = 2

                    st.rerun()

                # 🔥 2 un 4 → izvēle
                else:
                    st.session_state.selected = num
                    st.rerun()


# --- darbības (tikai 2 un 4) ---
if st.session_state.selected is not None and st.session_state.turn == 1:

    num = st.session_state.selected
    st.subheader(f"Darbības ar {num}:")

    col1, col2 = st.columns(2)

    # TAKE
    with col1:
        if st.button("Take"):

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

            st.session_state.history.append(f"Spēlētājs: {num} (take)")
            st.session_state.selected = None

            if game_over(new_numbers):
                st.session_state.game_over = True
            else:
                st.session_state.turn = 2

            st.rerun()

    # SPLIT
    with col2:
        if st.button("Split"):

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

            st.session_state.history.append(f"Spēlētājs: {num} (split)")
            st.session_state.selected = None

            if game_over(new_numbers):
                st.session_state.game_over = True
            else:
                st.session_state.turn = 2

            st.rerun()


# --- info ---
st.subheader("Spēles stāvoklis")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total", st.session_state.total)

with col2:
    st.metric("Banka", st.session_state.bank)


# --- AI ---
if st.session_state.turn == 2 and not st.session_state.game_over:

    best = find_best_move(
        st.session_state.numbers,
        st.session_state.total,
        st.session_state.bank,
        algorithm
    )

    if best:
        st.session_state.numbers = best.numbers
        st.session_state.total = best.total
        st.session_state.bank = best.bank

        st.session_state.history.append(f"AI: {best.move}")

        if game_over(best.numbers):
            st.session_state.game_over = True
        else:
            st.session_state.turn = 1

    st.rerun()