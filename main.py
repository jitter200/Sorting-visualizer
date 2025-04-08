import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализатор сортировок")
        self.root.geometry("900x600")
        self.array = []
        self.speed = 100
        self.paused = False
        self.sorting = False

        self.canvas = tk.Canvas(root, width=850, height=400, bg='white')
        self.canvas.pack(pady=20)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.input_entry = tk.Entry(self.controls_frame, width=40)
        self.input_entry.grid(row=0, column=0, padx=5)
        tk.Button(self.controls_frame, text="Ввести массив", command=self.load_input_array).grid(row=0, column=1, padx=5)
        tk.Button(self.controls_frame, text="Случайный массив", command=self.generate_random_array).grid(row=0, column=2, padx=5)
        tk.Button(self.controls_frame, text="Старт", command=self.start_sort).grid(row=0, column=3, padx=5)
        tk.Button(self.controls_frame, text="Пауза / Продолжить", command=self.toggle_pause).grid(row=0, column=4, padx=5)

        tk.Label(self.controls_frame, text="Скорость:").grid(row=1, column=0, padx=5, pady=10)
        self.speed_scale = tk.Scale(self.controls_frame, from_=1, to=500, orient=tk.HORIZONTAL, command=self.set_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=1, column=1, padx=5)

        tk.Label(self.controls_frame, text="Алгоритм:").grid(row=1, column=2, padx=5)
        self.algorithm_choice = ttk.Combobox(self.controls_frame, values=["Bubble Sort", "Quick Sort", "Merge Sort"])
        self.algorithm_choice.set("Bubble Sort")
        self.algorithm_choice.grid(row=1, column=3, padx=5)

        self.generate_random_array()

    def load_input_array(self):
        try:
            values = list(map(int, self.input_entry.get().split(',')))
            self.array = values
            self.draw_array()
        except:
            print("Ошибка ввода!")

    def generate_random_array(self):
        self.array = [random.randint(10, 390) for _ in range(50)]
        self.draw_array()

    def draw_array(self, highlight_indices=[]):
        self.canvas.delete("all")
        if not self.array:
            return
        bar_width = 850 // len(self.array)
        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = 400 - val
            x1 = x0 + bar_width - 2
            y1 = 400
            color = "red" if i in highlight_indices else "blue"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def set_speed(self, val):
        self.speed = int(val)

    def toggle_pause(self):
        self.paused = not self.paused

    def wait(self):
        while self.paused:
            time.sleep(0.05)

    def start_sort(self):
        if self.sorting: return
        algo = self.algorithm_choice.get()
        t = threading.Thread(target=self.run_sort, args=(algo,))
        t.start()

    def run_sort(self, algo):
        self.sorting = True
        if algo == "Bubble Sort":
            self.bubble_sort()
        elif algo == "Quick Sort":
            self.quick_sort(0, len(self.array) - 1)
        elif algo == "Merge Sort":
            self.merge_sort(0, len(self.array) - 1)
        self.sorting = False

    def bubble_sort(self):
        arr = self.array
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.draw_array([j, j+1])
                    self.wait()
                    time.sleep(self.speed / 1000.0)

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

    def partition(self, low, high):
        arr = self.array
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                self.draw_array([i, j])
                self.wait()
                time.sleep(self.speed / 1000.0)
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        self.draw_array([i, high])
        time.sleep(self.speed / 1000.0)
        return i

    def merge_sort(self, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        self.merge_sort(left, mid)
        self.merge_sort(mid + 1, right)
        self.merge(left, mid, right)

    def merge(self, left, mid, right):
        arr = self.array
        left_part = arr[left:mid+1]
        right_part = arr[mid+1:right+1]
        i = j = 0
        for k in range(left, right + 1):
            if j >= len(right_part) or (i < len(left_part) and left_part[i] <= right_part[j]):
                arr[k] = left_part[i]
                i += 1
            else:
                arr[k] = right_part[j]
                j += 1
            self.draw_array([k])
            self.wait()
            time.sleep(self.speed / 1000.0)

if __name__ == '__main__':
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
