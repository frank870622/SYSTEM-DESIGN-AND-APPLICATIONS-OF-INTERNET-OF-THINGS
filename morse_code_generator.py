import turtle
from PIL import Image

char2morse = { 'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010', 'G': '110', 'H': '0000', 'I': '00', 'J': '0111', 'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111', 'P': '0110', 'Q': '1101', 'R': '010', 'S': '000', 'T': '1', 'U': '001', 'V': '0001', 'W': '011', 'X': '1001', 'Y': '1011', 'Z': '1100', '1': '01111', '2': '00111', '3': '00011', '4': '00001', '5': '00000', '6': '10000', '7': '11000', '8': '11100', '9': '11110', '0': '00000'}

def parse(text):
    out = []
    for c in text.upper():
        if c == " ":
            out.append(c)
        else:
            out.append(char2morse[c])

    return out

def draw_rect(pen):
    pen.left(90)
    pen.fd(10)
    pen.right(90)
    pen.pd()
    pen.begin_fill()
    pen.fd(100)
    pen.left(90)
    pen.fd(40)
    pen.left(90)
    pen.fd(100)
    pen.left(90)
    pen.fd(40)
    pen.end_fill()
    pen.pu()
    pen.fd(10)
    pen.left(90)
    pen.fd(100)

def draw_circle(pen, rad = 30):
    pen.fd(30)
    pen.pd()
    pen.begin_fill()
    pen.circle(rad)
    pen.end_fill()
    pen.pu()
    pen.fd(rad)

def draw(text, file_name):
    elements = parse(text)

    screen = turtle.Screen()
    screen.setup(1000, 1000)

    pen = turtle.Turtle()
    pen.pensize(3)
    pen.hideturtle()
    pen.speed(10)

    pen.st()

    # draw anchor point
    pen.pu()
    pen.goto(-480, 330)
    draw_circle(pen)
    pen.goto(420, 330)
    draw_circle(pen)
    pen.goto(-480, -320)
    draw_circle(pen, -30)
    pen.goto(420, -320)
    draw_circle(pen, -30)



    pen.pu()
    orig_x = -350
    pen.goto(-350, 250)

    for e in elements:
        for m in e:
            if m == '1':
                draw_rect(pen)
            elif m == '0':
                draw_circle(pen)

            pen.goto(pen.xcor()+50, pen.ycor())

        pen.goto(orig_x, pen.ycor()-100)

    pen.ht()

    pen.getscreen().getcanvas().postscript(file= file_name+'.eps')
    img = Image.open(file_name + '.eps') 
    img.save(file_name + '.png') 

    turtle.done()
            

if __name__ == "__main__":
    plaintext = "m1"
    file_name = "hello"
    
    draw(plaintext, file_name)

