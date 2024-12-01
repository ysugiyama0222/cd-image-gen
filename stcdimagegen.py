import streamlit as st
from openai_client import get_openai_client
from image_generator import generate_image_with_ai, create_image_without_ai

def main():
    st.title("CDカバー画像生成アプリ")

    output_file = st.text_input('生成された画像の保存先パス', 'cat.png')
    title = st.text_input('CDのタイトル', 'cat')
    artist = st.text_input('アーティスト名', 'LON')
    use_ai = st.checkbox('AIを使用して画像を生成する', True)
    ai_prompt = st.text_input('AI画像生成のためのプロンプト', 'たくさんの猫が襲ってくる, ピカソ風デザイン, モノトーン, アクセントカラーオレンジ')

    if st.button('画像を生成'):
        if use_ai:
            client = get_openai_client()
            generate_image_with_ai(client, ai_prompt, output_file, title, artist)
        else:
            create_image_without_ai("default_background.png", output_file, title, artist)
        
        st.image(output_file, caption='生成されたCDカバー画像')

if __name__ == "__main__":
    main()
