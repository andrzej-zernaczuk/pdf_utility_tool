import os
import datetime
import tkinter as tk
from groq import Groq
from openai import OpenAI
from screeninfo import get_monitors

api_provider = os.getenv('API_PROVIDER')

if api_provider == 'GROQ':
    client = Groq(
        api_key=os.getenv('GROQ_API_KEY'),
    )
elif api_provider == 'OPENAI':
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        organization=os.getenv('OPENAI_ORG'),
        project=os.getenv('OPENAI_PROJECT'),
    )


def toggle_llm_api(llm_var):
    if llm_var.get():
        print("LLM API enabled")
    else:
        print("LLM API disabled")


def generate_suggested_filename(file_names: list[str], suggest_name: bool) -> str:
    """Generate a suggested filename for a merged PDF document based on the input file names."""
    suggested_filename = ""
    prompt = f"Based on these PDF file names: {file_names}, respond by suggesting only one concise filename for a merged PDF document. It must be without any spaces, new lines etc.. Write nothing more, just the name of the file without the .pdf extension."

    if suggest_name:
        try:
            response = client.chat.completions.create(
                model=f"{os.getenv(f'{api_provider}_MODEL_ID')}",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                # max_completion_tokens=20 #for GPT o1
                max_tokens=20 # for GPT 4o and Groq
            )
            # Extract the suggestion from the response
            # TODO: check if this works for OPENAI
            suggested_filename = response.choices[0].message.content
            suggested_filename = suggested_filename.strip()
        except Exception as e:
            print(f"An error occurred while calling the API: {e}")

    # if suggested_filename is empty, generate a default filename
    if not suggested_filename:
        suggested_filename: str = f"merged_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    return suggested_filename


def center_window(window: tk.Tk):
    # Select primary monitor
    primary_monitor = get_monitors()[0]

    # Get screen width and height
    screen_width = primary_monitor.width
    screen_height = primary_monitor.height

    # Get the monitor's x and y position
    monitor_x = primary_monitor.x
    monitor_y = primary_monitor.y

    # Get the window's current width and height
    window.update_idletasks()  # Ensure all pending events have been processed
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Calculate the position x and y to center the window
    x = monitor_x + (screen_width // 2) - (window_width // 2)
    y = monitor_y + (screen_height // 2) - (window_height // 2)

    # Set the geometry of the window (position only, no size)
    window.geometry(f'+{x}+{y}')
