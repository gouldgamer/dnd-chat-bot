import streamlit as st

st.text('st.text')
st.markdown('st.markdown') # see #*
st.caption('st.caption')
st.latex(r''' e^{i\pi} + 1 = 0 ''')
st.write('st.write') # df, err, func, keras!
st.write(['st', 'is <', 3]) # see *
st.title('My title')
st.header('My header')
st.subheader('My sub')
st.code('for i in range(8): foo()')