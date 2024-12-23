import streamlit as st
import bcrypt
import time

HASHED_USERNAME = b'$2b$12$6Z7uGGvuoXjuAOASX7irDOTstWuQCsys.LziYYP6cHKk5X1qFUAYy' 
HASHED_PASSWORD = b'$2b$12$Sk935GMM.9WwjQkgelg7UeELjwO2/T1DDb5S/nn.G1qqAmUFUTn0e'  

def authenticate(username, password):
    username_valid = bcrypt.checkpw(username.encode(), HASHED_USERNAME)
    password_valid = bcrypt.checkpw(password.encode(), HASHED_PASSWORD)
    return username_valid and password_valid

def login_page():
    st.title("Tela de Autenticação")
    st.write("Por favor, faça login para continuar.")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Login")
    #reload_param = st.query_params.get("reload", "0")
    if login_button:
        if authenticate(username, password):
            st.success("Login realizado com sucesso!")
            st.session_state["authenticated"] = True
            #redirecionar para a página principal
            st.write("Redirecionando para a página principal...")
            time.sleep(3)
            st.rerun()

        else:
            st.error("Usuário ou senha incorretos!")

def main_page():
    st.title("Página Principal")
    st.write("Bem-vindo à aplicação!")


    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main_page()
else:
    login_page()
