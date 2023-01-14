from kivy.lang import Builder
from kivymd.app import MDApp


class GameApp(MDApp):
    title = "Tic Tac Toe"
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('TicTacToe.kv')

    # Define Turn (X - 1, Y - 0)
    turn = 1
    # Rows, Cols
    rows = 3
    cols = 3
    # Wins Tracking
    x_wins = 0
    o_wins = 0

    def matrix(self):
        # Widget Text List
        wid_lst = []
        # Game Matrix
        gmatrix = []
        # Convert id's value dictionary to list
        for i in self.root.ids:
            "" if i == "my_layout" else wid_lst.append(self.root.ids[i])
        # Building the Matrix
        for i in range(self.rows*self.cols): # of all the buttons
            gmatrix.append(wid_lst[i]) 
        return gmatrix

    # Update the won text
    def ending(self, x, y, z):
        if x.text == "X":
            x.color = 'red'
            y.color = 'red'
            z.color = 'red'
        if x.text == "O":
            x.color = (0, 1, 0, 1)
            y.color = (0, 1, 0, 1)
            z.color = (0, 1, 0, 1)

    def win(self, lst):
        # Across
        for i in range(0, 9, 3):
            if lst[i].text == lst[i+1].text == lst[i+2].text == "X":
                self.ending(lst[i], lst[i+1], lst[i+2])
                return "X"
            if lst[i].text == lst[i+1].text == lst[i+2].text == "O":
                self.ending(lst[i], lst[i+1], lst[i+2])
                return "O"
        # Down
        for i in range(3):
            if lst[i].text == lst[i+3].text == lst[i+6].text =="X":
                self.ending(lst[i], lst[i+3], lst[i+6])
                return "X"
            if lst[i].text == lst[i+3].text == lst[i+6].text =="O":
                self.ending(lst[i], lst[i+3], lst[i+6])
                return "O"
        
        # Left Diagonal
        if lst[0].text == lst[4].text == lst[8].text == "X":
            self.ending(lst[0], lst[4], lst[8])
            return "X"  
        if lst[0].text == lst[4].text == lst[8].text == "O":
            self.ending(lst[0], lst[4], lst[8])
            return "O"

        # Right Diagonal
        if lst[2].text == lst[4].text == lst[6].text == "X":
            self.ending(lst[2], lst[4], lst[6])
            return "X"
        if lst[2].text == lst[4].text == lst[6].text == "O":
            self.ending(lst[2], lst[4], lst[6])
            return "O"
        
    def tie(self):
        current_game = self.matrix() # Return a list of current game matrix
        for i in current_game:
            if i.text == "":
                return
        # If all not empty
        self.root.ids.update_label.bold = True
        self.root.ids.update_label.color = (242/255, 224/255, 109/255, 1)
        self.root.ids.update_label.text = "TIE GAME"

    def see_id(self, instance):
        #for i in self.root.ids:
        #    print(self.root.ids[i].text) 
            # i = btn1, btn2..., update_label, restart -> string
            # self.root.ids[i].text --> get all text from widget which have an id
            # self.root.ids.btn1 = instance
        # Access Widget instance/object
        print(self.root.ids.btn1)
        print(self.root.ids["btn1"])

    def presser(self, btn):
        if self.turn:
            btn.text = "X"
            self.root.ids.update_label.text = "O's Turn"
            self.turn = 0       
        else:
            btn.text = "O"
            self.root.ids.update_label.text = "X's Turn"
            self.turn = 1
        btn.disabled = True # Disable the button
        
        # Check and enable Win condition   
        current_game = self.matrix() # Return a list of current game matrix

        # Check and enable Tie condition
        self.tie() 
        """self.tie() is put here so even if the board is full, but 
        there is a winner, the winner label is still updated below"""

        # Update the Win label
        result = self.win(current_game)
        if result:
            self.root.ids.update_label.bold = True
            for i in current_game:
                i.disabled = True

            if result == "X":
                self.root.ids.update_label.text = "X WON"
                self.root.ids.update_label.color = (1, 0, 0, 1)
                self.x_wins += 1

            elif result == "O":
                self.root.ids.update_label.text = "O WON"
                self.root.ids.update_label.color = (0, 1, 0, 1)
                self.o_wins += 1

        # Update Score
        self.root.ids.score_label.text = f"X Wins: {self.x_wins}  |  O Wins: {self.o_wins}"
            
    def restart(self):
        # Accessing all widgets
        for i in self.root.ids:
            # Enable Buttons
            self.root.ids[i].disabled = False
            # Clear Buttons
            self.root.ids[i].text = ""
            # Reset Label text attributes
            self.root.ids.update_label.color = (1, 1, 1, 1)
            self.root.ids.update_label.bold = False
            # Reset Buttons text attributes
            self.root.ids[i].color = (1, 1, 1, 1) # Any color is possible

        # Reset Turn    
        self.turn = 1
        # Reset Text
        self.root.ids.update_label.text = "X GOES FIRST"
        self.root.ids.restart.text = "Restart The Game"
        self.root.ids.score_label.text = f"X Wins: {self.x_wins}  |  O Wins: {self.o_wins}"


GameApp().run()