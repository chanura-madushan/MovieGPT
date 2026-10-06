import tkinter as tk
from tkinter import font
import threading
import ollama

from recommender import recommend, find_title


# ==================================================
# COLORS
# ==================================================

BACKGROUND = "#0b0b0c"
SIDEBAR = "#111113"
CHAT_BACKGROUND = "#0b0b0c"

WHITE = "#f5f5f5"
SILVER = "#a1a1aa"
LIGHT_SILVER = "#d4d4d8"

BORDER = "#27272a"
INPUT_BACKGROUND = "#18181b"

FIRE_ORANGE = "#ff5a1f"
FIRE_ORANGE_DARK = "#e64a17"

USER_BUBBLE = "#242426"
ASSISTANT_BUBBLE = "#111113"


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()

root.title("MovieGPT")

root.geometry("1200x750")

root.minsize(900, 600)

root.configure(
    bg=BACKGROUND
)


# ==================================================
# FONTS
# ==================================================

available_fonts = font.families()

if "SF Pro Display" in available_fonts:

    MAIN_FONT = "SF Pro Display"

elif "SF Pro Text" in available_fonts:

    MAIN_FONT = "SF Pro Text"

elif "Helvetica Neue" in available_fonts:

    MAIN_FONT = "Helvetica Neue"

else:

    MAIN_FONT = "Segoe UI"


# ==================================================
# VARIABLES
# ==================================================

conversation_started = False


# ==================================================
# FUNCTIONS
# ==================================================

def clear_chat():

    global conversation_started

    conversation_started = False

    for widget in chat_frame.winfo_children():

        widget.destroy()

    show_welcome()


def show_welcome():

    welcome_frame = tk.Frame(
        chat_frame,
        bg=CHAT_BACKGROUND
    )

    welcome_frame.pack(
        expand=True
    )

    title = tk.Label(
        welcome_frame,
        text="How can I help you today?",
        bg=CHAT_BACKGROUND,
        fg=WHITE,
        font=(MAIN_FONT, 30, "bold")
    )

    title.pack(
        pady=(180, 12)
    )

    line = tk.Frame(
        welcome_frame,
        bg=FIRE_ORANGE,
        height=3,
        width=40
    )

    line.pack(
        pady=8
    )

    subtitle = tk.Label(
        welcome_frame,
        text=(
            "Discover movies and TV shows "
            "based on what you already enjoy."
        ),
        bg=CHAT_BACKGROUND,
        fg=SILVER,
        font=(MAIN_FONT, 15)
    )

    subtitle.pack(
        pady=12
    )


def add_user_message(message):

    message_frame = tk.Frame(
        chat_frame,
        bg=CHAT_BACKGROUND
    )

    message_frame.pack(
        fill="x",
        padx=35,
        pady=12
    )

    bubble = tk.Label(
        message_frame,
        text=message,
        bg=USER_BUBBLE,
        fg=WHITE,
        font=(MAIN_FONT, 14),
        padx=16,
        pady=11,
        justify="left",
        wraplength=650
    )

    bubble.pack(
        anchor="e"
    )


def add_assistant_message(message):

    message_frame = tk.Frame(
        chat_frame,
        bg=CHAT_BACKGROUND
    )

    message_frame.pack(
        fill="x",
        padx=35,
        pady=12
    )

    name = tk.Label(
        message_frame,
        text="MovieGPT",
        bg=CHAT_BACKGROUND,
        fg=FIRE_ORANGE,
        font=(MAIN_FONT, 13, "bold")
    )

    name.pack(
        anchor="w"
    )

    response = tk.Label(
        message_frame,
        text=message,
        bg=CHAT_BACKGROUND,
        fg=LIGHT_SILVER,
        font=(MAIN_FONT, 14),
        justify="left",
        anchor="w",
        wraplength=800
    )

    response.pack(
        anchor="w",
        pady=(5, 0)
    )


def show_thinking():

    global thinking_label

    thinking_label = tk.Label(
        chat_frame,
        text="Thinking...",
        bg=CHAT_BACKGROUND,
        fg=SILVER,
        font=(MAIN_FONT, 13, "italic")
    )

    thinking_label.pack(
        fill="x",
        padx=35,
        pady=10
    )

    chat_canvas.update_idletasks()

    chat_canvas.yview_moveto(1)


def remove_thinking():

    if thinking_label:

        thinking_label.destroy()


def get_intent(user_input):

    response = ollama.chat(

        model="qwen2.5:3b",

        messages=[

            {
                "role": "system",

                "content": """
You are the intent classifier for MovieGPT.

Classify the user's message into exactly ONE category:

GREETING
RECOMMENDATION
HELP
GOODBYE

Examples:

hello -> GREETING
hi -> GREETING
hey -> GREETING
good morning -> GREETING

I want something like Blood & Water -> RECOMMENDATION
recommend me a movie -> RECOMMENDATION
what should I watch -> RECOMMENDATION
find something similar to Stranger Things -> RECOMMENDATION

help -> HELP
what can you do -> HELP
how does this work -> HELP

bye -> GOODBYE
goodbye -> GOODBYE
see you later -> GOODBYE

Return ONLY the category name.
"""
            },

            {
                "role": "user",
                "content": user_input
            }

        ]
    )

    return response["message"]["content"].strip().upper()


def process_message(user_input):

    try:

        intent = get_intent(user_input)

        # ------------------------------------------
        # GREETING
        # ------------------------------------------

        if intent == "GREETING":

            response = (
                "Hello. Tell me a movie or TV show you like "
                "and I will find similar titles."
            )


        # ------------------------------------------
        # HELP
        # ------------------------------------------

        elif intent == "HELP":

            response = (
                "I can recommend movies and TV shows from "
                "my Netflix dataset. Tell me about a movie "
                "or show you enjoyed and I will find similar titles."
            )


        # ------------------------------------------
        # GOODBYE
        # ------------------------------------------

        elif intent == "GOODBYE":

            response = (
                "Goodbye. Come back whenever you need "
                "a recommendation."
            )


        # ------------------------------------------
        # RECOMMENDATION
        # ------------------------------------------

        elif intent == "RECOMMENDATION":

            title = find_title(user_input)

            if title:

                recommendations = recommend(title)

                response = (
                    f"Because you like {title}, "
                    "you might also like:\n\n"
                )

                for i, movie in enumerate(
                    recommendations,
                    1
                ):

                    response += (
                        f"{i}. {movie}\n"
                    )

            else:

                response = (
                    "I could not find that movie or TV show "
                    "in my dataset.\n\n"
                    "Try mentioning a specific movie or show "
                    "title."
                )


        # ------------------------------------------
        # UNKNOWN
        # ------------------------------------------

        else:

            response = (
                "I am not sure what you mean. "
                "Try asking for a movie recommendation."
            )


        root.after(
            0,
            finish_response,
            response
        )

    except Exception as error:

        root.after(
            0,
            finish_response,
            f"Something went wrong:\n{error}"
        )


def finish_response(response):

    remove_thinking()

    add_assistant_message(
        response
    )

    enable_input()

    scroll_to_bottom()


def send_message(event=None):

    global conversation_started

    user_input = input_box.get(
        "1.0",
        "end"
    ).strip()

    if not user_input:

        return

    if not conversation_started:

        conversation_started = True

        for widget in chat_frame.winfo_children():

            widget.destroy()


    input_box.delete(
        "1.0",
        "end"
    )

    add_user_message(
        user_input
    )

    disable_input()

    show_thinking()

    scroll_to_bottom()

    thread = threading.Thread(
        target=process_message,
        args=(user_input,),
        daemon=True
    )

    thread.start()


def disable_input():

    send_button.config(
        state="disabled"
    )

    input_box.config(
        state="disabled"
    )


def enable_input():

    send_button.config(
        state="normal"
    )

    input_box.config(
        state="normal"
    )

    input_box.focus_set()


def scroll_to_bottom():

    root.after(
        50,
        lambda: chat_canvas.yview_moveto(1)
    )


# ==================================================
# SIDEBAR
# ==================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=245
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(
    False
)


# Logo

logo = tk.Label(
    sidebar,
    text="MovieGPT",
    bg=SIDEBAR,
    fg=WHITE,
    font=(MAIN_FONT, 19, "bold")
)

logo.pack(
    anchor="w",
    padx=22,
    pady=(22, 25)
)


# Orange line

logo_line = tk.Frame(
    sidebar,
    bg=FIRE_ORANGE,
    height=2,
    width=35
)

logo_line.pack(
    anchor="w",
    padx=22,
    pady=(0, 20)
)


# New chat button

new_chat_button = tk.Button(
    sidebar,
    text="+  New chat",
    command=clear_chat,
    bg=INPUT_BACKGROUND,
    fg=WHITE,
    activebackground="#242426",
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    font=(MAIN_FONT, 13),
    cursor="hand2",
    padx=12,
    pady=10
)

new_chat_button.pack(
    fill="x",
    padx=15
)


# Recent section

recent_label = tk.Label(
    sidebar,
    text="RECENT",
    bg=SIDEBAR,
    fg="#71717a",
    font=(MAIN_FONT, 10, "bold")
)

recent_label.pack(
    anchor="w",
    padx=22,
    pady=(35, 8)
)


recent_text = tk.Label(
    sidebar,
    text="No conversations yet.",
    bg=SIDEBAR,
    fg="#71717a",
    font=(MAIN_FONT, 12),
    wraplength=190,
    justify="left"
)

recent_text.pack(
    anchor="w",
    padx=22
)


# System section

system_label = tk.Label(
    sidebar,
    text="SYSTEM",
    bg=SIDEBAR,
    fg="#71717a",
    font=(MAIN_FONT, 10, "bold")
)

system_label.pack(
    anchor="w",
    padx=22,
    pady=(35, 10)
)


model_text = tk.Label(
    sidebar,
    text="Model: Qwen 2.5 3B",
    bg=SIDEBAR,
    fg=SILVER,
    font=(MAIN_FONT, 11)
)

model_text.pack(
    anchor="w",
    padx=22,
    pady=2
)


engine_text = tk.Label(
    sidebar,
    text="Engine: TF-IDF",
    bg=SIDEBAR,
    fg=SILVER,
    font=(MAIN_FONT, 11)
)

engine_text.pack(
    anchor="w",
    padx=22,
    pady=2
)


# ==================================================
# MAIN AREA
# ==================================================

main_area = tk.Frame(
    root,
    bg=CHAT_BACKGROUND
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ==================================================
# HEADER
# ==================================================

header = tk.Frame(
    main_area,
    bg=CHAT_BACKGROUND,
    height=60
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


header_title = tk.Label(
    header,
    text="MovieGPT",
    bg=CHAT_BACKGROUND,
    fg=WHITE,
    font=(MAIN_FONT, 17, "bold")
)

header_title.pack(
    side="left",
    padx=25,
    pady=17
)


status_label = tk.Label(
    header,
    text="Qwen 2.5 3B",
    bg=CHAT_BACKGROUND,
    fg=SILVER,
    font=(MAIN_FONT, 10)
)

status_label.pack(
    side="right",
    padx=25
)


# Header border

header_border = tk.Frame(
    main_area,
    bg=BORDER,
    height=1
)

header_border.pack(
    fill="x"
)


# ==================================================
# CHAT AREA
# ==================================================

chat_container = tk.Frame(
    main_area,
    bg=CHAT_BACKGROUND
)

chat_container.pack(
    fill="both",
    expand=True
)


chat_canvas = tk.Canvas(
    chat_container,
    bg=CHAT_BACKGROUND,
    highlightthickness=0
)

chat_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = tk.Scrollbar(
    chat_container,
    orient="vertical",
    command=chat_canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


chat_canvas.configure(
    yscrollcommand=scrollbar.set
)


chat_frame = tk.Frame(
    chat_canvas,
    bg=CHAT_BACKGROUND
)


chat_window = chat_canvas.create_window(
    (0, 0),
    window=chat_frame,
    anchor="nw"
)


def update_scroll_region(event=None):

    chat_canvas.configure(
        scrollregion=chat_canvas.bbox("all")
    )


chat_frame.bind(
    "<Configure>",
    update_scroll_region
)


def resize_chat_frame(event):

    chat_canvas.itemconfig(
        chat_window,
        width=event.width
    )


chat_canvas.bind(
    "<Configure>",
    resize_chat_frame
)


# ==================================================
# INPUT AREA
# ==================================================

input_area = tk.Frame(
    main_area,
    bg=CHAT_BACKGROUND,
    height=95
)

input_area.pack(
    fill="x"
)

input_area.pack_propagate(
    False
)


input_frame = tk.Frame(
    input_area,
    bg=INPUT_BACKGROUND,
    highlightbackground="#3f3f46",
    highlightthickness=1
)

input_frame.pack(
    fill="x",
    padx=35,
    pady=18
)


input_box = tk.Text(
    input_frame,
    height=1,
    bg=INPUT_BACKGROUND,
    fg=WHITE,
    insertbackground=FIRE_ORANGE,
    selectbackground=FIRE_ORANGE,
    selectforeground=WHITE,
    relief="flat",
    bd=0,
    wrap="word",
    font=(MAIN_FONT, 14),
    padx=12,
    pady=10
)

input_box.pack(
    side="left",
    fill="both",
    expand=True
)


send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    bg=FIRE_ORANGE,
    fg=WHITE,
    activebackground=FIRE_ORANGE_DARK,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    font=(MAIN_FONT, 11, "bold"),
    cursor="hand2",
    padx=18,
    pady=8
)

send_button.pack(
    side="right",
    padx=8,
    pady=7
)


# ==================================================
# ENTER KEY
# ==================================================

input_box.bind(
    "<Return>",
    send_message
)


# ==================================================
# INITIAL SCREEN
# ==================================================

show_welcome()

input_box.focus_set()


# ==================================================
# START APPLICATION
# ==================================================

root.mainloop()