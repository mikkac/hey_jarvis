#!/usr/bin/env python3

import argparse
import sys

from rich.console import Console
from rich.panel import Panel

from voice import VoiceRecognizer, VoskVoiceRecognizer, VoiceAPI
from chat import init_chat_api, request_chat_response
from utils import get_args, parse_config, Config


def main(config: Config) -> None:
    init_chat_api(config.openai_api_key)

    if config.voice_api == VoiceAPI.VOSK:
        voice_recognizer: VoiceRecognizer = VoskVoiceRecognizer(
            language=config.language, device=config.device_id)

    console = Console()
    with console.status("[bold green]Listening...") as status:
        for prompt in voice_recognizer.listen():
            status.stop()
            console.print(Panel(f'[bold green]You:[/bold green] {prompt}'))
            with console.status("[bold blue]Waiting for response...", spinner="point", spinner_style="blue"):
                response = request_chat_response(prompt)
                console.print(Panel(f'[bold blue]jarvis:[/bold blue] {response}'))
            status.start()


if __name__ == "__main__":
    try:
        cmd_args: argparse.Namespace = get_args()
        if not cmd_args.config:
            from pathlib import Path
            cmd_args.config = Path.home() / ".config" / "jarvis.toml"
        print(cmd_args.config)
        config: Config = parse_config(cmd_args.config)
        main(config)
    except KeyboardInterrupt:
        print("\nDone")
        sys.exit(0)
    except Exception as e:
        print(type(e).__name__ + ": " + str(e))
        sys.exit(1)
