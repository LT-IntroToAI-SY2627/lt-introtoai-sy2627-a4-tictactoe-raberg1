"""A graphical Tic Tac Toe game for two people or one person vs. the computer."""

import random
import tkinter as tk

from a4 import TTTBoard


class TicTacToeGUI:
    """Provide a graphical interface for local and computer games."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        self.board = TTTBoard()
        self.current_player = "X"
        self.game_finished = False
        self.mode = tk.StringVar(value="Two Players")
        self.pending_computer_move: str | None = None
        self.computer_thinking = False

        tk.Label(
            root,
            text="Tic Tac Toe",
            font=("Segoe UI", 22, "bold"),
            pady=12,
        ).pack()
        tk.OptionMenu(
            root,
            self.mode,
            "Two Players",
            "Play Computer",
            command=self.change_mode,
        ).pack()
        self.status = tk.StringVar(value="Player X's turn")
        tk.Label(
            root,
            textvariable=self.status,
            font=("Segoe UI", 13),
            pady=6,
        ).pack()

        board_frame = tk.Frame(root, padx=14, pady=8)
        board_frame.pack()
        self.buttons = []
        for position in range(9):
            button = tk.Button(
                board_frame,
                text="",
                font=("Segoe UI", 28, "bold"),
                width=4,
                height=1,
                bg="white",
                activebackground="#e8eef5",
                relief=tk.RAISED,
                command=lambda cell=position: self.play_move(cell),
            )
            button.grid(
                row=position // 3,
                column=position % 3,
                padx=4,
                pady=4,
                ipady=8,
            )
            self.buttons.append(button)

        tk.Button(
            root,
            text="New Game",
            font=("Segoe UI", 11),
            command=self.new_game,
            padx=12,
            pady=5,
        ).pack(pady=(4, 16))

    def play_move(self, position: int) -> None:
        """Make the current player's move and update the game display."""
        if self.game_finished or self.computer_thinking or not self.board.make_move(
            self.current_player, position
        ):
            return

        self._show_move(position, self.current_player)
        self._advance_game()

    def _show_move(self, position: int, player: str) -> None:
        """Display a move and disable its square."""
        self.buttons[position].config(
            text=player,
            fg="#1769aa" if player == "X" else "#b23a48",
            disabledforeground="#1769aa" if player == "X" else "#b23a48",
            state=tk.DISABLED,
        )

    def _advance_game(self) -> None:
        """Check the last move and either finish or hand over the turn."""
        last_player = self.current_player
        if self.board.has_won(last_player):
            winner = (
                "Computer"
                if self.mode.get() == "Play Computer" and last_player == "O"
                else f"Player {last_player}"
            )
            self.status.set(f"{winner} wins!")
            self.game_finished = True
        elif self.board.game_over():
            self.status.set("It's a draw!")
            self.game_finished = True
        else:
            self.current_player = "O" if last_player == "X" else "X"
            if self.mode.get() == "Play Computer" and self.current_player == "O":
                self.status.set("Computer's turn...")
                self.computer_thinking = True
                self.pending_computer_move = self.root.after(
                    350, self._play_computer_move
                )
            else:
                self.status.set(f"Player {self.current_player}'s turn")

        if self.game_finished:
            for remaining_button in self.buttons:
                remaining_button.config(state=tk.DISABLED)

    def _play_computer_move(self) -> None:
        """Have the computer make one legal move."""
        self.pending_computer_move = None
        if self.game_finished or self.mode.get() != "Play Computer":
            self.computer_thinking = False
            return

        position = self._choose_computer_move()
        self.board.make_move("O", position)
        self._show_move(position, "O")
        self.computer_thinking = False
        self._advance_game()

    def _choose_computer_move(self) -> int:
        """Choose a winning move, sometimes block, or play randomly."""
        available = [
            position
            for position, square in enumerate(self.board.board)
            if square == "*"
        ]
        winning_move = self._find_immediate_move("O", available)
        if winning_move is not None:
            return winning_move

        blocking_move = self._find_immediate_move("X", available)
        if blocking_move is not None and random.random() < 0.5:
            return blocking_move

        return random.choice(available)

    def _find_immediate_move(self, player: str, available: list[int]) -> int | None:
        """Return a square that lets player win immediately, if one exists."""
        for position in available:
            test_board = TTTBoard()
            test_board.board = self.board.board.copy()
            test_board.make_move(player, position)
            if test_board.has_won(player):
                return position
        return None

    def change_mode(self, mode: str) -> None:
        """Switch game mode and start a fresh game."""
        self.mode.set(mode)
        self.new_game()

    def new_game(self) -> None:
        """Reset the board and start again with player X."""
        if self.pending_computer_move is not None:
            self.root.after_cancel(self.pending_computer_move)
            self.pending_computer_move = None
        self.board.clear()
        self.current_player = "X"
        self.game_finished = False
        self.computer_thinking = False
        self.status.set("Player X's turn")
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL, fg="black")


def main() -> None:
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
