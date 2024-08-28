

if user_input:
    if user_input.lower() == "continue":
        # If 'continue' is typed, Gorc responds to Momos' last reply
        if st.session_state.chat2.history:
            last_momos_response = st.session_state.chat2.history[-1].parts[0].text
            response_gork = st.session_state.chat1.send_message(last_momos_response)
            st.chat_message("user").write("continue")
            with st.chat_message("Gork"):
                st.image("images/orc_avatar-2024-06-18-16-32-10.webp", width=100)
                st.write(response_gork.text)

            # Add a short delay before getting Momos' response
            time.sleep(2)  # Adjust the time as needed (in seconds)

            # Now get Momos' response to Gorc's new statement
            response_momos = st.session_state.chat2.send_message(response_gork.text)
            with st.chat_message('Momos'):
                st.image("images/dwarf-2024-06-18-17-24-27.webp", width=100)
                st.write(response_momos.text)

    else:
        # User prompts Gorc with a new input
        response1 = st.session_state.chat1.send_message(user_input)
        st.chat_message("user").write(user_input)
        with st.chat_message("Gork"):
            st.image("images/orc_avatar-2024-06-18-16-32-10.webp", width=100)
            st.write(response1.text)

        # Add a short delay before getting Momos' response
        time.sleep(2)

        # Momos responds to Gorc's statement
        response2 = st.session_state.chat2.send_message(response1.text)
        with st.chat_message('Momos'):
            st.image("images/dwarf-2024-06-18-17-24-27.webp", width=100)
            st.write(response2.text)