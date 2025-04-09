import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Server")
        self.root.geometry("1920x1080")
#make a chicken appear on the screen
        self.chicken_image = tk.PhotoImage(file="C:/Users/danie/OneDrive/Desktop/Skibidi/chicken.png")
        self.chicken_label = tk.Label(root, image=self.chicken_image)
        self.chicken_label.pack()
        #make the chicken smaller and just in the top left corner
        self.chicken_label.place(x=0, y=0)
        self.chicken_label.image = self.chicken_image
        # Folder selection
        self.folder_frame = ttk.Frame(root)
        self.folder_frame.pack(pady=10, padx=10, fill="x")
        
        self.folder_label = ttk.Label(self.folder_frame, text="Folder:")
        self.folder_label.pack(side="left")
        
        self.folder_entry = ttk.Entry(self.folder_frame)
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(5, 5))
        
        self.browse_button = ttk.Button(self.folder_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="right")

        # Port selection
        self.port_frame = ttk.Frame(root)
        self.port_frame.pack(pady=10, padx=10, fill="x")
        
        self.port_label = ttk.Label(self.port_frame, text="Port:")
        self.port_label.pack(side="left")
        
        self.port_entry = ttk.Entry(self.port_frame)
        self.port_entry.insert(0, "8000")
        self.port_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Start button
        self.start_button = ttk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack(pady=20)

        # Status label
        self.status_label = ttk.Label(root, text="Server: Stopped")
        self.status_label.pack(pady=10)

        self.server = None
        self.server_thread = None

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def start_server(self):
        if self.server is None:
            folder = self.folder_entry.get()
            try:
                port = int(self.port_entry.get())
            except ValueError:
                tk.messagebox.showerror("Error", "Invalid port number")
                return

            if not folder:
                tk.messagebox.showerror("Error", "Please select a folder")
                return

            # Create a custom handler class that uses the selected directory
            class CustomHandler(SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=folder, **kwargs)

            self.server = HTTPServer(('', port), CustomHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.status_label.config(text=f"Server: Running on port {port}")
            self.start_button.config(text="Stop Server")
        else:
            self.server.shutdown()
            self.server = None
            self.status_label.config(text="Server: Stopped")
            self.start_button.config(text="Start Server")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()