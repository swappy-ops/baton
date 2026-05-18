import time
import ollama

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


client = ollama.Client(
    host='http://192.168.1.19:11434'
)

WATCH_FOLDER = "tasks"


class TaskHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        print(f"\nNew task file: {event.src_path}")

        # wait for file write completion
        time.sleep(1)

        with open(event.src_path, "r") as f:
            task = f.read()

        response = client.chat(
            model='qwen2.5-coder:7b',
            messages=[
                {
                    "role": "system",
                    "content": """
You are Baton.

Baton is an autonomous AI orchestration framework.

Your role:
- analyze tasks
- generate actionable outputs
- think like a systems architect
- avoid generic disclaimers
- do not claim ignorance about Baton
- assume Baton is the active system being developed

Be direct, structured, and technical.
"""
                },
                {
                    "role": "user",
                    "content": task
                }
            ]
        )

        print("\nBaton Response:\n")

        print(
            response["message"]["content"]
        )


observer = Observer()

observer.schedule(
    TaskHandler(),
    WATCH_FOLDER,
    recursive=False
)

observer.start()

print(f"Watching folder: {WATCH_FOLDER}")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping watcher...")

    observer.stop()

observer.join()
