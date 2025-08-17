import customtkinter as ctk
import tkinter.messagebox as messagebox
import base64
import pyttsx3
import speech_recognition as sr
import qrcode
from PIL import Image, ImageTk, UnidentifiedImageError
import os

# Morse Code Dict
MORSE_CODE_DICT = {
    'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---',
    'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
    'Z':'--..', '1':'.----', '2': '..---', '3':'...--',
    '4':'....-', '5':'.....', '6':'-....', '7':'--...',
    '8':'---..', '9':'----.', '0':'-----', ',':'--..--',
    '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-',
    '(':'-.--.', ')':'-.--.-', ' ':'/'
}

def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(c.upper(), '') for c in text)

def morse_to_text(morse):
    reversed_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return ''.join(reversed_dict.get(code, '') for code in morse.split())

def caesar_cipher(text, shift, mode):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            if mode == "encode":
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception:
        return "[Invalid Base64]"

engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def listen_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            input_box.delete("0.0", "end")
            input_box.insert("end", text)
        except Exception as e:
            input_box.insert("end", "[Error: " + str(e) + "]")

def generate_qr():
    text = output_box.get("0.0", "end").strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text to generate QR.")
        return
    img = qrcode.make(text)
    img.save("qr_code.png")
    img = Image.open("qr_code.png").resize((120, 120))
    qr_img = ImageTk.PhotoImage(img)
    qr_label.configure(image=qr_img)
    qr_label.image = qr_img

def process(mode):
    text = input_box.get("0.0", "end").strip()
    method = method_option.get()
    if method == "Caesar":
        output = caesar_cipher(text, 3, mode)
    elif method == "Base64":
        output = base64_encode(text) if mode == "encode" else base64_decode(text)
    elif method == "Morse":
        output = text_to_morse(text) if mode == "encode" else morse_to_text(text)
    else:
        output = "[Unsupported Method]"
    output_box.delete("0.0", "end")
    output_box.insert("end", output)

# THEME
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Smart Text Encoder & Decoder")
app.geometry("1000x800")

# ✅ Safe Background Image Load
try:
    bg_path = r"C:\\Users\\HP\\Downloads\\background.jpg"
    with open(bg_path, "rb") as f:
        img = Image.open(f)
        img = img.convert("RGB").resize((1000, 800))
        bg_photo = ImageTk.PhotoImage(img)
        background_label = ctk.CTkLabel(app, image=bg_photo, text="")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.lower()
except Exception as e:
    print(f"[Background Error] {e}")

# Scrollable Frame
scrollable_frame = ctk.CTkScrollableFrame(app, width=900, height=750)
scrollable_frame.pack(padx=10, pady=10, fill="both", expand=True)

title = ctk.CTkLabel(scrollable_frame, text="🔐 Smart Text Encoder & Decoder", font=("Segoe UI", 28, "bold"), text_color="#1f2937")
title.pack(pady=20)

method_option = ctk.CTkOptionMenu(scrollable_frame, values=["Caesar", "Base64", "Morse"], fg_color="#2563eb", button_color="#1d4ed8", text_color="white")
method_option.set("Caesar")
method_option.pack(pady=10)

input_label = ctk.CTkLabel(scrollable_frame, text="Enter Text:", font=("Segoe UI", 16, "bold"))
input_label.pack()
input_box = ctk.CTkTextbox(scrollable_frame, height=130, width=700, font=("Segoe UI", 14))
input_box.pack(pady=10)

output_label = ctk.CTkLabel(scrollable_frame, text="Result:", font=("Segoe UI", 16, "bold"))
output_label.pack()
output_box = ctk.CTkTextbox(scrollable_frame, height=130, width=700, font=("Segoe UI", 14))
output_box.pack(pady=10)

btn_frame = ctk.CTkFrame(scrollable_frame, fg_color="#e5e7eb")
btn_frame.pack(pady=20)

# Define button change logic
all_buttons = []
def highlight_active_button(btn):
    for b in all_buttons:
        b.configure(fg_color="#10b981")  # Green default
    btn.configure(fg_color="#3b82f6")     # Blue active

# Buttons with highlight logic
btn_encode = ctk.CTkButton(btn_frame, text="🔒 Encode", width=140, fg_color="#10b981", command=lambda: (process("encode"), highlight_active_button(btn_encode)))
btn_decode = ctk.CTkButton(btn_frame, text="🔓 Decode", width=140, fg_color="#10b981", command=lambda: (process("decode"), highlight_active_button(btn_decode)))
btn_clear = ctk.CTkButton(btn_frame, text="🧹 Clear", width=140, fg_color="#10b981", command=lambda: (input_box.delete("0.0", "end"), output_box.delete("0.0", "end"), highlight_active_button(btn_clear)))
btn_speak_input = ctk.CTkButton(btn_frame, text="🎤 Speak Input", width=140, fg_color="#10b981", command=lambda: (listen_text(), highlight_active_button(btn_speak_input)))
btn_speak_output = ctk.CTkButton(btn_frame, text="🔊 Speak Output", width=140, fg_color="#10b981", command=lambda: (speak_text(output_box.get("0.0", "end").strip()), highlight_active_button(btn_speak_output)))
btn_qr = ctk.CTkButton(btn_frame, text="🔳 Generate QR", width=140, fg_color="#10b981", command=lambda: (generate_qr(), highlight_active_button(btn_qr)))

# Place buttons and collect references
buttons = [btn_encode, btn_decode, btn_clear, btn_speak_input, btn_speak_output, btn_qr]
for i, btn in enumerate(buttons):
    btn.grid(row=i//3, column=i%3, padx=10, pady=8)
    all_buttons.append(btn)

qr_label = ctk.CTkLabel(scrollable_frame, text="")
qr_label.pack(pady=10)

def toggle_theme():
    current = ctk.get_appearance_mode()
    ctk.set_appearance_mode("Dark" if current == "Light" else "Light")

ctk.CTkButton(scrollable_frame, text="🌓 Toggle Theme", command=toggle_theme, fg_color="#6366f1", width=200).pack(pady=20)

app.mainloop()
