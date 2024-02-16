# Pydoku

<figure>
    <blockquote>
        <i>One could say life is like a Sudoku game, you take it one square at a time.</i>
    </blockquote>
</figure>

<h1>Introduction</h1>

I had always been a fan of solving sudoku puzzles ever since my friend showed how to do them in school. At that time, our school was trying to get us acquainted with reading newspapers because well, why not? So they provided us with them from local prints (and it wasn't for free, though I am not complaining), and they also gave us oppurtunities to write articles for these newspaper for our classmates to read. It did actually incentivise us for checking out all the different stuff that was written about. But what was even more popular was the comics section and the puzzles section, which included a crossword puzzle and a (apparently medium difficult) Sudoku puzzle, which at the time I had no idea how to solve. So it was a great thing when it started to get popular amongst us, and I ended up learning it from a very good friend of mine. 

Before, I used to find the entire thing completely alien, and the few tries that I ever gave when I was little was filled with me just placing numbers in random spots, hoping it will somehow get magically solved. But alas, that never happened. After I was shown how it may be solved by understanding the rules of the puzzle and observing the clues given to me, it suddenly clicked. And I was successfully introduced to the world of Sudoku solving. I used to solve it everyday since when the newspaper came. After I got my phone, I downloaded a Sudoku app and used to just solve puzzles whenever I was free, when I was taking the bus back home from college, whenever it was possible.

I always had a great fascination for game development, and I always wanted to create my own games. However, I never did anything of the sort and at this time, I am very new to this. In fact, this is my first time I even made a full fledged game, and I chose it to be about Sudoku because of the impact that it was able to have on me. I took the principles of the ways in which Sudoku puzzle are solved and applied it to my life, and it lead me to pursuing Computer Science, and I would forever be grateful to this 9x9 grid puzzle.<br>

<h1>Details</h1>

<b>NOTE 1:</b> Although I included the option, the impossible does not at this time generate any puzzle. This is because of the way the Sudoku generation algorithm works, and I may work to find a solution for this in the future.

<b>NOTE 2:</b> I chose to make this game in Python since I am more accustomed to it, and it was really convinient to use modules like the Pygame Module for most of the stuff. I am also learning the OpenGL and SDL frameworks, so I may recreate the game with these frameworks.

This is a standard Sudoku Game, where the user is presented with a randomly generated puzzle based on a difficulity chosen by them. I made two versions of this, one is terminal based, which I made when I was just starting with coding, so it may not look its best and may have a whole lot of repeated code, and is not too much user friendly, but I really liked the final UI look (although I am a bad judge, my brother sure didn't like it), and the other is made using Pygame, and the code is much more clean as a result.

Both of these games have been given music (all of them taken from pixabay) and have different UIs. I will try and highlight the main ones:-

<table>
    <tr>
        <th>Terminal Based</th>
        <th>Pygame Based</th>
    </tr>
    <tr>
        <td>Keyboard Input</td>
        <td>Mouse Input</td>
    </tr>
    <tr>
        <td>Has a Score System</td>
        <td>Currently does not have a Score System</td>
    </tr>
    <tr>
        <td>Shows Solution on defeat</td>
        <td>Did not implement this feature</td>
    </tr>
    <tr>
        <td>No Restart/New Game/Pause Options</td>
        <td>Restart/New Game/Pause Options Available</td>
    </tr>
    <tr>
        <td>Does not have a Timer</td>
        <td>Timer Available</td>
    </tr>
    <tr>
        <td>Terminal Themed</td>
        <td>Newspaper Themed</td>
    </tr>
    <tr>
        <td>Works on Linux perfectly, may not work as well on Windows</td>
        <td>Works on Linux and Windows</td>
    </tr>
</table><br>

<h1>How to Use</h1>

<h3>Terminal Sudoku</h3>
To use the terminal sudoku, download the SudokuTerminal folder, and run the sudokuPlayer.py script. Alternatively, you could use pyinstaller to convert the script to an .exe file for this, just remember to use a spec file to account for the content folder.

<h3>Pygame Sudoku</h3>
To use the pygame version, download the SudokuGame folder and run the player.py script. Or you may convert it to an .exe file using pyinstaller. 

<h1>Preview</h1>

<figure>
    <img src = ".\__doc_pics\TSH.png">
    <figcaption><i>Terminal Sudoku Home Screen</i></figcaption>
</figure>
<br>
<figure>
    <img src = ".\__doc_pics\TSG.png">
    <figcaption><i>Terminal Sudoku Gameplay</i></figcaption>
</figure>
<br>
<figure>
    <img src = ".\__doc_pics\PSH.png">
    <figcaption><i>Pygame Sudoku Home Screen</i><figcaption>
</figure>
<br>
<figure>
    <img src = ".\__doc_pics\PSG.png">
    <figcaption><i>Pygame Sudoku Gameplay</i><figcaption>
</figure>

<h1>Reference</h1>
All sounds have been taken from the <a href = "https://pixabay.com/">pixabay website</a>.<br>
Copperplate font taken from <a href = "https://fontmeme.com/fonts/copperplate-font/">here</a>