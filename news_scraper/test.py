import clr
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(current_dir, 'custom_selenium.dll')

if os.path.exists(dll_path):
    print(f"Файл знайдено: {dll_path}")
else:
    print("DLL файл не знайдено!")

clr.AddReference(dll_path)

