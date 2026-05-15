import os
import json
import time
import shutil
import ollama

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


client = ollama.Client(
    host='http://192.168.1.19:11434'
)

INCOMING = "incoming_tasks"
PROCESSING = "processing_tasks"
COMPLETED = "completed_tasks"
FAILED = "failed_tasks"


class TaskHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".json"):
            return

        print(f"\nNew Task: {event.src_path}")

        time.sleep(1)

        try:

            with open(event.src_path, "r") as f:
                task = json.load(f)

            task_id = task["id"]
            goal = task["goal"]
            task_type = task["type"]

            processing_path = (
                f"{PROCESSING}/{task_id}.json"
            )

            shutil.move(
                event.src_path,
                processing_path
            )

            print(
                f"\nProcessing: {task_id}"
            )

            system_prompt = f"""
You are ProjSkep.

You are an autonomous orchestration system.

Task Type:
{task_type}

Rules:
- produce actionable outputs
- think structurally
- avoid generic disclaimers
- assume ProjSkep is an active AI framework
- be technical and direct
"""

            response = client.chat(
                model='qwen2.5-coder:7b',
                messages=[
                    {
                        "role":"system",
                        "content":system_prompt
                    },
                    {
                        "role":"user",
                        "content":goal
                    }
                ]
            )

            result = response[
                "message"
            ]["content"]

            output = {
                "id": task_id,
                "goal": goal,
                "result": result,
                "status": "completed"
            }

            completed_path = (
                f"{COMPLETED}/{task_id}.json"
            )

            with open(
                completed_path,
                "w"
            ) as f:

                json.dump(
                    output,
                    f,
                    indent=2
                )

            os.remove(
                processing_path
            )

            print(
                f"\nCompleted: {task_id}"
            )

        except Exception as e:

            print("\nERROR:\n")
            print(e)

            failed_path = (
                f"{FAILED}/failed_task.json"
            )

            if os.path.exists(
                event.src_path
            ):

                shutil.move(
                    event.src_path,
                    failed_path
                )


observer = Observer()

observer.schedule(
    TaskHandler(),
    INCOMING,
    recursive=False
)

observer.start()

print("\nProjSkep Orchestrator Running...")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping Orchestrator...")

    observer.stop()

observer.join()
