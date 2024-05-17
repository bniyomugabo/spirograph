from ezTK import *
from math import *
from ezCLI import *
from random import *
from PIL import Image, ImageTk, ImageGrab



info = {
    'X_axis': [],
    'Y_axis': [],
    'Name':[],
    'angle':[]
}


def main():

    global win
    win = Win(title='TROCHOIDE PREMIUM', flow="E", op=1)

    frame = Frame(win, flow='S', bg='#230', fg="#FFF",
                  font='Arial 17 ', height=1000)
    values = tuple(range(0, 900000))

    Label(frame, font='Arial 40 bold', text='Spirograph',
          bg="#000", border=1, grow=False)

    fr1 = Frame(frame)

    Label(fr1, font='Arial 16', text="  Rayon d'orbite <R> ", bg="#000", grow=False)

    win.R = Spinbox(fr1, values=values,
                    state=values[100], width=1, wrap=False)

    Label(fr1, font='Arial 16', text='  Rayon du cercle mobile <r> ',
          bg="#000", grow=False)
    win.r = Spinbox(fr1, values=values,
                    state=values[50], width=1, wrap=False)

    Label(fr1, font='Arial 16', text='  Distance du centre <r> à <d> ',
          bg="#000", grow=False)
    win.distance = Spinbox(
        fr1, values=values, state=values[120], width=1, wrap=False)

    Label(fr1, font='Arial 16', text='  Rotation <en degré> ',
          bg="#000", grow=False)
    win.orbit = Spinbox(fr1, values=values,
                        state=values[360], width=1, wrap=False)
    colors = ('#fff','#000')
    scale = (0, 255)
    win.frame = Frame(fr1, op=0)
    Label(win.frame,text='#FFF',bg='#000')
    Scale(win.frame, scale=scale, state=0, command=on_scale)
    Scale(win.frame, scale=scale, state=0, command=on_scale)
    Scale(win.frame, scale=scale, state=0, command=on_scale)
    

    Label(fr1, font='Arial 16', text="  Couleur d'arrière plan ",
          bg="#000", grow=False)
    win.background = Spinbox(
        fr1, values=colors, state=colors[1], width=1, wrap=False)

    fr2 = Frame(frame, grow=False)
    
    Label(fr2, font='Arial 16', text=" cercle mobile", bg="#000", grow=False)
    drawTypes = ('Cercle mobile: interieur', 'Cercle mobile: exterieur')
    win.graphs = Spinbox(fr2, values=drawTypes,
                         state=drawTypes[0], width=1, wrap=False)
    
    Button(fr2, text=" Orbit ", command=orbital, bg="#000", fg="#869191")
    Button(fr2, text=' Dessine ',  command=drawings, bg="#000", fg="#869191")
    Button(fr2, text=' Recommener ', command=reset, bg="#000", fg="#869191")
    Button(fr2, text=' Sauvegarder ', command=save, bg="#000", fg="#869191")

    Frame(fr2, height=200)

    win.indicator = 0
    win.counter = 0
    win.delete = 0

    win.fr3 = Frame(win, bg=win.background.state)
    canvas = Canvas(win.fr3, width=900, height=900)
    win.canvas = win.fr3[0]

    win.loop()

def on_scale ():
    crd = (0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F')
    r = crd[(win.frame[1].state)//16]
    win.frame[1]['bg']= f"#{r}00"
    g = crd[(win.frame[2].state)//16]
    win.frame[2]['bg'] = f"#0{g}0"
    b = crd[(win.frame[3].state)//16]
    win.frame[3]['bg'] = f"#00{b}"
    win.frame[0]['text'] = f"#{r}{g}{b}"
    win.frame[0]['bg'] = f"#{r}{g}{b}"
    win.frame[0]['fg'] = f"#FFF" if (win.frame[1].state + win.frame[2].state + win.frame[3].state)/3 < 127 else "#000"

    
    
def orbital(xC=450, yC=400):  # xC  et xC sont des coardonnées du centre du grand cercle
    R = int(win.R.state)
    if win.indicator == 0:
        win.indicator = 2
        color = "#ABB848"
        xB, yB = xC + (R * cos(0)), yC - (R * sin(0))
        for beta in range(361):  # beta est l'angle
            beta = radians(beta)
            xA, yA, xB, yB = xB, yB, xC + (R * cos(beta)), yC - (R * sin(beta))
            win.canvas.create_line(xA, yA, xB, yB, width=2, fill=color)
            
    elif win.indicator == 2:
        win.indicator = 0
        color = win.background.state
        xB, yB = xC + (R * cos(0)), yC - (R * sin(0))
        for i in range(10):
            for beta in range(361):  # beta est l'angle
                beta = radians(beta)
                xA, yA, xB, yB = xB, yB, xC + (R * cos(beta)), yC - (R * sin(beta))
                win.canvas.create_line(xA, yA, xB, yB, width=2, fill=color)
        

    

def spirograph(xC=450, yC=400):
    R = int(win.R.state)
    r = int(win.r.state)
    d = int(win.distance.state)
    angle = int(win.orbit.state) + 1
    for beta in range(angle):  # beta est l'angle
        beta = radians(beta)
        alpha = (R*beta)/r
        xB, yB = xC + (R * cos(beta)), yC - (R * sin(beta))
        xc, yc = xB - r * cos(beta), yB + r * sin(beta)
        pencilpath(d, xc, yc, alpha)

    animation()
    win.delete = 1


def epitrochoide(xC=450, yC=400):
    R = int(win.R.state)
    r = int(win.r.state)
    d = int(win.distance.state)
    angle = int(win.orbit.state) + 1
    for beta in range(angle+1):  # beta est l'angle
        beta = radians(beta)
        alpha = (R*beta)/r
        xc, yc = xC + ((r+R) * cos(beta)), yC - ((r+R) * sin(beta))

        pencilpath(d, xc, yc, alpha)

    animation()
    win.delete = 'not delete'


def pencilpath(d, xc, yc, alpha):
    color = win.frame[0]['bg']
    alpha = radians(360 - degrees(alpha))
    xa, ya = xc + (d * cos(alpha)), yc - (d * sin(alpha))
    alpha = radians(degrees(alpha+0.01))
    xb, yb = xc + (d * cos(alpha)), yc - (d * sin(alpha))
    x = info['X_axis'].append(xa)
    y = info['Y_axis'].append(ya)
    angle = info['angle'].append(int(win.orbit.state))
    
    


def animation():
    if len(info['X_axis'])-1 > (win.counter):
        color = win.frame[0]['bg'] if win.delete != 'delete' else win.background.state
        xa, ya, xb, yb = info['X_axis'][win.counter], info['Y_axis'][win.counter], info['X_axis'][win.counter +1], info['Y_axis'][win.counter + 1]
        win.canvas.create_line(xa, ya, xb, yb, width=2,
                               fill=color, caps='round')
        win.counter += 1

    win.after(2, animation)


def drawings():
    win.counter = len(info['X_axis'])
    R, r = int(win.R.state), int(win.r.state)
    win.canvas['bg'] = win.background.state
    if r < R and win.graphs.state == 'Cercle mobile: interieur':
        return spirograph(xC=450, yC=400)
    elif win.graphs.state == 'Cercle mobile: exterieur':
        return epitrochoide(xC=450, yC=400)
    else:
        None



def save():
    #name = Dialog('open',title=O)
    x = win.winfo_rootx() + win.canvas.winfo_x()
    y = win.winfo_rooty() + win.canvas.winfo_y()
    x1 = x+win.canvas.winfo_width()
    y1 = y+win.canvas.winfo_height()
    #print(name)
    
    ImageGrab.grab().crop((x, y, x1, y1)).save('PREMIUM')
    
    
# In[]
def reset():
    info['X_axis'].clear()
    info['Y_axis'].clear()
    win.indicator = 0
    win.counter = 0
    win.delete = 0
    del win.fr3[0]
    win.canvas = Canvas(win.fr3, width=900, height=900)
   
if __name__ == "__main__":
    main()
