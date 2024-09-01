import tkinter as tk
import tkinter.simpledialog as dialog
import tkinter.messagebox as message
import time
import threading

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title('Productivity Timer')

        self.time_left = 0
        self.reference_time = 0
        self.running = False
        self.paused = False  # Track if the timer is paused

        self.label = tk.Label(root, text='00:00', font=("Helvetica", 48))
        self.label.pack()

        self.start_button = tk.Button(root, text='Start', command=self.start_timer)
        self.start_button.pack(side='left')

        self.reset_button = tk.Button(root, text='Reset', command=self.reset_timer)
        self.reset_button.pack(side='left')

        self.pause_button = tk.Button(root, text='Pause', command=self.pause_resume_timer)
        self.pause_button.pack(side='left')

        self.hide_button = tk.Button(root, text='Hide', command=self.hide_timer)
        self.hide_button.pack(side='left')

    def get_time(self):
        self.reference_time = dialog.askinteger("Set Timer", "Enter time in seconds: ")

        while self.reference_time == 0 or type(self.reference_time) != int:
            message.showwarning("Invalid Input", "Please enter a valid time (Cannot enter 0 seconds or non-integer values)")
            self.reference_time = dialog.askinteger("Set Timer", "Enter time in seconds: ")

        message.showinfo("Timer Set", f"Timer set to {self.reference_time} seconds")
        return self.reference_time

    def start_timer(self):
        if not self.running and not self.paused:
            self.time_left = self.get_time()
            self.running = True
            threading.Thread(target=self.update_timer).start()

    def pause_resume_timer(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text='Resume')
            else:
                self.pause_button.config(text='Pause')
    
    def reset_timer(self):
        time.sleep(0.5)
        self.time_left = self.reference_time
        mins, secs = divmod(self.time_left, 60)
        self.label.config(text=f'{mins:02d}:{secs:02d}')
        self.running = True
    
        if not self.paused:
            self.paused = True
            self.pause_button.config(text='Resume')

    def hide_timer(self):
        self.root.iconify()

    def update_timer(self):
        while self.time_left > 0 and self.running:
            if not self.paused:
                mins, secs = divmod(self.time_left, 60)
                timer = f'{mins:02d}:{secs:02d}'
                self.label.config(text=timer)
                self.root.update()
                time.sleep(1)
                self.time_left -= 1

        if self.time_left == 0:
            self.label.config(text="Time's Up!!")
            self.root.deiconify()
            self.running = False  # Reset running state when time is up

def run_timer():
    root = tk.Tk()
    timer = CountdownTimer(root)
    root.mainloop()


if __name__ == "__main__":
    run_timer()