import tkinter as tk
from PIL import Image, ImageTk

BOARD_SIZE = 8
TILE_SIZE = 125  # 1000 / 8 = 125

# FEN-based simple start position
START_POSITION = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp"] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    [""] * 8,
    ["wp"] * 8,
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess GUI - A new Chapter")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * TILE_SIZE, height=BOARD_SIZE * TILE_SIZE)
        self.canvas.pack()
        self.images = {}
        self.load_images()
        self.board = [row[:] for row in START_POSITION]
        self.selected = None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

        self.root.geometry("1000x1000") #make res to be 1200 fixed while testing. 
        self.root.resizable(False, False)  # Disable resizing

        # Add Escape key to close the app
        self.root.bind("<Escape>", self.show_closing_message)

    def show_closing_message(self, event=None):
        # Display "Closing..." text in the center with red color
        self.closing_text_id = self.canvas.create_text(
            BOARD_SIZE * TILE_SIZE // 2,
            BOARD_SIZE * TILE_SIZE // 2,
            text="Closing...",
            font=("Helvetica", 36, "bold"),
            fill="#FF0000"
        )
        self.fade_step = 0
        self.fade_out_text()

    def fade_out_text(self):
        # Fade color from red to light red to transparent
        if self.fade_step < 20:
            alpha = int(255 * (1 - self.fade_step / 20))  # 255 to 0
            color = f"#{alpha:02x}0000"  # Red with decreasing intensity
            self.canvas.itemconfig(self.closing_text_id, fill=color)
            self.fade_step += 1
            self.root.after(100, self.fade_out_text)
        else:
            self.canvas.delete(self.closing_text_id)
            self.root.quit()

    def load_images(self):
        pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
                'bp', 'br', 'bn', 'bb', 'bq', 'bk']
        for piece in pieces:
            img_path = f"images/png/converted/{piece}.png"
            img = Image.open(img_path).convert("RGBA").resize((TILE_SIZE, TILE_SIZE))
            self.images[piece] = ImageTk.PhotoImage(img)


    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * TILE_SIZE
                y1 = row * TILE_SIZE
                # Light squares yellowish, dark squares green
                color = "#616062" if (row + col) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x1, y1, x1 + TILE_SIZE, y1 + TILE_SIZE, fill=color)

                piece = self.board[row][col]
                # if piece:
                    # self.canvas.create_image(x1, y1, anchor="nw", image=self.images[piece])
                if piece:
                    # Draw a colored rect behind the piece (debug only)
                    self.canvas.create_rectangle(x1 + 5, y1 + 5, x1 + TILE_SIZE - 5, y1 + TILE_SIZE - 5, outline="")
                    self.canvas.create_image(x1, y1, anchor="nw", image=self.images[piece])

        if self.selected:
            r, c = self.selected
            self.canvas.create_rectangle(
                c * TILE_SIZE, r * TILE_SIZE,
                (c + 1) * TILE_SIZE, (r + 1) * TILE_SIZE,
                outline="red", width=3
            )

    def on_click(self, event):
        col = event.x // TILE_SIZE
        row = event.y // TILE_SIZE

        if self.selected:
            sr, sc = self.selected
            if (sr, sc) != (row, col):
                self.board[row][col] = self.board[sr][sc]
                self.board[sr][sc] = ""
            self.selected = None
        elif self.board[row][col]:
            self.selected = (row, col)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
