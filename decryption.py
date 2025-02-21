import cv2

def create_char_mappings():
    return {i: chr(i) for i in range(255)}

def decrypt_message(image_path, entered_password):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found or invalid path.")
        return

    int_to_char = create_char_mappings()
    height, width, _ = img.shape

   
    password_length = img[0, 0, 0]

    
    stored_password = ""
    idx = 1
    for _ in range(password_length):
        stored_password += int_to_char.get(img[idx // width, idx % width, 0], "?")
        idx += 1

    
    if entered_password != stored_password:
        print("YOU ARE NOT AUTHORIZED!")
        return

    
    message_length = img[idx // width, idx % width, 0]
    idx += 1

   
    decrypted_message = ""
    for _ in range(message_length):
        if idx >= height * width:  
            break
        decrypted_message += int_to_char.get(img[idx // width, idx % width, 0], "?")
        idx += 1

    print("Decrypted message:", decrypted_message.strip())

if __name__ == "__main__":
    image_path = "encryptedImage.png"
    entered_password = input("Enter password for decryption: ")

    decrypt_message(image_path, entered_password)
