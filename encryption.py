import cv2
import pickle  # To store original pixel values

def encrypt_message(image_path, message, password, output_path="encryptedImage.png"):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found! Please check the path.")
        return

    # Convert message to ASCII and add termination marker (0)
    ascii_values = [ord(char) for char in message] + [0]

    original_pixels = {}  # Dictionary to store original pixel values

    idx = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):  # BGR channels
                if idx < len(ascii_values):
                    original_pixels[(i, j, k)] = img[i, j, k]  # Save original pixel
                    img[i, j, k] = ascii_values[idx]  # Embed message
                    idx += 1
                else:
                    break
            if idx >= len(ascii_values):
                break
        if idx >= len(ascii_values):
            break

    # Save encrypted image
    cv2.imwrite(output_path, img)

    # Save original pixels and password
    with open("original_pixels.pkl", "wb") as f:
        pickle.dump(original_pixels, f)
    
    with open("password.txt", "w") as f:
        f.write(password)

    print("Encryption complete! Image saved as", output_path)

if __name__ == "__main__":
    img_path = input("Enter image path: ")
    msg = input("Enter secret message: ")
    pwd = input("Enter a passcode: ")
    encrypt_message(img_path, msg, pwd)
