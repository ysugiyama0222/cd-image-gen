import argparse
from openai_client import get_openai_client
from image_generator import generate_image_with_ai, create_image_without_ai

def main(output_file, title, artist, use_ai, ai_prompt):
    if use_ai:
        client = get_openai_client()
        generate_image_with_ai(client, ai_prompt, output_file, title, artist)
    else:
        create_image_without_ai("default_background.png", output_file, title, artist)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CDカバー画像を生成します")
    parser.add_argument('--output_file', type=str, required=True, help='生成された画像の保存先パス')
    parser.add_argument('--title', type=str, required=True, help='CDのタイトル')
    parser.add_argument('--artist', type=str, required=True, help='アーティスト名')
    parser.add_argument('--use_ai', action='store_true', help='AIを使用して画像を生成するかどうか')
    parser.add_argument('--ai_prompt', type=str, help='AI画像生成のためのプロンプト')
    args = parser.parse_args()
    
    main(args.output_file, args.title, args.artist, args.use_ai, args.ai_prompt)
