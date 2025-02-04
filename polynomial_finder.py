import tkinter as tk
import customtkinter as ctk
import numpy as np
import warnings
WIDTH = 1000
HEIGHT = 750


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{WIDTH}x{HEIGHT+25}")
        self.resizable(0, 0)
        self.title("Find Polynomial")
        self.canvas = tk.Canvas(self)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=0.97)
        self.point_x = []
        self.point_y = []
        self.degree = len(self.point_y) - 1

        self.canvas.bind("<Button-1>", self.mouse_pos)

        self.show = True
        self.var = tk.BooleanVar(value=True)

        self.show_button = tk.Checkbutton(self, text="Show polynomial", font="Arial 19",
                                          onvalue=True, offvalue=False, variable=self.var, command=self.hide)
        self.reset_btn = tk.Button(self, text="Reset", font="Arial 20", command=self.restart)

        self.show_button.place(x=0, y=0)
        self.reset_btn.place(x=900, y=0, height=50, width=100)

        self.draw_grid()

        self.mainloop()

    def restart(self):
        self.canvas.delete("all")
        self.point_x = []
        self.point_y = []
        self.degree = len(self.point_y) - 1
        self.draw_grid()
        self.show = self.var.get()

    def hide(self):
        if self.show:
            self.canvas.delete("all")
            self.show = False
            self.draw_grid()
            self.draw_points()
        else:
            self.show = True
            self.canvas.delete("all")
            self.draw_grid()
            self.draw_points()
            if self.degree >= 1:
                self.draw_polynomial()

    def draw_grid(self):
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='white')
        self.canvas.create_line(WIDTH/2, 0, WIDTH/2, HEIGHT, fill="black", width=3)
        self.canvas.create_line(0, HEIGHT/2, WIDTH, HEIGHT/2, fill="black", width=3)

        width = 0
        height = 0
        while width < WIDTH:
            width += 25
            self.canvas.create_line(width, 0, width, HEIGHT)
        while height < HEIGHT:
            height += 25
            self.canvas.create_line(0, height, WIDTH, height)

    def draw_points(self):
        for i in range(len(self.point_x)):
            self.canvas.create_oval(self.point_x[i]-3, self.point_y[i]-3,
                                    self.point_x[i]+3, self.point_y[i]+3,
                                    fill="red", outline="red")

    def mouse_pos(self, e):
        self.point_x.append(e.x)
        self.point_y.append(e.y)
        self.canvas.create_oval(e.x-3, e.y-3, e.x+3, e.y+3, fill="red", outline="red")

        self.degree = len(self.point_y) - 1

        if self.degree >= 1:
            self.draw_grid()
            if self.show:
                self.draw_polynomial()
            self.draw_points()

    def draw_polynomial(self):

        coeff = np.polyfit(self.point_x, self.point_y, deg=self.degree)

        def func(arg):
            res = 0
            deg = len(coeff) - 1
            for j in coeff:
                res += j * pow(arg, deg)
                deg -= 1
            return res

        last = [0, func(0)]

        for x in range(WIDTH+1):
            self.canvas.create_line(last[0], last[1], x, func(x), width=2, fill="blue")
            last = [x, func(x)]


Window()
