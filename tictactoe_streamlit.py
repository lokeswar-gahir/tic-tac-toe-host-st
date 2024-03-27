import streamlit as st
from streamlit.components.v1 import html
import random
from checker import get_best_coords_for_streamlit, find_winner, is_empty

styling = '''
<style>
[data-testid="baseButton-secondary"], [data-testid="baseButton-primary"]{
width:100px;
height:100px;
}
[data-testid="stAppViewBlockContainer"]{
padding: 1rem 1rem 1rem;
}
[data-testid="stVerticalBlockBorderWrapper"]{
/*max-width:371px;*/
}
[data-testid="column"]{
width:102px;
}

@media (max-width:640px){
    [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"]{
    width:75px;
    height:75px;
    }

    [data-testid="column"]{
    width:77px;
    }
}

@media (max-width:335px){
    [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"]{
    width:50px;
    height:50px;
    }

    [data-testid="column"]{
    width:52px;
    }
}

@media (max-width:260px){
    [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"]{
    width:38px;
    height:38px;
    }

    [data-testid="column"]{
    width:40px;
    }
}

@media (max-width:222px){
    [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"]{
    width:15px;
    height:15px;
    }

    [data-testid="column"]{
    width:17px;
    }
}
</style>
'''

def reset_board():
    st.session_state["board"]=[["_", "_", "_"],["_", "_", "_"],["_", "_", "_"]]
    st.session_state["playable"]=True
    print("---New Game started---")

if "board" not in st.session_state:
    reset_board()
    st.session_state["play_again"]=False
if "message" not in st.session_state:
    st.session_state["message"]=None

st.markdown(styling, unsafe_allow_html=True)
st.title("Tic Tac Toe:lt (with AI)")
st.write("AI will predict the best possible move.:lt Here we go")
container = st.container(border=True)
row1 = container.columns(3)
row2 = container.columns(3)
row3 = container.columns(3)

def set_value(coordinates):
    coordinates = list(map(int,list(coordinates)))
    if st.session_state["board"][coordinates[0]][coordinates[1]]=="_" and st.session_state["playable"]:
        st.session_state["board"][coordinates[0]][coordinates[1]]="X"
        print("\nHuman choose:",coordinates,"\n")
        winning_status = find_winner(st.session_state["board"])
        if winning_status == "INCOMPLETE GAME":
            now_ai("O")
        elif winning_status == "X":
            st.session_state["message"]="HUMAN"
            st.balloons()
            st.session_state["play_again"]=True
            return
        elif winning_status=="DRAW":
            st.session_state["message"]="DRAW"
            st.session_state["play_again"]=True
            return
    else:
        st.session_state["message"]="NOT ALLOWED"

def now_ai(play_as):
    recieved_score=list()
    best_coord = get_best_coords_for_streamlit(st.session_state["board"], recieved_score, play_as)
    if len(best_coord)>2:
        best_coord = random.choice(best_coord)[1:]
    else:
        if len(best_coord)==2:
            if best_coord[-1][0][0]=="draw":
                best_coord = best_coord[-2][1:]
            else:
                best_coord = best_coord[-1][1:]
        else:
            best_coord = best_coord[0][1:]
    
    print("Best Move Choosen:", best_coord,"\n")
    st.session_state["board"][best_coord[0]][best_coord[1]]=play_as
    winning_status = find_winner(st.session_state["board"])
    if winning_status == play_as:
        st.session_state["message"]="AI"
        st.balloons()
        st.session_state["play_again"]=True
        return

for i ,row in enumerate([row1, row2, row3]):
    for j in range(3):
        if st.session_state["board"][i][j]=="O":
            row[j].button(st.session_state["board"][i][j], key="btn"+str(i)+str(j), on_click=set_value, args=[str(i)+str(j)], type="primary")
        else:    
            row[j].button(st.session_state["board"][i][j], key="btn"+str(i)+str(j), on_click=set_value, args=[str(i)+str(j)])

if st.session_state["message"]:
    if st.session_state["message"]=="AI":
        st.success("AI is the WINNER.", icon="🤖")
        print("\n\t---AI is the winner---\n")
    elif st.session_state["message"] =="DRAW":
        st.warning("This Match is DRAW.",icon="🚨")
        print("\n\t---This match is draw---\n")
    elif st.session_state["message"] =="HUMAN":
        st.success("YOU are the WINNER.")
        print("\n\t---HUMAN is the winner---\n")
    elif st.session_state["message"] =="NOT ALLOWED":
        st.warning("This action is not allowed !!!", icon="⚠️")
    st.session_state["message"]=None

if st.session_state["play_again"] or not st.session_state["playable"]:
    st.session_state["playable"]=False
    st.button("Play Again", on_click=reset_board)
    st.session_state["play_again"]=False
html_string = '''
<script>
// this if is for "play_again" button size
if (window.parent.document.querySelectorAll("p").length == 12){

    window.parent.document.querySelectorAll("p")[11].parentNode.parentNode.style.height="50px";
    window.parent.document.querySelectorAll("p")[11].parentNode.parentNode.style.width="100px";
    
}

// For removing all classes of buttons
mainNodes= window.parent.document.querySelectorAll(".row-widget")[0].parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.childNodes
mainNodes.forEach((row)=>{
row.childNodes.forEach((element)=>{
element.className=""
})
})

</script>
'''
html(html_string, height=0, width=0)
