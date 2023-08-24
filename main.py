import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import speed_method as speed
import time_method as time



def calculate_speed():
    # Получите значения из полей ввода и выполните расчеты для Метода 1 (Интервалы скоростей)
    Vn = float(entry_vn.get().replace(',', '.')) if entry_vn.get() else 0
    i = float(entry_i.get().replace(',', '.')) if entry_i.get() else 0
    Q = float(entry_q.get().replace(',', '.')) if entry_q.get() else 0
    P = float(entry_p.get().replace(',', '.')) if entry_p.get() else 0
    u = float(entry_u.get().replace(',', '.')) if entry_u.get() else 0
    thetachr = float(entry_theta_chr.get().replace(',', '.')) if entry_theta_chr.get() else 0
    thetakr = float(entry_theta_kkr.get().replace(',', '.')) if entry_theta_kkr.get() else 0
    a = float(entry_a.get().replace(',', '.')) if entry_a.get() else 0
    c = float(entry_c.get().replace(',', '.')) if entry_c.get() else 0
    A = float(entry_A.get().replace(',', '.')) if entry_A.get() else 0
    B = float(entry_B.get().replace(',', '.')) if entry_B.get() else 0
    C = float(entry_C.get().replace(',', '.')) if entry_C.get() else 0

    #Тест параметры
    Vn = 60  # Начальная скорость в км/ч
    i = -5.4  # Наклон спуска в %
    Q = 2100  # Вес sostава в тоннах
    P = 120  # Вес локомотива в тоннах
    u = 123.2  # Единичное ускорение поезда в м/с^2
    thetachr = 0.242
    thetakr = 0.054
    a = 7
    c = 10
    A = 0.889
    B = 0.00629
    C = 0.0001572

    try:
        result_list = speed.calculate_intervals(Vn, i, Q, P, u, thetachr, thetakr, a, c, A, B, C)
        show_table_and_plot(result_list, method=1)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def calculate_time():
    # Получите значения из полей ввода и выполните расчеты для Метода 2 (Временные интервалы)
    Vn = float(entry_vn_2.get().replace(',', '.')) if entry_vn_2.get() else 0.0
    i = float(entry_i_2.get().replace(',', '.')) if entry_i_2.get() else 0.0
    Q = float(entry_q_2.get().replace(',', '.')) if entry_q_2.get() else 0.0
    P = float(entry_p_2.get().replace(',', '.')) if entry_p_2.get() else 0.0
    u = float(entry_u_2.get().replace(',', '.')) if entry_u_2.get() else 0.0
    thetachr = float(entry_theta_chr_2.get().replace(',', '.')) if entry_theta_chr_2.get() else 0.0
    thetakr = float(entry_theta_kkr_2.get().replace(',', '.')) if entry_theta_kkr_2.get() else 0.0
    A = float(entry_A_2.get().replace(',', '.')) if entry_A_2.get() else 0.0
    B = float(entry_B_2.get().replace(',', '.')) if entry_B_2.get() else 0.0
    C = float(entry_C_2.get().replace(',', '.')) if entry_C_2.get() else 0.0
    l = float(entry_length.get().replace(',', '.')) if entry_length.get() else 0.0

    #Тест параметры
    Vn = 60  # Начальная скорость в км/ч
    i = -2.9  # Наклон спуска в %
    Q = 4200  # Вес sostава в тоннах
    P = 120  # Вес локомотива в тоннах
    u = 123.2  # Единичное ускорение поезда в м/с^2
    l = 950  # Длина поезда в метрах
    thetachr = 0.212
    thetakr = 0.074
    A = 0.889
    B = 0.00629
    C = 0.0001572


    # Выполните расчеты для Метода 2 с использованием введенных значений
    try:
        result_list = time.calculate_braking_intervals(Vn, i, Q, P, u, l, thetachr, thetakr, A, B, C)
        show_table_and_plot(result_list, method=2)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))



def show_table_and_plot(data, method):
    # Отобразите результаты в виде таблицы
    table_window = tk.Toplevel(root)
    table_window.title("Таблица результатов")
    table_window.geometry("1920x1080")  # Задаем размер окна таблицы

    table_text = tk.Text(table_window, wrap=tk.NONE, bg="white", font=("Courier", 10))
    table_text.pack(expand=tk.YES, fill=tk.BOTH)

    # Добавим проkrутку по обеим осям
    scroll_y = tk.Scrollbar(table_window, command=table_text.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    table_text.config(yscrollcommand=scroll_y.set)

    scroll_x = tk.Scrollbar(table_window, command=table_text.xview, orient=tk.HORIZONTAL)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    table_text.config(xscrollcommand=scroll_x.set)

    # Выведем таблицу результатов
    df = pd.DataFrame(data)
    table_text.insert(tk.END, df.to_string())

    if method == 1:
        x_column = 'dΣS'
        y_column = 'Vк'
        data.plot(x=x_column, y=y_column, kind='line', marker='o', linestyle='-')
        plt.xlabel('dΣS')
        plt.ylabel('Vк')
        plt.title('График зависимости скорости от пройденного расстояния')
        plt.show()
    elif method == 2:
        x_column = 'dΣS'
        y_column = 'Vк'
        data.plot(x=x_column, y=y_column, kind='line', marker='o', linestyle='-')
        plt.xlabel('dΣS')
        plt.ylabel('Vк')
        plt.title('График зависимости скорости от пройденного расстояния')
        plt.show(block=False)
        x_column = '№ интервала'
        y_column = 'ϑсост'
        data[x_column] = data[x_column].map(lambda x: int(x) * 3)
        data.plot(x=x_column, y=y_column, kind='line', marker='o', linestyle='-')
        plt.xlabel('dΣt')
        plt.ylabel('ϑсост')
        plt.title('График наполнения тормозных цилиндров')
        plt.show(block=False)


# Создайте основное окно
root = tk.Tk()
root.title("Тормозные расчёты")
root.resizable(False, False)

# Создайте вкладки
tab_control = ttk.Notebook(root)

# Вкладка для Метода 1 (Интервалы скоростей)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Метод интервалов скорости")

# Создайте поля ввода для первой вкладки
label_vn = tk.Label(tab1, text="Начальная скорость, км/ч (Vн):")
label_vn.grid(row=0, column=0, padx=5, pady=5)
entry_vn = ttk.Entry(tab1)
entry_vn.grid(row=0, column=1, padx=5, pady=5)

label_i = tk.Label(tab1, text="Уклон, % (i):")
label_i.grid(row=1, column=0, padx=5, pady=5)
entry_i = ttk.Entry(tab1)
entry_i.grid(row=1, column=1, padx=5, pady=5)

label_q = tk.Label(tab1, text="Масса состава, т (Q):")
label_q.grid(row=2, column=0, padx=5, pady=5)
entry_q = ttk.Entry(tab1)
entry_q.grid(row=2, column=1, padx=5, pady=5)

label_p = tk.Label(tab1, text="Масса локомотива, т (P):")
label_p.grid(row=3, column=0, padx=5, pady=5)
entry_p = ttk.Entry(tab1)
entry_p.grid(row=3, column=1, padx=5, pady=5)

label_u = tk.Label(tab1, text="Единичное ускорение поезда (ξ):")
label_u.grid(row=4, column=0, padx=5, pady=5)
entry_u = ttk.Entry(tab1)
entry_u.grid(row=4, column=1, padx=5, pady=5)

label_theta_chr = tk.Label(tab1, text="ϑчр:")
label_theta_chr.grid(row=5, column=0, padx=5, pady=5)
entry_theta_chr = ttk.Entry(tab1)
entry_theta_chr.grid(row=5, column=1, padx=5, pady=5)

label_theta_kkr = tk.Label(tab1, text="ϑкр:")
label_theta_kkr.grid(row=6, column=0, padx=5, pady=5)
entry_theta_kkr = ttk.Entry(tab1)
entry_theta_kkr.grid(row=6, column=1, padx=5, pady=5)

label_a = tk.Label(tab1, text="Коэффициент a для времени подготовки тормозов:", wraplength=200)
label_a.grid(row=7, column=0, padx=5, pady=5)
entry_a = ttk.Entry(tab1)
entry_a.grid(row=7, column=1, padx=5, pady=5)

label_c = tk.Label(tab1, text="Коэффициент c для времени подготовки тормозов:", wraplength=200)
label_c.grid(row=8, column=0, padx=5, pady=5)
entry_c = ttk.Entry(tab1)
entry_c.grid(row=8, column=1, padx=5, pady=5)

label_A = tk.Label(tab1, text="Коэффициент A для удельного сопротивления состава:", wraplength=200)
label_A.grid(row=9, column=0, padx=5, pady=5)
entry_A = ttk.Entry(tab1)
entry_A.grid(row=9, column=1, padx=5, pady=5)

label_B = tk.Label(tab1, text="Коэффициент B для удельного сопротивления состава:", wraplength=200)
label_B.grid(row=10, column=0, padx=5, pady=5)
entry_B = ttk.Entry(tab1)
entry_B.grid(row=10, column=1, padx=5, pady=5)

label_C = tk.Label(tab1, text="Коэффициент C для удельного сопротивления состава:", wraplength=200)
label_C.grid(row=11, column=0, padx=5, pady=5)
entry_C = ttk.Entry(tab1)
entry_C.grid(row=11, column=1, padx=5, pady=5)

# Кнопка для расчета Метода 1
calculate_button1 = tk.Button(tab1, text="Рассчитать", command=calculate_speed)
calculate_button1.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

# Вкладка для Метода 2 (Временные интервалы)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text="Метод интервалов времени")

# Создайте поля ввода для второй вкладки
label_vn_2 = tk.Label(tab2, text="Начальная скорость, км/ч (Vн):")
label_vn_2.grid(row=0, column=0, padx=5, pady=5)
entry_vn_2 = ttk.Entry(tab2)
entry_vn_2.grid(row=0, column=1, padx=5, pady=5)

label_i_2 = tk.Label(tab2, text="Уклон, % (i):")
label_i_2.grid(row=1, column=0, padx=5, pady=5)
entry_i_2 = ttk.Entry(tab2)
entry_i_2.grid(row=1, column=1, padx=5, pady=5)

label_q_2 = tk.Label(tab2, text="Масса состава, т (Q):")
label_q_2.grid(row=2, column=0, padx=5, pady=5)
entry_q_2 = ttk.Entry(tab2)
entry_q_2.grid(row=2, column=1, padx=5, pady=5)

label_p_2 = tk.Label(tab2, text="Масса локомотива, т (P):")
label_p_2.grid(row=3, column=0, padx=5, pady=5)
entry_p_2 = ttk.Entry(tab2)
entry_p_2.grid(row=3, column=1, padx=5, pady=5)

label_u_2 = tk.Label(tab2, text="Единичное ускорение поезда (ξ):")
label_u_2.grid(row=4, column=0, padx=5, pady=5)
entry_u_2 = ttk.Entry(tab2)
entry_u_2.grid(row=4, column=1, padx=5, pady=5)

label_theta_chr_2 = tk.Label(tab2, text="ϑчр:")
label_theta_chr_2.grid(row=5, column=0, padx=5, pady=5)
entry_theta_chr_2 = ttk.Entry(tab2)
entry_theta_chr_2.grid(row=5, column=1, padx=5, pady=5)

label_theta_kkr_2 = tk.Label(tab2, text="ϑкр:")
label_theta_kkr_2.grid(row=6, column=0, padx=5, pady=5)
entry_theta_kkr_2 = ttk.Entry(tab2)
entry_theta_kkr_2.grid(row=6, column=1, padx=5, pady=5)

label_A_2 = tk.Label(tab2, text="Коэффициент A для удельного сопротивления состава:", wraplength=200)
label_A_2.grid(row=9, column=0, padx=5, pady=5)
entry_A_2 = ttk.Entry(tab2)
entry_A_2.grid(row=9, column=1, padx=5, pady=5)

label_B_2 = tk.Label(tab2, text="Коэффициент B для удельного сопротивления состава:", wraplength=200)
label_B_2.grid(row=10, column=0, padx=5, pady=5)
entry_B_2 = ttk.Entry(tab2)
entry_B_2.grid(row=10, column=1, padx=5, pady=5)

label_C_2 = tk.Label(tab2, text="Коэффициент C для удельного сопротивления состава:", wraplength=200)
label_C_2.grid(row=11, column=0, padx=5, pady=5)
entry_C_2 = ttk.Entry(tab2)
entry_C_2.grid(row=11, column=1, padx=5, pady=5)

label_length = tk.Label(tab2, text="Длина поезда, м (l):")
label_length.grid(row=12, column=0, padx=5, pady=5)
entry_length = ttk.Entry(tab2)
entry_length.grid(row=12, column=1, padx=5, pady=5)

# Кнопка для расчета Метода 2
calculate_button2 = tk.Button(tab2, text="Рассчитать", command=calculate_time)
calculate_button2.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

tab_control.pack(expand=1, fill="both")

root.mainloop()
