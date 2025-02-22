import streamlit as st
from few_shots import FewShotPosts
from generator import generate
lang_opt = ['English', 'Hinglish']
length_opt = ['LONG', 'MEDIUM', 'SHORT']
 # this code is for creating an easy user interface


def main():
    st.set_page_config(page_title="Generate your post for LinkedIn", page_icon="📝", layout="centered")
    # Title with icon
    st.markdown("<h1 style='text-align: center;'>📢 Generate Your LinkedIn Post</h1>", unsafe_allow_html=True)

    st.divider()  # Adds a visual separator
    fs = FewShotPosts()
    # Dropdowns
    with st.expander("🔽 Choose Your Preferences", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            selected_title = st.selectbox("🎯 Select a Topic", options=fs.get_tags())

        with c2:
            selected_length = st.selectbox("📏 Choose Length", options=length_opt)

        with c3:
            selected_lang = st.selectbox("🌍 Select Language", options=lang_opt)

    if st.button("Generate"):
        post = generate(selected_length, selected_lang, selected_title)
        st.write(post)

if __name__ == "__main__":
    main()
