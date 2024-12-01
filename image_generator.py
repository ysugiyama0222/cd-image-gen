from PIL import Image, ImageDraw, ImageFont
import requests
import openai

def generate_image_with_ai(client, prompt, output_path, title, artist):
    """AIを使って背景画像を生成する"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url",
            style="vivid",
            quality="hd",
        )
        # 画像の保存処理などをここに追加
        image_url = response.data[0].url

        # 画像をダウンロードして保存
        background_path = "background_" + output_path
        download_image(image_url, background_path)

        # タイトルとアーティスト名を追加
        add_text_to_image(background_path, output_path, title, artist)

        # 画像を1600x1600に拡大
        enlarge_image(output_path)

    except openai.error.InvalidRequestError as e:
        print(f"Error code: {e.http_status} - {e.error}")

def download_image(url, output_path):
    """画像をダウンロードして保存する"""
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

def create_image_without_ai(background_path, output_path, title, artist):
    """AIを使わずに背景画像を生成する"""
    # タイトルとアーティスト名を追加
    add_text_to_image(background_path, output_path, title, artist)
    # 画像を1600x1600に拡大
    enlarge_image(output_path)

def enlarge_image(image_path):
    """画像を1600x1600に拡大する"""
    with Image.open(image_path) as img:
        img = img.resize((1600, 1600), Image.LANCZOS)
        img.save(image_path)

def add_text_to_image(background_path, image_path, title, artist):
    """画像にタイトルとアーティスト名を追加する"""
    with Image.open(background_path) as img:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 100)
        except IOError:
            font = ImageFont.load_default()
        # タイトルとアーティスト名を描画
        # パステルイエロー
        title_color = "rgb(255, 255, 102)"
        # パステルレッド
        artist_color = "rgb(255, 102, 102)"
        draw.text((50, 50), title, font=font, fill=title_color)
        draw.text((50, 150), artist, font=font, fill=artist_color)
        img.save(image_path)
