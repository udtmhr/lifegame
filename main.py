import tkinter as tk
from lifegame import LifeGame

WIDTH = 800
HEIGHT = 850
MASS = 64

class GUILifeGame(LifeGame):
    def __init__(self):
        super().__init__()

        self.make_root()
        self.make_canvas()
        self.make_widget()
        self.event()

    def make_root(self):
        self.root = tk.Tk()
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.title("Life Game")
    
    def make_widget(self):
        widget_frame = tk.Frame(
            self.root,
            width=WIDTH,
            height=HEIGHT - WIDTH,
        )

        widget_frame.propagate(False)
        widget_frame.pack()

        start_botton = tk.Button(
            widget_frame,
            text="start",
            width=10,
            height=10,
            command=self.run,
        )
        start_botton.pack(side=tk.LEFT)

        stop_boutton = tk.Button(
            widget_frame,
            text="stop",
            width=10,
            height=10,
            command=self.stop,
        )
        stop_boutton.pack(side=tk.LEFT)

        reset_button = tk.Button(
            widget_frame,
            text="reset",
            width=10,
            height=10,
            command=self.reset,
        )
        reset_button.pack(side=tk.LEFT)

        self.fps_scale = tk.Scale(
            widget_frame,
            variable=tk.DoubleVar(),
            orient=tk.HORIZONTAL,
            length=200,
            width=13,
            sliderlength=5,
            from_=0.1,
            to=5,
            resolution=0.1,
            tickinterval=5,
        )
        label = tk.Label(
            widget_frame,
            text="FPS(/s)",
        )
        self.fps_scale.pack(side=tk.RIGHT)
        label.pack(side=tk.RIGHT)

    def make_canvas(self):
        canvas_frame = tk.Frame(
            self.root,
            width=WIDTH,
            height=WIDTH,
        )

        canvas_frame.propagate(False)
        canvas_frame.pack(side=tk.TOP)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=WIDTH,
            height=WIDTH,
        )

        self.canvas.pack()
        mass_size = WIDTH / MASS
        for y in range(MASS):
            for x in range(MASS):
                self.canvas.create_rectangle(
                    x * mass_size, y * mass_size, (x + 1) * mass_size, (y + 1) * mass_size, 
                    fill="black", tags=f"mass_{x}_{y}",outline="white",
                )

    def change_color(self, tag, color):
        self.canvas.itemconfig(tag, fill=color)

    def update(self):
        for y in range(1, self.h + 1):
            for x in range(self.w):
                color = "green" if (self.board[y] << x) & 0x8000000000000000 else "black"
                self.change_color(f"mass_{x}_{y - 1}", color)
    
    def run(self):
        self.fps_scale["state"] = tk.DISABLED
        self.canvas["state"] = tk.DISABLED
        self.next_board()
        self.update()
        time = self.fps_scale.get() * 1000
        self.id = self.canvas.after(int(time), self.run)
    
    def stop(self):
        self.canvas.after_cancel(self.id)
        self.fps_scale["state"] = tk.NORMAL
        self.canvas["state"] = tk.NORMAL

    def reset(self):
        super().__init__()
        mass_size = WIDTH / MASS
        for y in range(MASS):
            for x in range(MASS):
                self.canvas.create_rectangle(
                    x * mass_size, y * mass_size, (x + 1) * mass_size, (y + 1) * mass_size, 
                    fill="black", tags=f"mass_{x}_{y}",outline="white",
                )
    
    def click(self, event, color="green"):
        mass_size = WIDTH / MASS
        x = int(event.x / mass_size)
        y = int(event.y / mass_size)
        #tag = self.canvas.find_closest(event.x, event.y)
        tag = f"mass_{x}_{y}"
        self.change_color(tag, color)
        self.set_life(x, y)
    
    def event(self):
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button1-Motion>", self.click)
        self.canvas.bind("<Button-3>", lambda event: self.click(event, "black"))
        self.canvas.bind("<Button3-Motion>", lambda event: self.click(event, "black"))

if __name__ == "__main__":
    gui = GUILifeGame()
    gui.root.mainloop()