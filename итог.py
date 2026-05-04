import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import requests
import json
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CurrencyConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Currency Converter")
        self.geometry("500x600")
        
        self.api_key = "ВАШ_API_КЛЮЧ"
        self.history_file = "history.json"
        self.history_data = self.load_history()

        self.label_title = ctk.CTkLabel(self, text="Конвертер валют", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        self.frame_curr = ctk.CTkFrame(self)
        self.frame_curr.pack(pady=10, padx=20, fill="x")

        self.from_curr = ctk.CTkComboBox(self.frame_curr, values=["USD", "EUR", "RUB", "GBP", "JPY"])
        self.from_curr.set("USD")
        self.from_curr.grid(row=0, column=0, padx=10, pady=10)

        self.to_curr = ctk.CTkComboBox(self.frame_curr, values=["RUB", "USD", "EUR", "GBP", "JPY"])
        self.to_curr.set("RUB")
        self.to_curr.grid(row=0, column=1, padx=10, pady=10)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Введите сумму")
        self.amount_entry.pack(pady=10, padx=20, fill="x")

        self.convert_btn = ctk.CTkButton(self, text="Конвертировать", command=self.convert)
        self.convert_btn.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="Результат: -", font=("Arial", 18))
        self.result_label.pack(pady=10)

        self.history_box = ctk.CTkTextbox(self, width=400, height=200)
        self.history_box.pack(pady=20, padx=20)
        self.update_history_display()

    def convert(self):
        amount = self.amount_entry.get()
        
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")
            return

        base = self.from_curr.get()
        target = self.to_curr.get()

        try:
            url = f"https://exchangerate-api.com{self.api_key}/pair/{base}/{target}/{amount}"
            response = requests.get(url).json()
            
            if response['result'] == 'success':
                res = response['conversion_result']
                rate = response['conversion_rate']
                self.result_label.configure(text=f"Результат: {res:.2f} {target}")
                
                entry = f"{datetime.now().strftime('%H:%M:%S')} | {amount} {base} -> {res:.2f} {target} (курс {rate})"
                self.save_to_history(entry)
            else:
                messagebox.showerror("Ошибка API", "Не удалось получить курс")
        except Exception as e:
            messagebox.showerror("Ошибка", "Проверьте интернет-соединение или API ключ")

    def save_to_history(self, entry):
        self.history_data.append(entry)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history_data, f, ensure_ascii=False)
        self.update_history_display()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def update_history_display(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", tk.END)
        for item in reversed(self.history_data):
            self.history_box.insert(tk.END, item + "\n")
        self.history_box.configure(state="disabled")

if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()