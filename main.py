import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

# JSONファイルのパスを指定
json_file_path = "dart_scores.json"

# JSONファイルからデータを読み込む関数
def load_scores():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# JSONファイルにデータを書き込む関数
def save_scores(scores):
    with open(json_file_path, "w") as f:
        json.dump(scores, f, indent=4)

# 点数順にソートして上位5名を取得
def get_top_5(scores):
    return sorted(scores, key=lambda x: x['score'], reverse=True)[:5]

class DartRankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dart Ranking Board")
        self.root.geometry("800x600")

        # ウィンドウサイズ変更に対応させる
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # メインフレームを作成して中央に配置
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # 背景画像の設定
        self.set_background()

        # スコアのデータをロード
        self.scores = load_scores()

        # 上部のラベル (中央揃え)
        title_label = tk.Label(self.main_frame, text="Top 5 Dart Players", font=("YDW バナナスリップplus plus", 24, "bold"), bg="#333", fg="white")
        title_label.grid(row=0, column=0, pady=10, sticky="n")

        # ランキング表示用のフレーム (幅と高さを縮小)
        self.rank_frame = tk.Frame(self.main_frame, bg="#222", width=400, height=200)
        self.rank_frame.grid(row=1, column=0, pady=10, sticky="nsew")
        self.rank_frame.grid_columnconfigure(0, weight=1)
        self.rank_frame.grid_rowconfigure(0, weight=1)

        # ランキングを更新
        self.update_ranking()

        # 入力エリア（中央揃え）
        self.entry_frame = tk.Frame(self.main_frame, bg="#222")
        self.entry_frame.grid(row=2, column=0, pady=20, padx=20, sticky="n")
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.entry_frame.grid_rowconfigure(0, weight=1)

        # 入力フィールドの設定
        self.name_label = tk.Label(self.entry_frame, text="Name:", bg="#222", fg="white", font=("源ノ角ゴシック JP", 12))
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.name_entry = tk.Entry(self.entry_frame, justify="center")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.score_label = tk.Label(self.entry_frame, text="Score:", bg="#222", fg="white", font=("源ノ角ゴシック JP", 12))
        self.score_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.score_entry = tk.Entry(self.entry_frame, justify="center")
        self.score_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # ボタン
        add_button = tk.Button(self.entry_frame, text="Add Score", command=self.add_score, bg="#4CAF50", fg="white", font=("源ノ角ゴシック JP", 12))
        add_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="n")

        del_button = tk.Button(self.entry_frame, text="Delete Score", command=self.delete_score, bg="#f44336", fg="white", font=("源ノ角ゴシック JP", 12))
        del_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="n")

    def set_background(self):
        """ダーツのイラスト背景を設定"""
        # 画像をロードし、サイズを調整
        self.bg_image = Image.open("dart_background.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.ANTIALIAS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # ラベルに画像を配置して背景にする
        self.background_label = tk.Label(self.main_frame, image=self.bg_image_tk)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_ranking(self):
        """ランキングをリフレッシュする"""
        # ランキングフレーム内をクリア
        for widget in self.rank_frame.winfo_children():
            widget.destroy()

        top_5 = get_top_5(self.scores)

        # ランキングの表示
        for idx, player in enumerate(top_5, start=1):
            player_label = tk.Label(self.rank_frame, text=f"{idx}. {player['name']} - {player['score']} pts",
                                    font=("源ノ角ゴシック JP", 18), bg="#222", fg="white")
            player_label.pack(anchor="center", pady=5)

    def add_score(self):
        name = self.name_entry.get()
        try:
            score = int(self.score_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Score must be a number")
            return

        if name and score:
            self.scores.append({"name": name, "score": score})
            save_scores(self.scores)
            self.update_ranking()
            self.name_entry.delete(0, tk.END)
            self.score_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Both fields must be filled")

    def delete_score(self):
        name = self.name_entry.get()
        if name:
            self.scores = [player for player in self.scores if player['name'] != name]
            save_scores(self.scores)
            self.update_ranking()
            self.name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid Input", "Name field must be filled")


# アプリの実行
if __name__ == "__main__":
    root = tk.Tk()
    app = DartRankingApp(root)
    root.mainloop()
