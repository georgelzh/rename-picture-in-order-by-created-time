import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

class App:
    def __init__(self) -> None:
        self.path = os.getcwd()
        self.window = tk.Tk()
        self.window.title("照片重命名神器 - by 李志鸿")
        self.window.geometry("600x300")
        self.window.configure(background="#856ff8")
        # self.window.resizable(False, False)
        self.hello_label = tk.Label(
            master=self.window,
            text="Hello！陌生人，你又想我了？",
            foreground="red",  # Set the text color to white
            background="black"  # Set the background color to black
        )
        self.hello_label.pack(padx=10, pady=10)

        self.input_frame = tk.Frame(self.window, width=500, height=300)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.columnconfigure(1, weight=1)
        self.input_frame.columnconfigure(2, weight=1)
        self.input_frame.columnconfigure(3, weight=1)

        self.picture_number_per_group_entry = tk.Entry(master=self.input_frame, width=25)
        self.picture_number_per_group_entry.insert(0, "请输入每组照片的数量，默认为4")

        self.curr_dir_entry = tk.Entry(master=self.input_frame, width=55)
        self.curr_dir_entry.insert(0, "照片文件夹的绝对路径，比如: 'C:\照片集' (不填也行，把此软件放到对应文件夹即可)")

        self.select_dir_button= tk.Button(self.input_frame, text="选择文件夹", command= self.select_dir)
        self.show_dir_path= tk.Label(self.input_frame, text="...", wraplength=300, width=90)

        self.confirm_button = tk.Button(
            master=self.input_frame,
            text="大力出奇迹 :))",
            width=9,
            height=3,
            fg="black",
            command=self.rename_pictures
        )

        self.picture_number_per_group_entry.grid(row=2, column=0, padx=5, pady=5)
        self.select_dir_button.grid(row=1, column=0, ipadx=5, pady=15)
        self.show_dir_path.grid(row=0, column=0, ipadx=5, pady=15)
        self.confirm_button.grid(row=3, column=0, padx=5, pady=5)
        self.input_frame.pack(padx=10, pady=10)
        self.window.mainloop()

    def get_sorted_files_n_created_time(self):
        dir_path = self.path
        filenames = os.listdir(self.path)
        files_n_create_time = []
        for idx, filename in enumerate(filenames):
            filepath = os.path.join(dir_path, filename)
            if os.path.isfile(filepath):
                # make sure the software doesn't rename itself.
                if ".py" in filepath or ".exe" in filepath or ".DS_Store" in filepath:
                    continue
                created_time = os.path.getmtime(filepath)
                created_time = datetime.fromtimestamp(created_time)
                files_n_create_time.append([str(created_time), filepath])

        files_n_create_time.sort(key=lambda x: x[0])  # [[created_time, abs_filepath], [created_time, abs_filepath], ...]
        return files_n_create_time

    def select_dir(self):
        path= filedialog.askdirectory(title="Select a File")
        self.show_dir_path.configure(text=path)
        self.path = path


    def rename_pictures(self, files_n_create_time: list = [], number: int = 4):
        """
        params:
            files_n_create_time (arr): all the files within the folder, sorted with stampstamp.
            number: used to group files and rename them
        """
        dir_path = self.path
        files_n_create_time = self.get_sorted_files_n_created_time()
        for file in files_n_create_time:
            print(file)

        try:
            number = int(self.picture_number_per_group_entry.get())
        except:
            number = 4

        product_num = 1
        file_suffix = ".jpg"
        try:
            file_suffix = "." + files_n_create_time[1][1].split(".")[-1]
            print("file_suffix for all files: ", file_suffix)
        except Exception as err:
            raise(err)
            print("please make sure the picture name is like 'hello.jpg' or 'hello.png' etc format")

        idx = 0
        file_idx = 0

        while file_idx < len(files_n_create_time):
            filepath = files_n_create_time[file_idx][1]
            print(filepath)

            if idx < number:
                if idx == 0:
                    os.rename(filepath, dir_path + "/" + "product_" + str(product_num) + "_1" + file_suffix)
                else:
                    os.rename(filepath, dir_path + "/" + "product_" + str(product_num) + "_1" + "0" + str(idx) + file_suffix)
            file_idx += 1
            idx += 1
            if idx == number:
                idx = 0
                product_num += 1
        messagebox.showinfo(title="重命名成功！", message="客官，下次再来哦！;)")


if __name__ == "__main__":
    App()
