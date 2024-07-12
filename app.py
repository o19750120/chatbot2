from openai import OpenAI
import streamlit as st


def main():

    openai_api_key = "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"

    # Initialize session state if not already done
    if "chatbot_active" not in st.session_state:
        st.session_state["chatbot_active"] = False

    # Create a form for the text areas and button
    with st.form(key='input_form'):
        col1, col2 = st.columns(2)
        with col1:
            text_area_1 = st.text_area("Input 1", key="input1")
        with col2:
            text_area_2 = st.text_area("Input 2", key="input2")

        submit_button = st.form_submit_button(label="Send")

    if submit_button:
        # Combine the text from both text areas
        combined_input = f"{st.session_state['input1']} {st.session_state['input2']}"
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        st.session_state.messages.append({
            "role": "user",
            "content": combined_input
        })
        st.session_state["chatbot_active"] = True

    if st.session_state["chatbot_active"]:
        st.title("💬 Chatbot")

        # Display existing messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if openai_api_key:
            client = OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o", messages=st.session_state.messages)
            msg = response.choices[0].message.content
            st.session_state.messages.append({
                "role": "assistant",
                "content": msg
            })
            st.chat_message("assistant").write(msg)
        else:
            st.info("Please add your OpenAI API key to continue.")

        if prompt := st.chat_input():
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            st.chat_message("user").write(prompt)

            if openai_api_key:
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-4o", messages=st.session_state.messages)
                msg = response.choices[0].message.content
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": msg
                })
                st.chat_message("assistant").write(msg)
            else:
                st.info("Please add your OpenAI API key to continue.")


if __name__ == '__main__':
    main()
