import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

def create_char_mappings():
    """Create character-to-integer and integer-to-character mappings."""
    return {chr(i): i for i in range(255)}, {i: chr(i) for i in range(255)}

def encrypt_message():
    """Encrypts a message into an image."""
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("PNG Files", "*.png")])
    if not image_path:
        return

    message = entry_message.get()
    password = entry_password.get()
    output_path = "encryptedImage.png"

    if not message or not password:
        messagebox.showerror("Error", "Message and password cannot be empty!")
        return

    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image selected.")
        return

    char_to_int, _ = create_char_mappings()
    message_bytes = [char_to_int.get(char, 0) for char in message]
    password_bytes = [char_to_int.get(char, 0) for char in password]

    height, width, _ = img.shape
    required_pixels = len(password_bytes) + len(message_bytes) + 2  # +2 for password length & message length

    if required_pixels > height * width:
        messagebox.showerror("Error", "Message is too long for the image.")
        return


    img[0, 0, 0] = len(password_bytes)


    idx = 1
    for value in password_bytes:
        img[idx // width, idx % width, 0] = value
        idx += 1

 
    img[idx // width, idx % width, 0] = len(message_bytes)
    idx += 1


    for value in message_bytes:
        img[idx // width, idx % width, 0] = value
        idx += 1

    cv2.imwrite(output_path, img)
    messagebox.showinfo("Success", f"Message encrypted successfully!\nSaved as: {output_path}")

def decrypt_message():
    """Decrypts a message from an image."""
    image_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("PNG Files", "*.png")])
    if not image_path:
        return

    entered_password = entry_password.get()
    if not entered_password:
        messagebox.showerror("Error", "Password cannot be empty!")
        return

    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Invalid image selected.")
        return

    _, int_to_char = create_char_mappings()
    height, width, _ = img.shape


    password_length = img[0, 0, 0]

    stored_password = ""
    idx = 1
    for _ in range(password_length):
        stored_password += int_to_char.get(img[idx // width, idx % width, 0], "?")
        idx += 1


    if entered_password != stored_password:
        messagebox.showerror("Error", "Incorrect password!")
        return


    message_length = img[idx // width, idx % width, 0]
    idx += 1


    decrypted_message = ""
    for _ in range(message_length):
        if idx >= height * width:
            break
        decrypted_message += int_to_char.get(img[idx // width, idx % width, 0], "?")
        idx += 1

    messagebox.showinfo("Decrypted Message", f"Decrypted Message:\n{decrypted_message}")


root = tk.Tk()
root.title("Steganography Tool")

tk.Label(root, text="Secret Message:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)


entry_message = tk.Entry(root, width=40)
entry_message.grid(row=0, column=1, padx=10, pady=5)

entry_password = tk.Entry(root, width=40, show="*")  
entry_password.grid(row=1, column=1, padx=10, pady=5)


btn_encrypt = tk.Button(root, text="Encrypt Message", command=encrypt_message, bg="lightblue")
btn_encrypt.grid(row=2, column=0, padx=10, pady=10)

btn_decrypt = tk.Button(root, text="Decrypt Message", command=decrypt_message, bg="lightgreen")
btn_decrypt.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
