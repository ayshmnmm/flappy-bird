import os
import random
import time
import tkinter
import turtle
import pickle
from config import *

# Root window
root = tkinter.Tk()
root.title('Flappy Bird')
root.geometry('500x600')
root.resizable(0, 0)
local_dir = os.path.dirname(__file__)
icon = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/icon.png"))
root.iconphoto(False, icon)

# Frames
menu = tkinter.Frame(root, height=600, width=500)
game = tkinter.Frame(root, height=600, width=500)
highscore = tkinter.Frame(root, height=600, width=500, background='light sea green')
gameover = tkinter.Frame(root, height=600, width=500, background='light sea green')
menu.place(x=0, y=0)
game.place(x=0, y=0)
highscore.place(x=0, y=0)
gameover.place(x=0, y=0)
menu.tkraise() 

# Game menu
menubg = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/menubg.png"))
bg = tkinter.Label(menu, image=menubg)
bg.place(x=-2, y=-2)
playimg = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/playbtn.png")).subsample(4, 4)
tkinter.Button(menu, text="Play!", image=playimg, height=50, width=80, command=lambda: new_game()).place(x=140, y=400)
hsimg = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/hsbtn.png")).subsample(4, 4)
tkinter.Button(menu, text="Play!", image=hsimg, height=50, width=80, command=lambda: display_hs()).place(x=280, y=400)


c = tkinter.Canvas(game, height=600, width=500)
c.pack()
score = 0
texth = ''

# HIGHSCORE IMPLEMENTATION
try:
    f = open(os.path.join(local_dir, "scores.txt"),'rb')
    highscores = pickle.load(f)
except:
    f = open(os.path.join(local_dir, "scores.txt"),'wb')
    highscores = []
    pickle.dump(highscores,f)

# Save highscores to scores.txt
def save_hs(score,name):
    get_hsbtn.config(state='disabled') 
    highscores.append((name,score))
    f = open(os.path.join(local_dir, "scores.txt"),'wb')
    pickle.dump(sorted(highscores, key = lambda h : h[-1], reverse=True)[:10],f)

# Check if score is valid highscore    
def check_hs(score):
    scores = []
    sorths = sorted(highscores, key = lambda h : h[-1], reverse=True)[:10]
    for i in sorths:
        scores.append(i[1])
    if score== 0:
        return False
    if len(sorths)==0 and score!=0:
        return True
    elif score >= min(scores) and score != 0:
        if len(sorths)==10 and score == scores[-1]:
            return False
        else:
            return True
    elif len(sorths)<10:
        return True
    else:
        return False

# Display highscores
def display_hs():
    global texth
    texth = ''
    for i in sorted(highscores, key = lambda h : h[-1], reverse=True)[:10]:
        texth += i[0] + ' : ' + str(i[1]) + '\n'
    hslabel.config(text=texth)
    highscore.tkraise()

# Highscore
tkinter.Label(highscore, text="Highscores", font=("courier", 20), bg='light sea green').place(x=167, y=30)
hslabel = tkinter.Label(highscore, text=texth, font=("courier", 20), bg='light sea green')
hslabel.place(x=167, y=100)
back_menuimg = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/menubtn.png")).subsample(3, 3)
tkinter.Button(highscore, text="Back", image=back_menuimg, borderwidth=0, command=lambda: menu.tkraise(), bg='light sea green').place(x=185, y=500)

# Gameover
menubg2 = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/gameover.png"))
bg2 = tkinter.Label(gameover, image=menubg2)
bg2.place(x=-2, y=-2)
score_label = tkinter.Label(gameover, font=("courier", 20), bg='light sea green')
score_label.place(x=135, y=230)
get_hs = tkinter.Entry(gameover)
get_hs.place(x=180, y=322)
get_hsbtn = tkinter.Button(gameover, text='Save', command=lambda: save_hs(score,get_hs.get()))
get_hsbtn.place(x=310, y=320)
restartbtn = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/restartbtn.png")).subsample(3, 3)
tkinter.Button(gameover, text="Back", image=back_menuimg, borderwidth=0, command=lambda: menu.tkraise(), bg='light sea green').place(x=280, y=400)
tkinter.Button(gameover, text="restart", image=restartbtn, borderwidth=0, command=lambda: new_game(), bg='light sea green').place(x=100, y=400)
tkinter.Button(gameover, text="hs", image=hsimg, height=50, width=80, command=lambda: display_hs()).place(x=210, y=500)


# Reset everything and start a new game
def new_game():
    global score
    score = 0
    a = 'bird1'
    ant = 0
    collided = False
    first_jump = False 

    images = {'bird1':['bird1_up','bird1'],'bird2':['bird2_up','bird2','bird2_down'],'bird3':['bird3_up','bird3']}
    screen = turtle.TurtleScreen(c)
    screen.tracer(0, 0) 
    screen.listen() 
    screen.onkeypress(lambda: jump(), 'Up') 
    screen.onkeypress(lambda: jump(), 'space')
    screen.bgpic(os.path.join(local_dir, "Images/bg.png")) 
    screen.register_shape(os.path.join(local_dir, "Images/pipe_up.gif"))
    screen.register_shape(os.path.join(local_dir, "Images/pipe_down.gif")) 
    screen.register_shape(os.path.join(local_dir, "Images/ground.gif")) 

    # Fetch images
    bird1 = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird1.gif")).zoom(2, 2)  
    bird1_up = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird1_up.gif")).zoom(2, 2)
    bird2 = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird2.gif")).zoom(2, 2) 
    bird2_down = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird2_down.gif")).zoom(2, 2)
    bird2_up = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird2_up.gif")).zoom(2, 2)
    bird3 = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird3.gif")).zoom(2, 2) 
    bird3_up = tkinter.PhotoImage(file=os.path.join(local_dir, "Images/bird3_up.gif")).zoom(2, 2)

    # Register turtle shapes
    screen.addshape("bird1", turtle.Shape("image", bird1))
    screen.addshape("bird1_up", turtle.Shape("image", bird1_up))
    screen.addshape("bird2", turtle.Shape("image", bird2))
    screen.addshape("bird2_down", turtle.Shape("image", bird2_down))
    screen.addshape("bird2_up", turtle.Shape("image", bird2_up))
    screen.addshape("bird3", turtle.Shape("image", bird3))
    screen.addshape("bird3_up", turtle.Shape("image", bird3_up))

    # Score tracker
    write_score = turtle.RawTurtle(screen)
    write_score.hideturtle()
    write_score.penup()
    write_score.goto(0, 150) 

    # Game instructions
    write_help = turtle.RawTurtle(screen)
    write_help.hideturtle()
    write_help.penup()
    write_help.goto(0, 150)
    write_help.write("Press spacebar or up arrow key\n     to control the bird", align="center", font=("Courier", 14, "italic"))

    pipes = []
    for i in range(2):
        d = {'top_pipe': turtle.RawTurtle(screen)}
        d['top_pipe'].penup()
        d['top_pipe'].shape(os.path.join(local_dir, "Images/pipe_up.gif"))
        d['bottom_pipe'] = turtle.RawTurtle(screen)
        d['bottom_pipe'].penup()
        d['bottom_pipe'].shape(os.path.join(local_dir, "Images/pipe_down.gif"))
        d['pipe_x'] = PIPE_X_START + (280 * i)
        d['pipe_y'] = PIPE_Y_START
        d['passed'] = False
        pipes.append(d)

    bird = turtle.RawTurtle(screen)
    bird.shapesize(20)
    bird.penup()
    bird_x = BIRD_X_START
    bird_y = BIRD_Y_START
    bird_vel = 0
    bird_time = 0

    ground = turtle.RawTurtle(screen)
    ground.shape(os.path.join(local_dir, "Images/ground.gif"))
    ground.penup()
    ground.goto(0, -280)
    ground_x = 0

    def jump():
        nonlocal bird_vel, bird_time, first_jump
        first_jump = True
        if not collided:
            bird_vel = -1 * JUMP_VELOCITY 
            bird_time = 0 

    # Check for collision and update score
    def collision_check():
        nonlocal collided
        global score
        for pipe in pipes:
            if (pipe['pipe_x'] - 59) <= bird_x <= (pipe['pipe_x'] + 59): 
                if bird_y >= (pipe['pipe_y'] - 270) or bird_y <= (pipe['pipe_y'] - (GAP - 270)): 
                    collided = True
            if bird_x >= (pipe['pipe_x'] + 59) and not pipe['passed']:
                score += 1
                pipe['passed'] = True

    # Calculate coordinates of all moving objects
    def move():
        nonlocal bird_time, bird_y, first_jump, ground_x, a, ant, bird_vel
        bird_time += 0.7
        displacement = 13
        if not first_jump:
            bird_y = BIRD_Y_START 

        else:
            # S = ut + 1/2at^2
            displacement = bird_vel * bird_time + 0.5 * GRAVITY * (bird_time ** 2)
            if displacement >= TERMINAL_VELOCITY:
                displacement = TERMINAL_VELOCITY 
            if displacement < 0:
                displacement-=2 
            bird_y -= displacement

            if not collided:
                for pipe in pipes:
                    pipe['pipe_x'] -= PIPE_VEL
                    if pipe['pipe_x'] < -270: 
                        pipe['pipe_x'] = 270
                        pipe['passed'] = False
                        pipe['pipe_y'] = random.randint(210, 530)
            else :
                bird_vel=0

        ant += 0.2 
        if ant <= 1:
            ab = 'bird1'
        elif ant <= 2:
            ab = 'bird2'
        elif ant <= 3:
            ab = 'bird3'
        else:
            ab = 'bird2'
            ant = 0

        if displacement <= 10:
            a = images[ab][0]
        if displacement > 10 and displacement <= 18:
            a = images[ab][1]
        if displacement > 18 and bird_time>23:
            a = 'bird2_down'

        if not collided:
            ground_x -= PIPE_VEL 
            if ground_x < -62:
                ground_x = 53 
    
    # Render a frame
    def draw():
        bird.shape(a)

        if first_jump:
            write_help.clear()
            write_score.clear()
            write_score.write(score, align="center", font=("Courier", 24, "bold"))

        for pipe in pipes:
            pipe['top_pipe'].goto(pipe['pipe_x'], pipe['pipe_y'])
            pipe['bottom_pipe'].goto(pipe['pipe_x'], (pipe['pipe_y'] - GAP))

        bird.goto(bird_x, bird_y)
        ground.goto(ground_x, -315)
        screen.update()

    last_frame = 0
    game.tkraise() 
    get_hsbtn.config(state='normal')

    # Main loop
    while True:
        if time.time() - last_frame >= (1 / FPS):
            move() 
            draw() 
            collision_check() 
            if bird_y <= -213:
                break
            last_frame = time.time()
            
    # Gameover 
    scr = "Your score : " + str(score) + "\nBest score : "
    if len(highscores)>=1:
        scr += str(sorted(highscores, key = lambda h : h[-1], reverse=True)[0][1])
    score_label.config(text=scr)
    if not check_hs(score):
        get_hsbtn.config(state='disabled')
    gameover.tkraise()

root.mainloop()
