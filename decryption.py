import cv2
import pickle

def decrypt_message(image_path, password, output_path="decryptedImage.png"):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found! Please check the path.")
        return

    # Check password
    with open("password.txt", "r") as f:
        stored_password = f.read().strip()

    if password != stored_password:
        print("YOU ARE NOT AUTHORIZED!")
        return

    message = ""
    idx = 0  # Message index

    # Extract message from image
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):  # BGR channels
                ascii_value = img[i, j, k]
                if ascii_value == 0:  # Stop at termination marker
                    print("Decrypted message:", message)
                    break
                message += chr(ascii_value)
                idx += 1
            if ascii_value == 0:
                break
        if ascii_value == 0:
            break

    # Restore original image
    with open("original_pixels.pkl", "rb") as f:
        original_pixels = pickle.load(f)

    for (i, j, k), original_value in original_pixels.items():
        img[i, j, k] = original_value  # Restore pixel

    # Save the decrypted image with the same compression as the original
    # Adjust compression to keep the file size similar (if original was PNG, save as PNG, if JPG, adjust quality)
    
    # Save as PNG (lossless)
    if output_path.lower().endswith('.png'):
        cv2.imwrite(output_path, img)
    # Save as JPEG (control quality)
    elif output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        # You can adjust quality to keep the size around 8KB
        cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # Adjust quality (0-100) as needed

    print("Original image restored! Saved as", output_path)

if __name__ == "__main__":
    img_path = input("Enter encrypted image path: ")
    pwd = input("Enter passcode for decryption: ")
    decrypt_message(img_path, pwd)
