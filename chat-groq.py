import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def main():
    st.title("Chat con Groq")
    
    # Solicitar API key de Groq
    groq_api_key = st.text_input("Introduce tu API key de Groq:", type="password")
    
    if not groq_api_key:
        st.warning("Por favor, introduce tu API key de Groq para continuar.")
        st.stop()
    
    # Configurar el modelo de Groq (por defecto llama3-70b-8192)
    model_name = st.selectbox(
        "Selecciona el modelo de Groq:",
        ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]
    )
    
    # Inicializar el LLM de Groq con la API key proporcionada
    llm = ChatGroq(model_name=model_name, groq_api_key=groq_api_key)
    
    bot_name = st.text_input("Nombre del asistente virtual:", value="Ángela")
    prompt = f"""Eres un asistente virtual te llamas {bot_name}, respondes preguntas con respuestas simples, además debes preguntar al usuario acorde al contexto del chat, también debes preguntarle cosas básicas al usuario para conocerlo"""
    bot_description = st.text_area("Descripción del asistente virtual:",
                                   value=prompt)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm

    user_input = st.text_input("Escribe tu pregunta:", key="user_input")

    if st.button("Enviar"):
        if user_input.lower() == "adios":
            st.stop()
        else:
            with st.spinner("Generando respuesta..."):
                response = chain.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
                st.session_state["chat_history"].append(HumanMessage(content=user_input))
                st.session_state["chat_history"].append(AIMessage(content=response.content))

    chat_display = ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            chat_display += f"👤 Humano: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_display += f"🤖 {bot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_display, height=400, key="chat_area")


if __name__ == "__main__":
    main()