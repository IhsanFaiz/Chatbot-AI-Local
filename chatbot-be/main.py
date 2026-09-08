import argparse
import sys

from config import init_directories
from model_manager import download_models, check_sys

def main():
    parser = argparse.ArgumentParser(description="Nox AI Chatbot Backend Server & CLI")
    parser.add_argument('--cli', action='store_true', help='Run interactive terminal CLI chat mode')
    parser.add_argument('--download-models', action='store_true', help='Download all GGUF models and exit')
    parser.add_argument('--port', type=int, default=5000, help='Port for Flask API server (default: 5000)')
    parser.add_argument('--no-ngrok', action='store_true', help='Disable Ngrok tunnel for API server')

    args = parser.parse_args()

    init_directories()

    if args.download_models:
        print("[Main] Starting model download...")
        download_models()
        print("[Main] Downloads completed.")
        sys.exit(0)

    if args.cli:
        from cli import start_chat
        start_chat()
    else:
        from app import run_api
        run_api(port=args.port, use_ngrok=not args.no_ngrok)

if __name__ == '__main__':
    main()
