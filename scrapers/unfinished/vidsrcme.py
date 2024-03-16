# File yeeted from Ciarands Vidsrcme extractor

import re
import requests

from typing import Optional, Dict
import base64

class Utilities:
    @staticmethod
    def decode_src(encoded, seed) -> str:
        encoded_buffer = bytes.fromhex(encoded)
        decoded = ""
        for i in range(len(encoded_buffer)):
            decoded += chr(encoded_buffer[i] ^ ord(seed[i % len(seed)]))
        return decoded

    @staticmethod
    def hunter(h, u, n, t, e, r) -> str:
        def hunter_def(d, e, f) -> int:
            charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
            source_base = charset[0:e]
            target_base = charset[0:f]

            reversed_input = list(d)[::-1]
            result = 0

            for power, digit in enumerate(reversed_input):
                if digit in source_base:
                    result += source_base.index(digit) * e**power

            converted_result = ""
            while result > 0:
                converted_result = target_base[result % f] + converted_result
                result = (result - (result % f)) // f

            return int(converted_result) or 0
        
        i = 0
        result_str = ""
        while i < len(h):
            j = 0
            s = ""
            while h[i] != n[e]:
                s += h[i]
                i += 1

            while j < len(n):
                s = s.replace(n[j], str(j))
                j += 1

            result_str += chr(hunter_def(s, e, 10) - t)
            i += 1

        return result_str

    @staticmethod
    def decode_base64_url_safe(s: str) -> bytearray:
        standardized_input = s.replace('_', '/').replace('-', '+')
        binary_data = base64.b64decode(standardized_input)
        return bytearray(binary_data)

        
class VidsrcStreamExtractor:
    @staticmethod
    def decode_hls_url(encoded_url: str) -> str:
        def format_hls_b64(data: str) -> str:
            encoded_b64 = re.sub(r"\/@#@\/[^=\/]+==", "", data)
            if re.search(r"\/@#@\/[^=\/]+==", encoded_b64):
                return format_hls_b64(encoded_b64)
            return encoded_b64

        formatted_b64 = format_hls_b64(encoded_url[2:])
        b64_data = Utilities.decode_base64_url_safe(formatted_b64)
        return b64_data.decode("utf-8")

    def resolve_source(self, **kwargs) -> Optional[Dict]:
        req = requests.get(kwargs.get("url"), headers={"Referer": kwargs.get("referrer")})
        if req.status_code != 200:
            print(f"[VidsrcStreamExtractor] Failed to retrieve media, status code: {req.status_code}...")
            return None
        
        encoded_hls_url = re.search(r'file:"([^"]*)"', req.text)
        hls_password_url = re.search(r'var pass_path = "(.*?)";', req.text)

        if not encoded_hls_url or not hls_password_url:
            print("[VidsrcStreamExtractor] Failed to extract hls or password url...")
            return None
        
        hls_password_url = hls_password_url.group(1)
        if hls_password_url.startswith("//"):
            hls_password_url = f"https:{hls_password_url}"

        hls_url = self.decode_hls_url(encoded_hls_url.group(1))
        requests.get(hls_password_url, headers={"Referer": kwargs.get("referrer")}) # 26/01/2024 - this isnt necessary, also actual source calls this continuously

        return {
            "streams": [hls_url],
            "subtitles": {}
        }