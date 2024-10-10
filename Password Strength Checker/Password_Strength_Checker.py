import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
import re
import sqlite3
import webbrowser  # لاستعمال الروابط

# إنشاء قاعدة بيانات
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS strong_passwords (password TEXT)''')
conn.commit()

def check_password_strength(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("اجعل كلمة المرور تتكون من 8 أحرف على الأقل.")
    if not re.search(r"[A-Z]", password):
        suggestions.append("أضف حرفًا كبيرًا.")
    if not re.search(r"[a-z]", password):
        suggestions.append("أضف حرفًا صغيرًا.")
    if not re.search(r"[0-9]", password):
        suggestions.append("أضف رقمًا.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append("أضف رمزًا خاصًا.")

    if suggestions:
        return "كلمة المرور ضعيفة:\n" + "\n".join(suggestions)
    
    return "كلمة المرور قوية!"

def save_password(password):
    c.execute("INSERT INTO strong_passwords (password) VALUES (?)", (password,))
    conn.commit()

def show_result(result):
    result_window = Toplevel(root)
    result_window.title("نتيجة التحقق")
    result_window.geometry("300x300")
    result_window.configure(bg="#f0f0f0")
    
    label = Label(result_window, text=result, bg="#f0f0f0", font=("Arial", 12), wraplength=250)
    label.pack(pady=20)

    button = Button(result_window, text="إغلاق", command=result_window.destroy, bg="#4CAF50", fg="white")
    button.pack(pady=10)

    # إضافة روابط GitHub وLinkedIn
    github_button = Button(result_window, text="GitHub", command=lambda: webbrowser.open("https://github.com/Nelzouki22"), bg="#24292e", fg="white")
    github_button.pack(pady=5)

    linkedin_button = Button(result_window, text="LinkedIn", command=lambda: webbrowser.open("https://www.linkedin.com/in/nadir-elzouki-40679a1a9/"), bg="#0077b5", fg="white")
    linkedin_button.pack(pady=5)

def check_password():
    password = entry.get()
    result = check_password_strength(password)
    show_result(result)
    if "قوية" in result:
        save_password(password)

# إعداد نافذة التطبيق
root = tk.Tk()
root.title("مدقق قوة كلمات المرور")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# إضافة حقل إدخال
label = tk.Label(root, text="أدخل كلمة المرور الخاصة بك:", bg="#f0f0f0", font=("Arial", 14))
label.pack(pady=10)
entry = tk.Entry(root, show="*", font=("Arial", 14), width=30)
entry.pack(pady=10)

# إضافة زر للتحقق
button = tk.Button(root, text="تحقق", command=check_password, font=("Arial", 12), bg="#4CAF50", fg="white")
button.pack(pady=20)

# تشغيل التطبيق
root.mainloop()
