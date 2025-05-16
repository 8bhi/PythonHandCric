import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import mysql.connector as s

class CricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Game")
        self.root.configure(bg='black')
        
        # Game variables
        self.uteam = ""
        self.team = ""
        self.runs_1 = 0
        self.wickets_1 = 0
        self.balls_1 = 0
        self.runs_2 = 0
        self.wickets_2 = 0
        self.balls_2 = 0
        self.Bat_first = ""
        self.Ball_first = ""
        self.Bat_second = ""
        self.u_opt = ""
        self.c_opt = ""
        
        # Configure styles
        self.big_font = ('Helvetica', 14)
        self.medium_font = ('Helvetica', 12)
        self.small_font = ('Helvetica', 10)
        
        self.setup_welcome_screen()
    
    def setup_welcome_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Welcome message
        welcome_label = tk.Label(self.root, 
                                text="~~~~~~~~~~ Game of Cricket ~~~~~~~~~~",
                                font=self.big_font, fg='white', bg='black')
        welcome_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Text(self.root, height=20, width=80, 
                              font=self.small_font, fg='white', bg='black',
                              relief=tk.FLAT, wrap=tk.WORD)
        instructions.pack(pady=10, padx=20)
        
        instructions.insert(tk.END, "Instructions:\n\n")
        instructions.insert(tk.END, "1. You have to select any random number from 1 to 6.\n")
        instructions.insert(tk.END, "2. The computer will also select a number.\n")
        instructions.insert(tk.END, "3. While batting, if the number selected by you and computer is different, then your number will add to your runs.\n")
        instructions.insert(tk.END, "   If the number selected by you and computer is same, then you will lose your wicket.\n")
        instructions.insert(tk.END, "4. While bowling, if the number selected by you and computer is different, then the computer's number will add to its runs.\n")
        instructions.insert(tk.END, "   If the number selected by you and computer is same, then the computer will lose its wicket.\n")
        instructions.insert(tk.END, "5. Each player will get 2 wickets and 2 overs (12 balls) for batting and bowling.\n")
        instructions.insert(tk.END, "6. The innings will end after either the three wickets fell or the overs end.\n")
        instructions.insert(tk.END, "7. The player with maximum runs wins.\n")
        instructions.configure(state='disabled')
        
        # Start button
        start_btn = tk.Button(self.root, text="Start Game", font=self.medium_font,
                            command=self.start_game, bg='gray', fg='white')
        start_btn.pack(pady=20)
    
    def start_game(self):
        # Get team name
        self.uteam = simpledialog.askstring("Team Name", "Enter your team name:", parent=self.root)
        if not self.uteam:
            self.uteam = "Player"
        self.team = self.uteam + "_vs_computer"
        
        self.do_toss()
    
    def do_toss(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Toss interface
        toss_label = tk.Label(self.root, text="Here comes the Toss", 
                             font=self.big_font, fg='white', bg='black')
        toss_label.pack(pady=20)
        
        toss_question = tk.Label(self.root, text="Choose heads or tails (h/t):", 
                                font=self.medium_font, fg='white', bg='black')
        toss_question.pack()
        
        self.toss_entry = tk.Entry(self.root, font=self.medium_font)
        self.toss_entry.pack(pady=10)
        self.toss_entry.focus_set()
        
        toss_btn = tk.Button(self.root, text="Submit", font=self.medium_font,
                           command=self.process_toss, bg='gray', fg='white')
        toss_btn.pack(pady=20)
        
        # Bind Enter key to toss submission
        self.root.bind('<Return>', lambda event: self.process_toss())
    
    def process_toss(self):
        toss = self.toss_entry.get().lower()
        
        if toss not in ['h', 't']:
            return
        
        random_toss = random.randint(1, 2)  # 1=Heads, 2=Tails
        random_opt = random.randint(1, 2)   # 1=bat, 2=ball
        
        if (random_toss == 1 and toss == "h") or (random_toss == 2 and toss == "t"):
            # User won toss
            self.u_opt = simpledialog.askstring("Choose", "You won the toss!\nChoose bat or ball:").lower()
            if self.u_opt not in ['bat', 'ball']:
                return
        else:
            # Computer won toss
            self.c_opt = "bat" if random_opt == 1 else "ball"
            messagebox.showinfo("Toss Result", f"Computer chooses to {self.c_opt}")
        
        self.setup_innings(1)
    
    def setup_innings(self, innings):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        title_text = f"---------- Innings {innings} ----------"
        title_label = tk.Label(self.root, text=title_text, 
                              font=self.big_font, fg='white', bg='black')
        title_label.pack(pady=10)
        
        # Determine batting and bowling teams
        if innings == 1:
            if self.u_opt == "bat" or self.c_opt == "ball":
                self.Bat_first = "You"
                self.Ball_first = "Computer"
            elif self.u_opt == "ball" or self.c_opt == "bat":
                self.Bat_first = "Computer"
                self.Ball_first = "You"
            
            batting_label = tk.Label(self.root, text=f"{self.Bat_first} are batting first", 
                                   font=self.medium_font, fg='white', bg='black')
            batting_label.pack()
            
            self.runs_1 = 0
            self.wickets_1 = 0
            self.balls_1 = 0
        else:
            batting_label = tk.Label(self.root, text=f"{self.Ball_first} are now batting", 
                                    font=self.medium_font, fg='white', bg='black')
            batting_label.pack()
            
            target_label = tk.Label(self.root, 
                                  text=f"Target: {self.runs_1 + 1} runs", 
                                  font=self.medium_font, fg='white', bg='black')
            target_label.pack()
            
            self.runs_2 = 0
            self.wickets_2 = 0
            self.balls_2 = 0
        
        # Score display frame
        score_frame = tk.Frame(self.root, bg='black')
        score_frame.pack(pady=10)
        
        self.score_var = tk.StringVar()
        self.update_score_display(innings)
        
        score_label = tk.Label(score_frame, textvariable=self.score_var, 
                              font=self.big_font, fg='white', bg='black')
        score_label.pack()
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='black')
        input_frame.pack(pady=10)
        
        num_label = tk.Label(input_frame, text="Choose a number (1-6):", 
                            font=self.medium_font, fg='white', bg='black')
        num_label.grid(row=0, column=0, padx=5)
        
        self.num_entry = tk.Entry(input_frame, font=self.medium_font, width=5)
        self.num_entry.grid(row=0, column=1, padx=5)
        self.num_entry.focus_set()
        
        submit_btn = tk.Button(input_frame, text="Submit", font=self.medium_font,
                              command=lambda: self.play_ball(innings), 
                              bg='gray', fg='white')
        submit_btn.grid(row=0, column=2, padx=5)
        
        # Ball result display
        self.result_var = tk.StringVar()
        self.result_var.set("")
        result_label = tk.Label(self.root, textvariable=self.result_var, 
                               font=self.medium_font, fg='white', bg='black')
        result_label.pack(pady=10)
        
        # Bind Enter key to play ball
        self.root.bind('<Return>', lambda event: self.play_ball(innings))
    
    def play_ball(self, innings):
        try:
            u_choice = int(self.num_entry.get())
            if u_choice < 1 or u_choice > 6:
                self.result_var.set("Please enter a number between 1 and 6")
                return
        except ValueError:
            self.result_var.set("Please enter a valid number")
            return
        
        c_choice = random.randint(1, 6)
        
        if innings == 1:
            if u_choice == c_choice:
                self.wickets_1 += 1
                result = f"OUT! {'You' if self.Bat_first == 'You' else 'Computer'} lost a wicket."
            else:
                if self.Bat_first == "You":
                    self.runs_1 += u_choice  # User batting - count user's number
                else:
                    self.runs_1 += c_choice  # Computer batting - count computer's number
                result = f"Runs scored: {u_choice if self.Bat_first == 'You' else c_choice}"
            
            self.balls_1 += 1
            
            # Update ball result
            self.result_var.set(f"Your choice: {u_choice} | Computer's choice: {c_choice}\n{result}")
            
            # Update score display
            self.update_score_display(innings)
            
            # Check if innings should end
            if self.wickets_1 >= 2 or self.balls_1 >= 12:
                self.end_innings(1)
            else:
                self.num_entry.delete(0, tk.END)
                self.num_entry.focus_set()
        else:
            if u_choice == c_choice:
                self.wickets_2 += 1
                result = f"OUT! {'Computer' if self.Ball_first == 'Computer' else 'You'} lost a wicket."
            else:
                if self.Ball_first == "Computer":
                    self.runs_2 += c_choice  # Computer batting - count computer's number
                else:
                    self.runs_2 += u_choice  # User batting - count user's number
                result = f"Runs scored: {c_choice if self.Ball_first == 'Computer' else u_choice}"
            
            self.balls_2 += 1
            
            # Update ball result
            self.result_var.set(f"Your choice: {u_choice} | Computer's choice: {c_choice}\n{result}")
            
            # Update score display
            self.update_score_display(innings)
            
            # Check if innings should end
            if (self.wickets_2 >= 2 or self.balls_2 >= 12 or 
                (self.Ball_first == "Computer" and self.runs_2 > self.runs_1) or
                (self.Ball_first == "You" and self.runs_2 > self.runs_1)):
                self.end_innings(2)
            else:
                self.num_entry.delete(0, tk.END)
                self.num_entry.focus_set()
    
    def update_score_display(self, innings):
        if innings == 1:
            score_text = (f"{self.Bat_first} Batting\n"
                         f"Score: {self.runs_1}/{self.wickets_1}\n"
                         f"Balls: {self.balls_1}/12")
        else:
            score_text = (f"{self.Ball_first} Batting\n"
                        f"Score: {self.runs_2}/{self.wickets_2}\n"
                        f"Balls: {self.balls_2}/12\n"
                        f"Target: {self.runs_1 + 1}\n"
                        f"Need: {max(0, (self.runs_1 + 1) - self.runs_2)} from {12 - self.balls_2} balls")
        
        self.score_var.set(score_text)
    
    def end_innings(self, innings):
        if innings == 1:
            messagebox.showinfo("End of Innings", 
                              f"End of First Innings\n{self.Bat_first} scored {self.runs_1}/{self.wickets_1}")
            self.setup_innings(2)
        else:
            messagebox.showinfo("End of Innings", 
                              f"End of Second Innings\n{self.Ball_first} scored {self.runs_2}/{self.wickets_2}")
            self.show_result()
    
    def show_result(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        result_label = tk.Label(self.root, text="~~~~~~~~~~ Result ~~~~~~~~~~", 
                              font=self.big_font, fg='white', bg='black')
        result_label.pack(pady=20)
        
        if self.runs_1 > self.runs_2:
            if self.Bat_first == "You":
                result_text = f"Congratulations! {self.uteam} won by {self.runs_1 - self.runs_2} runs."
            else:
                result_text = f"Computer won by {self.runs_1 - self.runs_2} runs."
        elif self.runs_2 > self.runs_1:
            if self.Ball_first == "You":
                result_text = f"Congratulations! {self.uteam} won by {2 - self.wickets_2} wickets."
            else:
                result_text = f"Computer won by {2 - self.wickets_2} wickets."
        else:
            result_text = "The match is a tie!"
        
        result_display = tk.Label(self.root, text=result_text, 
                                font=self.medium_font, fg='white', bg='black')
        result_display.pack(pady=20)
        
        # Score summary
        summary_text = (f"\nFirst Innings: {self.Bat_first} - {self.runs_1}/{self.wickets_1}\n"
                       f"Second Innings: {self.Ball_first} - {self.runs_2}/{self.wickets_2}")
        
        summary_label = tk.Label(self.root, text=summary_text,
                               font=self.small_font, fg='white', bg='black')
        summary_label.pack(pady=10)
        
        # Store results in database
        self.store_results()
        
        # Play again button
        play_again_btn = tk.Button(self.root, text="Play Again", font=self.medium_font,
                                 command=self.setup_welcome_screen, bg='gray', fg='white')
        play_again_btn.pack(pady=20)
        
        # Exit button (now properly closes the window)
        exit_btn = tk.Button(self.root, text="Exit", font=self.medium_font,
                           command=self.root.destroy, bg='gray', fg='white')
        exit_btn.pack(pady=10)
    
    def store_results(self):
        try:
            mycon = s.connect(host="localhost", user="root", passwd="cs208@08", database="cric")
            cursor = mycon.cursor()
            
            # Create table if not exists
            query = f'CREATE TABLE IF NOT EXISTS {self.team} (Player char(30), Runs int, Wicket int)'
            cursor.execute(query)
            
            # Insert data
            q = f'INSERT INTO {self.team} (Player, Runs, Wicket) VALUES (%s, %s, %s)'
            L = [(self.Bat_first, self.runs_1, self.wickets_1), 
                (self.Ball_first, self.runs_2, self.wickets_2)]
            
            for i in L:
                cursor.execute(q, i)
            
            mycon.commit()
            
            # Ask user if they want to clear the table
            response = messagebox.askyesno("Database", "Table created successfully.\nDo you want to clear the table?")
            if response:
                cursor.execute(f'DROP TABLE {self.team}')
                mycon.commit()
            
            cursor.close()
            mycon.close()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    game = CricketGame(root)
    root.mainloop()
