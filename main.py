import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox, scrolledtext
import os
import readOF
import config_for_interface
import fact
import file_transfer


def button_click(folder_id):
    folder_path = filedialog.askdirectory()
    if folder_id == 1:
        if folder_path:
            config_for_interface.path_to_to_folder = folder_path
            button1.configure(bg="#118844")
            button2.configure(state="normal", bg="#1166EE")
        else:
            messagebox.showerror("Ошибка", "Выберите папку")
            return
    elif folder_id == 2:
        if folder_path:
            config_for_interface.path_to_from_folder = folder_path
            button2.configure(bg="#118844")
            button3.configure(state="normal", bg="#1166EE")
        else:
            messagebox.showerror("Ошибка", "Выберите папку")
            return
    elif folder_id == 3:
        if folder_path:
            config_for_interface.path_to_from_folder = folder_path
            button6.configure(bg="#118844")
            button7.configure(state="normal", bg="#1166EE")
        else:
            messagebox.showerror("Ошибка", "Выберите папку")
            return
    elif folder_id == 4:
        if folder_path:
            config_for_interface.path_to_to_folder = folder_path
            button7.configure(bg="#118844")
            start_button_for_fact.configure(state="normal", bg="#1166EE")
        else:
            messagebox.showerror("Ошибка", "Выберите папку")
            return


def get_paths_to_file(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            file_paths.append(file_path)
    return file_paths


def update_progress(value, count):
    """Функция обновляет значение количества загруженных файлов"""
    percent_label.configure(text=f"Загружено: {value} файлов из {count}")


def switch_info_labels(value):
    """Функция выводит текстовую информацию о результате загрузки"""
    succes = sum(1 for item in config_for_interface.path_to_results
                 if item is not None)
    if value == 0:
        info_label.configure(text="Пожалуйста, ожидайте, выгрузка ОФ может занимать длительное время")
    else:
        info_label.configure(
            text=f"Загрузка завершена. Загружено: {len(config_for_interface.path_to_results)} файлов.\n Успешно: {succes}")


def change_after_work(value):
    """Функция задает изменения в стилях после окончания выгрузки обменных форм"""
    percent_label.place_forget()
    switch_info_labels(value)
    info_label.place_configure(relx=0.025, rely=0.5)
    button3.configure(bg="#118844")
    button4.configure(state="normal", bg="#1166EE")
    button5.configure(state="normal", bg="#1166EE")


def find_name(list_projects, excel_path):
    name = os.path.splitext(os.path.basename(excel_path))[0]
    for path in list_projects:
        file_name = os.path.splitext(os.path.basename(path))[0]
        if file_name == name:
            return path


def start_click(folder_id):
    if not os.path.exists(config_for_interface.path_to_reserve_folder):
        os.mkdir(config_for_interface.path_to_reserve_folder)
    path_to_excel_folder = config_for_interface.path_to_reserve_folder + '\\' + "OF"
    path_to_project_folder = config_for_interface.path_to_reserve_folder + '\\' + "projects"
    path_to_unsuccessful_folder = config_for_interface.path_to_reserve_folder + '\\' + "unsuccessful"
    paths_to_bad_files = []
    if not os.path.exists(path_to_excel_folder):
        os.mkdir(path_to_excel_folder)
    if not os.path.exists(path_to_project_folder):
        os.mkdir(path_to_project_folder)
    if not os.path.exists(path_to_unsuccessful_folder):
        os.mkdir(path_to_unsuccessful_folder)
    value = 0
    percent_label.place(relx=0.025, rely=0.5)
    info_label.place(relx=0.025, rely=0.55)
    switch_info_labels(value)
    if folder_id == 1:
        paths_to_projects = get_paths_to_file(config_for_interface.path_to_from_folder)
        if paths_to_projects is None:
            return
        update_progress(value, len(paths_to_projects))
        window.update()
        try:
            file_transfer.transfer_files(paths_to_projects, path_to_project_folder)
        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка",
                                 e)
            return
        for path in paths_to_projects:
            file_name = os.path.basename(path)
            path = os.path.join(path_to_project_folder, file_name)
            res = readOF.main(path, path_to_excel_folder)
            if res is None:
                paths_to_bad_files.append(path)
                text_area.insert(tk.INSERT,
                                 f"{os.path.basename(paths_to_projects[value])}    -    Не успешно\n")
            else:
                text_area.insert(tk.INSERT,
                                 f"{os.path.basename(paths_to_projects[value])}    -    Успешно\n")
            value = value + 1
            update_progress(value, len(paths_to_projects))
            window.update()
            config_for_interface.path_to_results.append(res)
    elif folder_id == 2:
        paths_to_excel = get_paths_to_file(config_for_interface.path_to_from_folder)
        paths_to_projects = get_paths_to_file(config_for_interface.path_to_to_folder)
        try:
            file_transfer.transfer_files(paths_to_projects, path_to_project_folder)
            file_transfer.transfer_files(paths_to_excel, path_to_excel_folder)
        except Exception as e:
            print(e)
            messagebox.showerror("Ошибка",
                                 e)
            return
        for path in paths_to_excel:
            path_to_proj = find_name(paths_to_projects, path)
            if path_to_proj is None:
                continue
            fact.main(path_to_proj, path)

    try:
        file_transfer.transfer_files(config_for_interface.path_to_results, config_for_interface.path_to_to_folder)
    except Exception as e:
        print(e)
        messagebox.showerror("Ошибка",
                             e)
        return
    if paths_to_bad_files:
        file_transfer.transfer_files(paths_to_bad_files, path_to_unsuccessful_folder)

    change_after_work(value)


def on_tab_selected(event):
    """Обработчик переключения вкладок приложения"""
    selected_tab = notebook.index(notebook.select())
    if selected_tab == 0:
        button1.config(state="normal")
        button2.config(state="disabled")
    elif selected_tab == 1:
        button1.config(state="disabled")
        button2.config(state="normal")


def on_window_resize(event):
    """Обработчик события изменения размеров окна"""
    new_width = window.winfo_width()
    new_height = window.winfo_height()

    button_width = int(new_width / 7)
    button_height = int(new_height / 15)
    label_width = int(new_width / 1.2)
    label_height = int(new_height / 15)
    text_area_height = int(new_height / 3)
    # Обновляем ширину кнопок
    button1.place(width=button_width, height=button_height)
    button2.place(width=button_width, height=button_height)
    button3.place(width=button_width, height=button_height)
    label1.place(width=label_width, height=label_height)
    label2.place(width=label_width, height=label_height)
    label3.place(width=label_width, height=label_height)
    text_area.place(width=label_width / 1.3, height=text_area_height)


def open_reserve_folder():
    if config_for_interface.path_to_reserve_folder:
        os.startfile(config_for_interface.path_to_reserve_folder)


def open_folder_with_res():
    if config_for_interface.path_to_to_folder:
        os.startfile(config_for_interface.path_to_to_folder)


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Приложение для работы с ОФ")
    window.geometry("1000x600")
    window.minsize(1000, 600)
    window.configure(background="light blue")
    notebook = ttk.Notebook(window)
    notebook.bind("<<NotebookTabChanged>>", on_tab_selected)
    style = ttk.Style()
    style.configure("TNotebook", background="blue")
    style.configure("TFrame", background="light blue")
    button_style_active = {'background': '#1166EE', 'foreground': 'white',
                           'font': ('Arial', 12)}
    button_style_done = {'background': '#118844', 'foreground': 'white',
                         'font': ('Arial', 12)}
    button_style_block = {'background': '#969699', 'foreground': 'white',
                          'font': ('Arial', 12)}
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab1, text="Выгрузка ОФ")
    label0 = tk.Label(tab1, text="Эта программа предназначена для выгрузки обменных форм из файлов project в папку",
                      font=('Arial', 14), background="light blue")
    label0.pack()
    button1 = tk.Button(tab1, text="Выбрать папку",
                        command=lambda: button_click(1),
                        **button_style_active, state="normal",
                        width=15)
    button1.place(relx=0.025, rely=0.17)
    label1 = tk.Label(tab1, text="Эта кнопка позволяет выбрать папку, в которую нужно выгрузить обменные формы",
                      font=('Arial', 14), anchor='w', background="light blue")
    label1.place(relx=0.2, rely=0.17)
    button2 = tk.Button(tab1, text="Выбрать папку",
                        command=lambda: button_click(2),
                        **button_style_block, state="disabled",
                        width=15)
    button2.place(relx=0.025, rely=0.27)
    label2 = tk.Label(tab1, text="Эта кнопка позволяет выбрать папку с файлами project для выгрузки обменной формы",
                      font=('Arial', 14), anchor='w', background="light blue")
    label2.place(relx=0.2, rely=0.27)
    button3 = tk.Button(tab1, text="Начать",
                        command=lambda: start_click(1),
                        **button_style_block, state="disabled",
                        width=15)
    button3.place(relx=0.025, rely=0.37)
    label3 = tk.Label(tab1, text="Эта кнопка позволяет начать выполнение программы",
                      font=('Arial', 14), anchor='w', background="light blue")
    label3.place(relx=0.2, rely=0.37)
    button4 = tk.Button(tab1, text="Открыть резервную папку", command=open_reserve_folder, **button_style_block,
                        state="disabled",
                        width=21)
    button4.place(relx=0.78, rely=0.5)
    button5 = tk.Button(tab1, text="Открыть папку с ОФ", command=open_folder_with_res, **button_style_block,
                        state="disabled",
                        width=17)
    button5.place(relx=0.6, rely=0.5)
    percent_label = tk.Label(tab1, text="Выгружено: 0 файлов", font=('Arial', 12), background="light blue")
    info_label = tk.Label(tab1, text="Пожалуйста, ожидайте, выгрузка ОФ может занимать длительное время",
                          font=('Arial', 12), background="light blue")
    text_area = scrolledtext.ScrolledText(tab1, width=80, height=10)
    text_area.place(relx=0.17, rely=0.6)

    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Вкладка 2")

    button6 = tk.Button(tab2, text="Выбрать папку с ОФ", command=lambda: button_click(3), **button_style_active,
                        width=20)
    button6.place(relx=0.025, rely=0.17)
    button7 = tk.Button(tab2, text="Выбрать папку с project", command=lambda: button_click(4), **button_style_block, width=20)
    button7.place(relx=0.025, rely=0.27)
    start_button_for_fact = tk.Button(tab2, text="Начать внесение", command=lambda: start_click(2), **button_style_block,
                                      width=20)
    start_button_for_fact.place(relx=0.025, rely=0.37)

    window.bind("<Configure>", on_window_resize)
    notebook.pack(fill=tk.BOTH, expand=True)
    messagebox.showwarning("Предупреждение",
                           "Пожалуйста, закройте открытые файлы project для корректной работы программы")
    window.mainloop()
