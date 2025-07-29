import tkinter as tk
from PIL import Image, ImageTk

BOARD_SIZE = 8
TILE_SIZE = 64

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
        self.root.title("Chess GUI")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * TILE_SIZE, height=BOARD_SIZE * TILE_SIZE)
        self.canvas.pack()
        self.images = {}
        self.load_images()
        self.board = [row[:] for row in START_POSITION]
        self.selected = None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def load_images(self):
        pieces = ['wp', 'wr', 'wn', 'wb', 'wq', 'wk',
                  'bp', 'br', 'bn', 'bb', 'bq', 'bk']
        for piece in pieces:
            img_path = f"images/png/{piece}.png"
            img = Image.open(img_path).resize((TILE_SIZE, TILE_SIZE))
            self.images[piece] = ImageTk.PhotoImage(img)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * TILE_SIZE
                y1 = row * TILE_SIZE
                color = "#EEEED2" if (row + col) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x1, y1, x1 + TILE_SIZE, y1 + TILE_SIZE, fill=color)

                piece = self.board[row][col]
                if piece:
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
