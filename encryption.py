import cv2

def create_char_mappings():
    return {chr(i): i for i in range(255)}

def encrypt_message(image_path, message, password, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found or invalid path.")
        return False

    char_to_int = create_char_mappings()
    message_bytes = [char_to_int.get(char, 0) for char in message]
    password_bytes = [char_to_int.get(char, 0) for char in password]

    height, width, _ = img.shape
    required_pixels = len(password_bytes) + len(message_bytes) + 2 
    if required_pixels > height * width:
        print("Error: Message is too long for the image.")
        return False

    
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
    print(f"Message encrypted successfully in {output_path}")
    return True

if __name__ == "__main__":
    image_path = "mypic.png"
    output_path = "encryptedImage.png"

    message = input("Enter secret message: ")
    password = input("Enter a password: ")

    encrypt_message(image_path, message, password, output_path)
