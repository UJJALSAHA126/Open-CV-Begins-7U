from tkinter import *

def button_press(num) :
    global eq_text
    eq_text = eq_text + str(num)
    eq_lable.set(eq_text)

def equals() :
    global eq_text
    try :
        total = str(eval(eq_text))
        eq_lable.set(total)
        eq_text = total
    except SyntaxError :
        eq_lable.set("Syntax Error")
    except ZeroDivisionError :
        eq_lable.set("Arithmatic Error")    

def clearr() :
    global eq_text

    eq_lable.set("")
    eq_text=""

def backspace() :
    global eq_text
    eq_text=eq_text[0:len(eq_text)-1]
    eq_lable.set(eq_text)

if __name__ == "__main__" :
    window = Tk()
    window.title("Calculator")
    window.geometry("600x600")

    eq_text = ""
    eq_lable = StringVar()

    lable =Label(window,textvariable=eq_lable,font=('consolas',20),bg="white",width=40,height=2)
    lable.pack()

    frame = Frame(window)
    frame.pack()

    button1 = Button(frame,text=1 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(1))
    button1.grid(row=0,column=0)         

    button2 = Button(frame,text=2 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(2))
    button2.grid(row=0,column=1)   

    button3 = Button(frame,text=3 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(3))
    button3.grid(row=0,column=2)

    button4 = Button(frame,text=4 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(4))
    button4.grid(row=1,column=0)

    button5 = Button(frame,text=5 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(5))
    button5.grid(row=1,column=1)

    button6 = Button(frame,text=6 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(6))
    button6.grid(row=1,column=2)

    button7 = Button(frame,text=7 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(7))
    button7.grid(row=2,column=0)

    button8 = Button(frame,text=8 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(8))
    button8.grid(row=2,column=1)

    button9 = Button(frame,text=9 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(9))
    button9.grid(row=2,column=2)

    button0 = Button(frame,text=0 , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press(0))
    button0.grid(row=3,column=1)

    plus = Button(frame,text='+' , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press('+'))
    plus.grid(row=0,column=3)

    minus = Button(frame,text='-' , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press('-'))
    minus.grid(row=1,column=3)

    multipy = Button(frame,text='X' , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press('*'))
    multipy.grid(row=2,column=3)

    divied = Button(frame,text='/' , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press('/'))
    divied.grid(row=3,column=3)

    equal = Button(frame,text='=' , height=4 , width=9 ,font=35 ,
                    command= equals, borderwidth=6,bg="grey")
    equal.grid(row=3,column=2)

    deci = Button(frame,text='.' , height=4 , width=9 ,font=35 ,
                    command= lambda : button_press('.'))
    deci.grid(row=3,column=0)

    clear = Button(window,text= 'clear' , height=4 , width=15 ,font=35 ,
                    command= clearr)
    clear.pack(side="bottom")

    backspac = Button(frame,text='<--' , height=4 , width=9 ,font=35 ,
                    command= backspace,fg="red")
    backspac.grid(row=4,column=0)

    window.mainloop()