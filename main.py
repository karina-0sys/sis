import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

FAVORITES_FILE = 'favorites.json'

def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=2)

def search_user():
    username = entry_search.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        response.raise_for_status()
        user_data = response.json()
        display_user(user_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Пользователь не найден или ошибка сети: {e}")

def display_user(user_data):
    listbox_results.delete(0, tk.END)
    listbox_results.insert(tk.END, f"Логин: {user_data.get('login')}")
    listbox_results.insert(tk.END, f"Имя: {user_data.get('name')}")
    listbox_results.insert(tk.END, f"URL: {user_data.get('html_url')}")
    listbox_results.insert(tk.END, f"Подписчики: {user_data.get('followers')}")
    current_user = user_data.get('login')

    btn_fav = ttk.Button(frame_results, text="Добавить в избранное", 
                         command=lambda: add_to_favorites(current_user))
    btn_fav.pack(pady=5)

def add_to_favorites(username):
    favorites = load_favorites()
    if username not in favorites:
        favorites.append(username)
        save_favorites(favorites)
        messagebox.showinfo("Успех", f"Пользователь {username} добавлен в избранное!")
    else:
        messagebox.showinfo("Информация", "Пользователь уже в избранном.")

root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("400x500")

frame_search = ttk.Frame(root)
frame_search.pack(pady=10)

label_search = ttk.Label(frame_search, text="Введите логин пользователя GitHub:")
label_search.pack(side=tk.LEFT)

entry_search = ttk.Entry(frame_search, width=30)
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = ttk.Button(frame_search, text="Поиск", command=search_user)
btn_search.pack(side=tk.LEFT)

frame_results = ttk.Frame(root)
frame_results.pack(pady=10, fill=tk.BOTH, expand=True)

listbox_results = tk.Listbox(frame_results, width=50, height=15)
listbox_results.pack(pady=5)

root.mainloop()
