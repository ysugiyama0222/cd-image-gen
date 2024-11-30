import argparse
import requests
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import configparser
import os

# ConfigParserオブジェクトを生成
config = configparser.ConfigParser()
# config.iniファイルを読み込む
config.read('config.ini')
# APIキーを取得
api_key = config['API_KEYS'].get('OPENAI_API_KEY')
# APIキーが取得できているか確認
if not api_key:
    raise ValueError("APIキーが設定されていません。config.iniを確認してください。")

client = OpenAI(api_key=api_key)

def generate_image_with_ai(prompt, output_path):
    """AIを使って背景画像を生成する"""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",  # サポートされているサイズに変更
        response_format="url",
        style="vivid",
        quality="hd",
    )
    data = requests.get(response.data[0].url).content
    with open(output_path, "wb") as handler:
        handler.write(data)
    
    # 画像を1600x1600に拡大
    img = Image.open(output_path)
    img = img.resize((1600, 1600), Image.LANCZOS)
    img.save(output_path)
    
    return output_path

def create_cd_jacket(background_path, output_file, title, artist):
    """CDジャケットを作成する"""
    # 背景画像を開く
    background = Image.open(background_path)
    draw = ImageDraw.Draw(background)

    # フォントの設定
    try:
        font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 100)
    except OSError:
        font = ImageFont.load_default()

    # タイトルとアーティスト名を描画
    # パステルイエロー
    title_color = "rgb(255, 255, 102)"
    # パステルレッド
    artist_color = "rgb(255, 102, 102)"
    draw.text((50, 50), title, font=font, fill=title_color)
    draw.text((50, 150), artist, font=font, fill=artist_color)

    # 画像を保存
    background.save(output_file)

def main():
    parser = argparse.ArgumentParser(description="CDジャケット画像を生成するツール")
    parser.add_argument("--output_file", required=True, help="出力ファイル名")
    parser.add_argument("--title", required=True, help="タイトル")
    parser.add_argument("--artist", required=True, help="アーティスト名")
    parser.add_argument("--use_ai", action="store_true", help="AIを使用して背景画像を生成する")
    parser.add_argument("--ai_prompt", help="AIに渡すプロンプト")

    args = parser.parse_args()

    if args.use_ai:
        background_path = generate_image_with_ai(args.ai_prompt, "background.png")
    else:
        background_path = "default_background.png"  # デフォルトの背景画像

    create_cd_jacket(background_path, args.output_file, args.title, args.artist)

if __name__ == "__main__":
    main()
