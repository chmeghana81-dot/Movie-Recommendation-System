import tkinter as tk
from tkinter import messagebox
from recommender import MovieRecommender


class MovieRecommendationApp:

    def __init__(self, root):

        self.root = root

        # ==============================
        # Window Configuration
        # ==============================

        self.root.title("Movie Recommendation System")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Background
        self.root.configure(bg="#0f172a")

        # Recommendation engine
        self.recommender = MovieRecommender()

        # ==============================
        # Colors
        # ==============================

        self.bg_color = "#0f172a"
        self.card_color = "#1e293b"
        self.input_color = "#334155"
        self.text_color = "#f8fafc"
        self.secondary_text = "#94a3b8"
        self.button_color = "#e11d48"
        self.button_hover = "#be123c"
        self.result_color = "#273449"

        # ==============================
        # Header
        # ==============================

        header = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        header.pack(
            fill="x",
            pady=(35, 10)
        )

        title = tk.Label(
            header,
            text="🎬  Movie Recommendation System",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Discover movies similar to your favorite films",
            font=("Arial", 13),
            bg=self.bg_color,
            fg=self.secondary_text
        )

        subtitle.pack(pady=(8, 0))

        # ==============================
        # Search Card
        # ==============================

        search_card = tk.Frame(
            self.root,
            bg=self.card_color,
            width=760,
            height=170
        )

        search_card.pack(
            pady=25,
            padx=70
        )

        search_card.pack_propagate(False)

        search_label = tk.Label(
            search_card,
            text="Search for a Movie",
            font=("Arial", 15, "bold"),
            bg=self.card_color,
            fg=self.text_color
        )

        search_label.pack(
            pady=(20, 10)
        )

        # ==============================
        # Input Area
        # ==============================

        input_frame = tk.Frame(
            search_card,
            bg=self.card_color
        )

        input_frame.pack()

        self.movie_entry = tk.Entry(
            input_frame,
            width=42,
            font=("Arial", 13),
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief="flat"
        )

        self.movie_entry.pack(
            side="left",
            ipady=10,
            padx=(0, 10)
        )

        # Placeholder
        self.placeholder = "Example: Interstellar"

        self.movie_entry.insert(
            0,
            self.placeholder
        )

        self.movie_entry.config(
            fg=self.secondary_text
        )

        self.movie_entry.bind(
            "<FocusIn>",
            self.remove_placeholder
        )

        self.movie_entry.bind(
            "<FocusOut>",
            self.restore_placeholder
        )

        self.movie_entry.bind(
            "<Return>",
            lambda event: self.get_recommendations()
        )

        # ==============================
        # Recommend Button
        # ==============================

        self.recommend_button = tk.Button(
            input_frame,
            text="🔍  Recommend",
            font=("Arial", 12, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
            command=self.get_recommendations
        )

        self.recommend_button.pack(
            side="left"
        )

        self.recommend_button.bind(
            "<Enter>",
            lambda event: self.recommend_button.config(
                bg=self.button_hover
            )
        )

        self.recommend_button.bind(
            "<Leave>",
            lambda event: self.recommend_button.config(
                bg=self.button_color
            )
        )

        # ==============================
        # Results Header
        # ==============================

        results_header = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        results_header.pack(
            fill="x",
            padx=70,
            pady=(10, 10)
        )

        self.result_title = tk.Label(
            results_header,
            text="Recommended Movies",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )

        self.result_title.pack(
            side="left"
        )

        self.clear_button = tk.Button(
            results_header,
            text="Clear",
            font=("Arial", 10, "bold"),
            bg=self.input_color,
            fg=self.text_color,
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self.clear_results
        )

        self.clear_button.pack(
            side="right"
        )

        # ==============================
        # Results Container
        # ==============================

        results_container = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        results_container.pack(
            fill="both",
            expand=True,
            padx=70
        )

        # Canvas
        self.canvas = tk.Canvas(
            results_container,
            bg=self.bg_color,
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scrollbar
        scrollbar = tk.Scrollbar(
            results_container,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.results_frame = tk.Frame(
            self.canvas,
            bg=self.bg_color
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.results_frame,
            anchor="nw"
        )

        self.results_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        # ==============================
        # Initial Message
        # ==============================

        self.show_initial_message()

    # =========================================================
    # Placeholder Functions
    # =========================================================

    def remove_placeholder(self, event):

        if self.movie_entry.get() == self.placeholder:

            self.movie_entry.delete(
                0,
                tk.END
            )

            self.movie_entry.config(
                fg=self.text_color
            )

    def restore_placeholder(self, event):

        if not self.movie_entry.get().strip():

            self.movie_entry.insert(
                0,
                self.placeholder
            )

            self.movie_entry.config(
                fg=self.secondary_text
            )

    # =========================================================
    # Initial Message
    # =========================================================

    def show_initial_message(self):

        message = tk.Label(
            self.results_frame,
            text="Enter a movie name above to get recommendations.",
            font=("Arial", 13),
            bg=self.bg_color,
            fg=self.secondary_text
        )

        message.pack(
            pady=40
        )

    # =========================================================
    # Clear Results
    # =========================================================

    def clear_results(self):

        self.movie_entry.delete(
            0,
            tk.END
        )

        self.movie_entry.insert(
            0,
            self.placeholder
        )

        self.movie_entry.config(
            fg=self.secondary_text
        )

        for widget in self.results_frame.winfo_children():

            widget.destroy()

        self.result_title.config(
            text="Recommended Movies"
        )

        self.show_initial_message()

    # =========================================================
    # Resize Canvas
    # =========================================================

    def resize_canvas(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # =========================================================
    # Get Recommendations
    # =========================================================

    def get_recommendations(self):

        movie_name = self.movie_entry.get().strip()

        # Check placeholder
        if movie_name == self.placeholder:

            movie_name = ""

        # Check empty input
        if not movie_name:

            messagebox.showwarning(
                "Movie Required",
                "Please enter a movie name."
            )

            return

        # Get recommendations
        recommendations = self.recommender.recommend(
            movie_name,
            5
        )

        # Movie not found
        if not recommendations:

            messagebox.showerror(
                "Movie Not Found",
                f"'{movie_name}' was not found in the dataset.\n\n"
                "Try a movie such as:\n"
                "Interstellar\n"
                "Inception\n"
                "The Martian"
            )

            return

        # Clear old results
        for widget in self.results_frame.winfo_children():

            widget.destroy()

        # Update title
        self.result_title.config(
            text=f"Movies Similar to '{movie_name}'"
        )

        # Create recommendation cards
        for index, movie in enumerate(
            recommendations,
            start=1
        ):

            self.create_movie_card(
                index,
                movie
            )

        # Scroll to top
        self.canvas.yview_moveto(0)

    # =========================================================
    # Movie Card
    # =========================================================

    def create_movie_card(self, index, movie):

        card = tk.Frame(
            self.results_frame,
            bg=self.result_color,
            height=90
        )

        card.pack(
            fill="x",
            pady=6
        )

        card.pack_propagate(False)

        # ==============================
        # Rank
        # ==============================

        rank = tk.Label(
            card,
            text=f"{index}",
            font=("Arial", 18, "bold"),
            bg=self.result_color,
            fg="#fbbf24",
            width=3
        )

        rank.pack(
            side="left",
            padx=(15, 5)
        )

        # ==============================
        # Movie Information
        # ==============================

        info = tk.Frame(
            card,
            bg=self.result_color
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=12
        )

        movie_title = tk.Label(
            info,
            text=movie["title"],
            font=("Arial", 15, "bold"),
            bg=self.result_color,
            fg=self.text_color,
            anchor="w"
        )

        movie_title.pack(
            fill="x"
        )

        details = tk.Label(
            info,
            text=f"🎭 {movie['genre']}    ⭐ Rating: {movie['rating']}",
            font=("Arial", 10),
            bg=self.result_color,
            fg=self.secondary_text,
            anchor="w"
        )

        details.pack(
            fill="x",
            pady=(5, 0)
        )

        # ==============================
        # Similarity
        # ==============================

        similarity_frame = tk.Frame(
            card,
            bg=self.result_color,
            width=150
        )

        similarity_frame.pack(
            side="right",
            fill="y",
            padx=15
        )

        similarity_frame.pack_propagate(False)

        similarity_label = tk.Label(
            similarity_frame,
            text="SIMILARITY",
            font=("Arial", 8, "bold"),
            bg=self.result_color,
            fg=self.secondary_text
        )

        similarity_label.pack(
            pady=(18, 2)
        )

        similarity_value = tk.Label(
            similarity_frame,
            text=f"{movie['similarity']}%",
            font=("Arial", 16, "bold"),
            bg=self.result_color,
            fg="#34d399"
        )

        similarity_value.pack()

        # Hover effect
        self.add_card_hover(
            card,
            info,
            rank,
            details,
            movie_title,
            similarity_frame,
            similarity_label,
            similarity_value
        )

    # =========================================================
    # Card Hover Effect
    # =========================================================

    def add_card_hover(self, *widgets):

        def enter(event):

            for widget in widgets:

                widget.config(
                    bg="#334155"
                )

        def leave(event):

            for widget in widgets:

                widget.config(
                    bg=self.result_color
                )

        for widget in widgets:

            widget.bind(
                "<Enter>",
                enter
            )

            widget.bind(
                "<Leave>",
                leave
            )


# =============================================================
# Start Application
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MovieRecommendationApp(
        root
    )

    root.mainloop()
