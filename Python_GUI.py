from tkinter import * #pip install tk
import customtkinter
import serial.tools.list_ports
import threading
import signal
import time
import json
import matplotlib.pyplot as plt #pip install matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D   


#port = "COM11"
#ser = serial.Serial(port, 2000000, timeout=0.01)
#ser.xonxoff=1

class Graphics():
    pass

def connect_menu_init():
    global root, connect_btn, refresh_btn, toggle_pin_START_L, input_print, input_print_rpm, input_print_C, input_txt, input_rpm, input_C ,buttons_frame, controlling_frame, xRPM, yRPM, Y_MAX_RPM, X_MAX_RPM, axRPM, chartRPM, figRPM, xDataRPM, yDataRPM, currentstate_frame, wartosci, velocityUART, directionUART, pwmUART, toggle_pin_START_R, wartosci1, wartosci2, xDataA, yDataA, Y_MAX_A, X_MAX_A, axA, chartA, figA, xA, yA, regulators_frame, controlling_frame, input_printDEFA, input_printKASK, input_printPRAD, input_printPRED, input_printKIP, input_printKIPP, input_printKIV, input_printKIVV, input_printKPVV, input_printKPP, input_printKPV, input_printKPPP, input_printPRAD, input_printPRED, input_KIP, input_KIPP, input_KIV, input_KPP, input_KPPP, input_KPV, input_KIVV, input_KIV, input_KPVV,ser, start
    root = Tk()
    root.title("Stanowisko BLDC")
    root.geometry("1150x900")
    root.resizable(False, False)
    #root.config(bg="white")

    buttons_frame = LabelFrame(root, width=20, text="Połączenie")
    buttons_frame.grid(columnspan=4, row=0,padx=15,pady=15, sticky='WE')

    port_av = Label(buttons_frame, text="Dostępne porty:")
    port_av.grid(column=1, row=2, pady=20, padx=10)

    port_bd = Label(buttons_frame, text="Baudrate:")
    port_bd.grid(column=1, row=3, pady=20, padx=10)

    refresh_btn = Button(buttons_frame, text="ODŚWIEŻ", height=2, width=7, command = update_coms)
    refresh_btn.grid(column=3, row=2,padx=10,pady=20)

    connect_btn = Button(buttons_frame, text="Połącz", height=2, width=7, state="disabled", command = com_connection)
    connect_btn.grid(column=3, row=3)

    start = Button(buttons_frame, text="Włącz UART", height=2, width=12, state="disabled", command = uart_connection)
    start.grid(column=2, row=4,padx=10,pady=20)





    controlling_frame = LabelFrame(root, width=20,text="Sterowanie")
    controlling_frame.grid(columnspan=4, row=1 ,padx=10,pady=10, sticky='WE')

    currentstate_frame = LabelFrame(root, width=20, text="Monitor zmiennych")
    #currentstate_frame.grid(columnspan=4, row=12, padx=10,pady=20, sticky='WE')

    regulators_frame = LabelFrame(root, width=20, text="Regulator kaskadowy")
    regulators_frame.grid(columnspan=4, row=8, padx=10,pady=10, sticky='WE')

    regulatorsPP_frame = LabelFrame(root, width=20, text="Regulator prędkości")
    regulatorsPP_frame.grid(columnspan=2, row=9, padx=10,pady=10, sticky='WE')

    regulatorsPPI_frame = LabelFrame(root, width=20, text="Regulator prądu")
    regulatorsPPI_frame.grid(columnspan=2, row=9, column =3,padx=10,pady=10, sticky='WE')

    regulatory_frame = LabelFrame(root, width=20, text="Regulacja")
    regulatory_frame.grid(columnspan=4, row=7, padx=10,pady=10, sticky='WE')

    wartosci = Label(currentstate_frame)
    wartosci.grid(column=3, row=3, pady=2, padx=1, sticky='W')

    wartosci1 = Label(currentstate_frame)
    wartosci1.grid(column=3, row=4, pady=2, padx=1, sticky='W')

    wartosci2 = Label(currentstate_frame)
    wartosci2.grid(column=3, row=5, pady=2, padx=1, sticky='W')

    toggle_pin_START_L= Button(controlling_frame, text="LEWO", height=2, width=10, state="disabled", command=toggleSTART_L)
    toggle_pin_START_L.grid(column=3, row=4,sticky='W', pady=1, padx=10)

    toggle_pin_START_R= Button(controlling_frame, text="PRAWO", height=2, width=10, state="disabled", command=toggleSTART_R)
    toggle_pin_START_R.grid(column=3, row=5, pady=1, padx=10)

    #test wysyania pwmUART
    input_txt = Text(controlling_frame, height=1, width=5)
    input_print = Button(controlling_frame, text = "PWM", height = 2, width = 10, command = printInputPWM, state="disabled")
    input_print.grid(column=4, row=4, pady=10, padx=10)
    input_txt.grid(column=4,row=5, pady=10, padx=10)

    input_rpm = Text(controlling_frame, height=1, width=5)
    input_print_rpm = Button(controlling_frame, text = "PRĘDKOŚĆ", height = 2, width = 10, command = printInputRPM, state="disabled")
    input_print_rpm.grid(column=5, row=4, pady=10, padx=10)
    input_rpm.grid(column=5,row=5, pady=10, padx=10)

    input_C = Text(controlling_frame, height=1, width=5)
    input_print_C = Button(controlling_frame, text = "PRĄD", height = 2, width = 10, command = printInputC, state="disabled")
    input_print_C.grid(column=6, row=4, pady=10, padx=10)
    input_C.grid(column=6,row=5, pady=10, padx=10)

    #regacja
    input_KIP = Text(regulators_frame, height=2, width=5)
    input_printKIP= Button(regulators_frame, text = "Ki - PRĄD", height = 2, width = 8, command = writeKASK_Ki_Curr, state="disabled")
    input_printKIP.grid(column=4, row=6, pady=10, padx=10)
    input_KIP.grid(column=4,row=7, pady=10, padx=10)

    input_KPP= Text(regulators_frame, height=2, width=5)
    input_printKPP = Button(regulators_frame, text = "Kp - PRĄD", height = 2, width = 8, command = writeKASK_Kp_Curr, state="disabled")
    input_printKPP.grid(column=5, row=6, pady=10, padx=10)
    input_KPP.grid(column=5,row=7, pady=10, padx=10)

    input_KIV = Text(regulators_frame, height=2, width=5)
    input_printKIV = Button(regulators_frame, text = "Ki - PRĘDKOŚĆ", height = 2, width = 12, command = writeKASK_Ki_Velo, state="disabled")
    input_printKIV.grid(column=7, row=6, pady=10, padx=10)
    input_KIV.grid(column=7,row=7, pady=10, padx=10)

    input_KPV = Text(regulators_frame, height=2, width=5)
    input_printKPV = Button(regulators_frame, text = "Kp - PRĘDKOŚĆ", height = 2, width = 12, command = writeKASK_Kp_Velo, state="disabled")
    input_printKPV.grid(column=8, row=6, pady=10, padx=10)
    input_KPV.grid(column=8,row=7, pady=10, padx=10)


    input_KIPP = Text(regulatorsPP_frame, height=2, width=5)
    input_printKIPP= Button(regulatorsPP_frame, text = "Ki - PRĄD", height = 2, width = 8, command = write_Ki_Curr, state="disabled")
    input_printKIPP.grid(column=4, row=8, pady=10, padx=10)
    input_KIPP.grid(column=4,row=9, pady=10, padx=10)

    input_KPPP= Text(regulatorsPP_frame, height=2, width=5)
    input_printKPPP = Button(regulatorsPP_frame, text = "Kp - PRĄD", height = 2, width = 8, command = write_Kp_Curr, state="disabled")
    input_printKPPP.grid(column=5, row=8, pady=10, padx=10)
    input_KPPP.grid(column=5,row=9, pady=10, padx=10)

    input_KIVV = Text(regulatorsPPI_frame, height=2, width=5)
    input_printKIVV = Button(regulatorsPPI_frame, text = "Ki - PRĘDKOŚĆ", height = 2, width = 12, command = write_Ki_Velo, state="disabled")
    input_printKIVV.grid(column=6, row=8, pady=10, padx=10)
    input_KIVV.grid(column=6,row=9, pady=10, padx=10)

    input_KPVV = Text(regulatorsPPI_frame, height=2, width=5)
    input_printKPVV = Button(regulatorsPPI_frame, text = "Kp - PRĘDKOŚĆ", height = 2, width = 12, command = write_Kp_Velo, state="disabled")
    input_printKPVV.grid(column=7, row=8, pady=10, padx=10)
    input_KPVV.grid(column=7,row=9, pady=10, padx=10)





    input_printKASK= Button(regulatory_frame, text = "KASKADOWY", height = 1, width = 12, command = chooseKASK, state="disabled")
    input_printKASK.grid(column=4, row=6, pady=10, padx=10)

    input_printPRAD = Button(regulatory_frame, text = "PRĄDU", height = 1, width = 12, command = chooseCURR, state="disabled")
    input_printPRAD.grid(column=5, row=6, pady=10, padx=10)
 
    input_printPRED = Button(regulatory_frame, text = "PRĘDKOŚCI", height = 1, width = 12, command = chooseVELO, state="disabled")
    input_printPRED.grid(column=6, row=6, pady=10, padx=10)

    input_printDEFA = Button(regulatory_frame, text = "DEFAULT", height = 1, width = 12, command = chooseDEFA, state="disabled")
    input_printDEFA.grid(column=7, row=6, pady=10, padx=10)

    baudrate_select()
    update_coms()
    X_MAX_RPM = 20
    Y_MAX_RPM = 5000

    figRPM = plt.Figure(figsize=(6, 4), dpi=100)
    axRPM = figRPM.add_subplot(111)
    axRPM.set_title("Prędkość [rpm]")
    axRPM.set_ylim([0, Y_MAX_RPM])
    axRPM.set_autoscale_on(False)
    chartRPM = FigureCanvasTkAgg(figRPM, master=root)
    chartRPM.get_tk_widget().grid(column=9, row=0, columnspan=6, rowspan=6, pady=10, padx=40)
    chartRPM.get_tk_widget()#.grid_remove()
 
    xDataRPM = []
    yDataRPM = []
    xRPM = []
    yRPM = []


    X_MAX_A = 20
    Y_MAX_A = 2

    figA = plt.Figure(figsize=(6, 4), dpi=100)
    axA = figA.add_subplot(111)
    axA.set_title("Prąd silnika [A]")
    axA.set_ylim([0, Y_MAX_A])
    axA.set_autoscale_on(False)
    chartA = FigureCanvasTkAgg(figA, master=root)
    chartA.get_tk_widget().grid(column=9, row=7, columnspan=6, rowspan=6, pady=10, padx=40)
    chartA.get_tk_widget()#.grid_remove()
 
    xDataA = []
    yDataA = []
    xA = []
    yA = []

def printInput():
    global ser, lb_info, input_txt 
    inp = input_txt.get(1.0, "end-1c")
    strSetPWM = "set_PWM="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 10.0) & (inp_pwm <= 95.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
        labelT.destroy()
    except:
        labelT = Label(root, text = "PWM <10-95>, PRĘDKOŚĆ <100-4000>, PRĄD <0.0-1.0>")
        labelT.config(font =("Courier", 10))
        labelT.grid(columnspan = 4, row=2 ,padx=5,pady=5, sticky='WE')
        labelT.after(2500, labelT.destroy)

def hideButton():
    Label.pack_forget()
def showButton():
    Label.pack()

def printInputPWM():
    global ser, lb_info, input_txt
    inp = input_txt.get(1.0, "end-1c")
    strSetPWM = "set_PWM="
    strEndLine = "\r\n"
    inp_pwm = float(inp)
    strPWM = str(inp)
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 10.0) & (inp_pwm <= 95.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
        labelT.destroy()
    except:
        labelT = Label(root, text = "PWM <10-95>, PRĘDKOŚĆ <100-4000>, PRĄD <0.0-1.0>")
        labelT.config(font =("Courier", 10))
        labelT.grid(columnspan = 4, row=2 ,padx=5,pady=5, sticky='WE')
        labelT.after(2500, labelT.destroy)

def printInputRPM():
    global ser, lb_info, input_txt
    inp = input_rpm.get(1.0, "end-1c")
    strSetPWM = "set_V="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 100.0) & (inp_pwm <= 4000.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
        labelT.destroy()
    except:
        labelT = Label(root, text = "PWM <10-95>, PRĘDKOŚĆ <100-4000>, PRĄD <0.0-1.0>")
        labelT.config(font =("Courier", 10))
        labelT.grid(columnspan = 4, row=2 ,padx=5,pady=5, sticky='WE')
        labelT.after(2500, labelT.destroy)

def printInputC():
    global ser, lb_info, input_txt
    inp = input_C.get(1.0, "end-1c")
    strSetPWM = "set_C="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 1.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
        labelT.destroy()
    except:
        labelT = Label(root, text = "PWM <10-95>, PRĘDKOŚĆ <100-4000>, PRĄD <0.0-1.0>")
        labelT.config(font =("Courier", 10))
        labelT.grid(columnspan = 4, row=2 ,padx=5,pady=5, sticky='WE')
        labelT.after(2500, labelT.destroy)

def write_Ki_Velo():
    global ser, lb_info, input_txt
    inp = input_KIV.get(1.0, "end-1c")
    strSetPWM = "set_IW="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def write_Ki_Curr():
    global ser, lb_info, input_txt
    inp = input_KIP.get(1.0, "end-1c")
    strSetPWM = "set_II="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def write_Kp_Curr():
    global ser, lb_info, input_txt
    inp = input_KPP.get(1.0, "end-1c")
    strSetPWM = "set_PI="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def write_Kp_Velo():
    global ser, lb_info, input_txt
    inp = input_KPV.get(1.0, "end-1c")
    strSetPWM = "set_PW="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass

def writeKASK_Ki_Velo():
    global ser, lb_info, input_txt
    inp = input_KIVV.get(1.0, "end-1c")
    strSetPWM = "set_IWK="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def writeKASK_Kp_Velo():
    global ser, lb_info, input_txt
    inp = input_KPVV.get(1.0, "end-1c")
    strSetPWM = "set_PWK="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def writeKASK_Kp_Curr():
    global ser, lb_info, input_txt
    inp = input_KPPP.get(1.0, "end-1c")
    strSetPWM = "set_PIK="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def writeKASK_Ki_Curr():
    global ser, lb_info, input_txt
    inp = input_KIPP.get(1.0, "end-1c")
    strSetPWM = "set_IIK="
    strEndLine = "\r\n"
    try:
        inp_pwm = float(inp)
        strPWM = str(inp)
        if(inp_pwm >= 0.0) & (inp_pwm <= 255.0):
            strPWMtoSend = strSetPWM + strPWM + strEndLine
            ser.write(strPWMtoSend.encode())
        else:
            pass
    except:
        pass
def chooseKASK():
        Close3 = "Close_ON=3\r\n"
        ser.write(Close3.encode()) 
def chooseCURR():
        Close2 = "Close_ON=2\r\n"
        ser.write(Close2.encode()) 
def chooseVELO():
        Close1 = "Close_ON=1\r\n"
        ser.write(Close1.encode()) 
def chooseDEFA():
        START_L = "set_Def\r\n"
        ser.write(START_L.encode()) 


def toggleSTART_L():
        START_L = "Start_L\r\n"
        ser.write(START_L.encode())

def toggleSTART_R():
        START_R = "Start_R\r\n"
        ser.write(START_R.encode())     


def update_chartRPM():
    global xRPM, yRPM,  figRPM , chartRPM, axRPM, serialData, xDataRPM, yDataRPM, velocityUART
    axRPM.clear()
    axRPM.plot(xRPM, yRPM, '-', dash_capstyle='projecting')
    axRPM.grid(color='b', linestyle='-', linewidth=0.3)
    axRPM.set_title("Prędkość [rpm]")
    axRPM.set_ylim([0, Y_MAX_RPM])
    axRPM.set_autoscale_on(False)
    figRPM.canvas.draw()
    if serialData:
        root.after(250, update_chartRPM)

def uart_connection():
        set_GUI = "GUI_ON\r\n"
        ser.write(set_GUI.encode()) 
def update_chartA():
    global xA, yA, figA, chartA, axA, serialData, xDataA, yDataA, velocityUART
    axA.clear()
    axA.plot(xA, yA, '-', dash_capstyle='projecting')
    axA.grid(color='r', linestyle='-', linewidth=0.3)
    axA.set_title("Prąd silnika [A]")
    axA.set_ylim([0, Y_MAX_A])
    axA.set_autoscale_on(False)
    figA.canvas.draw()
    if serialData:
        root.after(250, update_chartA)

def connect_check(args):
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"] = "disable"
    else:
        connect_btn["state"] = "active"
        
def baudrate_select():
    global clicked_bd, drop_bd
    clicked_bd = StringVar()
    bds = ["-","115200"]
    clicked_bd.set(bds[0])
    drop_bd = OptionMenu(buttons_frame, clicked_bd, *bds, command = connect_check)
    drop_bd.config(width=20)
    drop_bd.grid(column=2, row=3, padx=50)

def update_coms():
    global clicked_com, drop_COM
    ports = serial.tools.list_ports.comports()
    coms = [com[0] for com in ports]
    coms.insert(0, "-")
    try:
        drop_COM.destroy()
    except:
        pass
    clicked_com = StringVar()
    clicked_com.set(coms[0])
    drop_COM = OptionMenu(buttons_frame, clicked_com, *coms, command = connect_check)
    drop_COM.config(width=20)
    drop_COM.grid(column=2, row=2, padx=50)
    connect_check(0)


def readSerial():
    print("thread start")
    global serialData, xRPM, yRPM, yA, xA, refTimeRPM, refTimeA, JSONdecode, directionUART, pwmUART, velocityUART, kierunek, currentUART, samplingA, sampleA, velocityUARTabs
    average = 0
    samplingRPM = 2
    sampleRPM = 0
    samplingA = 2
    sampleA = 0
    # 5 Adding 10 reads to clean the buffe
    for _ in range(2):
        try:
            data = ser.readline()
        except:
            pass

    while serialData:

        data = ser.readline().strip()

        if len(data) > 0:
            try:
                dataDecode = data.decode('utf8')
                JSONdecode = json.loads(dataDecode)
                velocityUART = float(JSONdecode["vel"])
                velocityUARTabs = float(JSONdecode["vel"])
                directionUART = int(JSONdecode["dir"])
                pwmUART = float(JSONdecode["pwm"])
                currentUART = float(JSONdecode["curr"])

                if velocityUARTabs < 0:
                    velocityUART = abs(float(JSONdecode["vel"]))
                #print(currentUART)
                #print(pwmUART)
                if directionUART == 0:
                    kierunek = "PRAWO"
                elif directionUART == 1:
                    kierunek = "LEWO"
                else:
                    kierunek = "BRAK"

                labelPWM = Label(root, text = ["Prędkość:" ,velocityUART, "Kierunek:", kierunek,"PWM:" ,pwmUART])
                labelPWM.config(font =("Courier", 12))
                labelPWM.grid(columnspan=6, rowspan=6, pady=10, padx=40, column=9, row = 13)

                sampleRPM += 1
                sampleA += 1

                if sampleA == samplingA:
                    #average = 0
                    #print("data: ", data_sensor)
                    sampleA = 0

                    lenYdataA = len(yDataA)
                    lenXdataA = len(xDataA)

                    printRangeA = 0
                    TimeRangeA = 10

                    yDataA.append(currentUART)
                    for time_series2 in range(lenXdataA-1, 0, -1):
                        printRangeA += 1
                        if xDataA[lenXdataA-1] - xDataA[time_series2 - 1] > TimeRangeA:
                            break
                    if len(xDataA) == 0:
                        xDataA.append(0)
                    else:
                        xDataA.append(time.perf_counter()-refTimeA)

                    if lenXdataA == printRangeA:
                        yA = [k for k in yDataA]
                        xA = [k for k in xDataA]
                    else:
                        yA = yDataA[lenYdataA-printRangeA:lenYdataA]
                        xA = xDataA[lenXdataA-printRangeA:lenXdataA]
                    
                    if len(yDataA) > 10:
                        yDataA.clear
                    else:
                        pass

                if sampleRPM == samplingRPM:
                    #average = 0
                    #print("data: ", data_sensor)
                    sampleRPM = 0

                    lenYdataRPM = len(yDataRPM)
                    lenXdataRPM = len(xDataRPM)
                    printRangeRPM = 0
                    TimeRangeRPM = 10
                    yDataRPM.append(velocityUART)
                    for time_series in range(lenXdataRPM-1, 0, -1):
                        printRangeRPM += 1
                        if xDataRPM[lenXdataRPM-1] - xDataRPM[time_series - 1] > TimeRangeRPM:
                            break
                    if len(xDataRPM) == 0:
                        xDataRPM.append(0)
                    else:
                        xDataRPM.append(time.perf_counter()-refTimeRPM)

                    if lenXdataRPM == printRangeRPM:
                        yRPM = [k for k in yDataRPM]
                        xRPM = [k for k in xDataRPM]
                    else:
                        yRPM = yDataRPM[lenYdataRPM-printRangeRPM:lenYdataRPM]
                        xRPM = xDataRPM[lenXdataRPM-printRangeRPM:lenXdataRPM]

                    if len(yDataA) > 10:
                        yDataA.clear
                    else:
                        pass
            except:
                pass


def com_connection():
    global ser, serialData, refTimeRPM, refTimeA
    serialData = True
    if connect_btn["text"] in "Rozłącz":
        print(serialData)
        connect_btn["text"] = "Połącz"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"
        toggle_pin_START_L["state"] = "disable"
        toggle_pin_START_R["state"] = "disable"
        set_GUI = "GUI_OFF\r\n"
        ser.write(set_GUI.encode()) 
        serialData = False

    else:
        connect_btn["text"] = "Rozłącz"
        refresh_btn["state"] = "disable"
        toggle_pin_START_L["state"] = "active"
        toggle_pin_START_R["state"] = "active"
        input_print["state"] = "active"
        input_print_rpm["state"] = "active"
        input_print_C["state"] = "active"
        input_printKPPP["state"] = "active"
        input_printDEFA["state"] = "active"
        input_printKASK["state"] = "active"
        input_printKIP["state"] = "active"
        input_printPRED["state"] = "active"
        input_printPRAD["state"] = "active"
        input_printKPV["state"] = "active"
        input_printKPP["state"] = "active"
        input_printKPVV["state"] = "active"
        input_printKIV["state"] = "active"
        input_printKIPP["state"] = "active"
        input_printKIVV["state"] = "active"
        drop_bd["state"] = "disable"
        drop_COM["state"] = "disable"
        start["state"] = "active"
        #set_GUI = "GUI_ON\r\n"
        #ser.write(set_GUI.encode()) 
        port = clicked_com.get()
        baud = clicked_bd.get()
        try:
            ser = serial.Serial(port, baud, timeout=0.2)
        except:
            pass
        if len(xDataRPM) == 0:
           refTimeRPM = time.perf_counter()
        else:
            refTimeRPM = time.perf_counter()-xDataRPM[len(xDataRPM)-1] 

        if len(xDataA) == 0:
           refTimeA = time.perf_counter()
        else:
            refTimeA = time.perf_counter()-xDataA[len(xDataA)-1] 

        t1 = threading.Thread(target=readSerial)
        t1.deamon = True
        t1.start()
        update_chartRPM()
        update_chartA()

def close_window():
    global root, serialData
    serialData = False
    time.sleep(0.5)
    root.destroy()



connect_menu_init()  # Start the GUI & Initialization
root.protocol("WM_DELETE_WINDOW", close_window)  # When Closing the Window
root.mainloop()  # Stating the main loop / Thread


