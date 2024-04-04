from PIL import Image
import requests
import base64
import io

class MegaCloud:
    def __init__(self):
        self.name = "MegaCloud"
        self.main_url = "https://megacloud.tv"
        self.lucky_image_url = f"{self.main_url}/images/lucky_animal/icon.png"

    def init(self):
        try:
            image_response = requests.get(self.lucky_image_url)
            if image_response.status_code == 200:
                image = Image.open(io.BytesIO(image_response.content))
                key = self.extract_real_key(image)
              
                return list(key)
            else:
                print("Failed to fetch image. Status code:", image_response.status_code)
                return None
        except Exception as e:
            print("Error:", e)
            return None

    def extract_real_key(self, image):
        width, height = image.size
        pixel_data = []

        for y in range(height):
            for x in range(width):
                pixel = image.getpixel((x, y))
                pixel_data.extend([int(channel) for channel in pixel])

        encoded_byte_array = self.compute_key_from_image(pixel_data)
        return encoded_byte_array

    def compute_key_from_image(self, image_data):
        image_chunks = ""
        image_chunks_to_char = ""
        image_chunks_to_char_to_hex = []

        for i in range(image_data[3] * 8):
            image_chunks += str(image_data[(i + 1) * 4 + 3] % 2)

        image_chunks = image_chunks[:len(image_chunks) - len(image_chunks) % 2]
        for i in range(0, len(image_chunks), 8):
            image_chunks_to_char += chr(int(image_chunks[i:i + 8], 2))

        for i in range(0, len(image_chunks_to_char) - 1, 2):
            image_chunks_to_char_to_hex.append(int(image_chunks_to_char[i:i + 2], 16))

        key = bytes(image_chunks_to_char_to_hex)
        return key

# Usage
# key_extractor = MegaCloud()
# keys = key_extractor.init()
# print(keys)
