from pynput.keyboard import Listener, Key
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import threading, time, sys

first_time = time.time()
input_keyboard = []   #텍스트파일에 넣을 값을 정리하는 키보드값
qwer = [[], [], [], []]   #matplotlib형식에 맞게 qwer정리한 값
num = 0    #txt파일이 몇개 있는지 카운트하는 값
timer = 30  #몇초 주기로 할지 정하는 값
chat = False  #채팅 칠때 받지않는것으로 유도하는 값

def sort_graph():
    global first_time, timer, num, qwer
    qwer[0].clear()
    qwer[1].clear()
    qwer[2].clear()
    qwer[3].clear()
    q = 0
    w = 0
    e = 0
    r = 0
    ttime = first_time
    timer_count = 0
    for i in range(num + 1): 
        with open("Test{}.txt".format(i),'r') as txt_file:
            tmp = 0
            while True:
                txt_line = txt_file.readline()
                if not txt_line:
                    break
                if tmp % 2 == 0:
                    ttime = float(txt_line)
                    tmp += 1
                    continue
                tmp += 1
                if int((ttime - first_time)/timer) != timer_count:
                    while True:
                        if int((ttime - first_time)/timer) == timer_count:
                            break
                        qwer[0].append(q)
                        qwer[1].append(w)
                        qwer[2].append(e)
                        qwer[3].append(r)
                        print(qwer)
                        q = 0
                        w = 0
                        e = 0
                        r = 0
                        timer_count += 1
                if len(txt_line) > 5:
                    continue
                if txt_line.find('q')==1 or txt_line.find('Q') == 1:
                    q += 1
                elif txt_line.find('w')==1 or txt_line.find('W') == 1:
                    w += 1
                elif txt_line.find('e')==1 or txt_line.find('E') == 1:
                    e += 1
                elif txt_line.find('r')==1 or txt_line.find('R') == 1:
                    r += 1
    qwer[0].append(q)
    qwer[1].append(w)
    qwer[2].append(e)
    qwer[3].append(r)        

    x_val = []
    for i in range(timer_count + 1):
        x_val.append(i * timer)
    #print(x_val)
    for i in range(4):
        plt.plot(x_val, qwer[i])
    plt.xticks(x_val)
    plt.ylabel('Count')
    plt.xlabel('Time')
    plt.title('q,w,e,r COUNT')
    plt.legend(['Q','W','E','R'])
    plt.show()

def input_txt():
    with open("Test{}.txt".format(num),'w') as txt_file:
        for t in range(len(input_keyboard)):
            txt_file.write('%s\n' %input_keyboard[t])

def handlePress(key):
    global first_time, input_keyboard, chat, timer, num
    if key == Key.page_up:
        #chk.value = 0
        input_txt()
        return False
    if key == Key.enter: #챗팅칠땐 스킬을 못 쓰고 2번째 쓸경우 
        chat = not chat #입력하여 챗팅을 종료하는 의미이므로
    elif key == Key.esc: #esc키를 치면 챗팅시스템은 강제종료된다.
        chat = False

    if len(input_keyboard)>=1000:
        input_txt()
        num += 1
        input_keyboard.clear()

    if not chat:
        input_keyboard.append(time.time())
        input_keyboard.append(key)
    #print(input_keyboard)

class Exam(QWidget):    
    def __init__(self):
        super().__init__() #생성자
        self.initUI()
    
    def initUI(self):
        self.main_label = QLabel('MESSAGE : 측정 후 그래프를 눌러주세요.\n\t    디폴트 시간은 30초입니다.')

        self.btn1 = QPushButton('측정시작')
        self.btn1.clicked.connect(self.start_s)

        btn2 = QPushButton('그래프')
        btn2.clicked.connect(self.view_graph)

        btn3 = QPushButton('타이머주기 바꾸기')
        btn3.clicked.connect(self.change_timer)
        self.timer_s = QLineEdit()

        btn4 = QPushButton('초기화')
        btn4.clicked.connect(self.reset)

        btnbox2 = QGridLayout()
        btnbox2.addWidget(self.btn1, 0, 0)
        btnbox2.addWidget(QLabel('종료버튼은 PageUp입니다.'), 0, 1)
        btnbox2.addWidget(btn2, 1, 0)
        btnbox2.addWidget(QLabel('그래프를 표시해줍니다.'), 1, 1)
        btnbox2.addWidget(btn4, 2, 0)
        btnbox2.addWidget(QLabel('다시 측정해야하고 주기는 30초로 변경합니다.'), 2, 1)
        btnbox2.addWidget(btn3, 3, 0)
        btnbox2.addWidget(self.timer_s, 3, 1)
        group_box = QGroupBox()
        group_box.setLayout(btnbox2)
        
        btnbox = QVBoxLayout()
        btnbox.addWidget(self.main_label)
        
        btnbox.addWidget(group_box)

        self.setGeometry(500, 500, 400, 400) #창크기
        self.setLayout(btnbox)
        self.setWindowTitle('키보드값 추출기') #이름
        self.show()  #눈에보이기.
        
    def start_s(self):
        global first_time
        self.btn1.setEnabled(False)
        self.main_label.setText('MESSAGE : 측정완료\n\t    다시 측정하려면 초기화를 눌러주세요')
        first_time = time.time()
        self.hide()
        with Listener(on_press=handlePress) as listener:
            listener.join()
            self.show()
    #def start_ss(self):
        #global first_time
        #self.btn1.setEnabled(False)
        #self.main_label.setText('MESSAGE : 측정완료\n\t    다시 측정하려면 초기화를 눌러주세요')
        #first_time = time.time()
        #with Listener(on_press=handlePress) as listener:
        #    listener.join()
    def view_graph(self):
        self.main_label.setText('MESSAGE : 그래프 출력')
        #print('그래프 출력')
        sort_graph()
    
    def change_timer(self):
        global timer
        if(len(self.timer_s.text()) == 0):
            print(timer)
            self.main_label.setText('MESSAGE : 숫자를 입력해주세요') 
            return
        timer=int(self.timer_s.text())
        self.main_label.setText('MESSAGE : {}초로 변경완료'.format(timer))
        self.timer_s.setText('')
        #print(timer)
    
    def reset(self):
        global timer, num
        self.btn1.setEnabled(True)
        timer = 30
        num = 0
        input_keyboard.clear()
        qwer.clear()
        self.main_label.setText('MESSAGE : 초기화 완료. 다시 측정하세요.')
def start_UI():
    app = QApplication(sys.argv) #어플리케이션 객체를 생성하는 단계 인자는 명령줄을 제어하는 부분
    w = Exam()
    sys.exit(app.exec_()) #프로그램 종료 / 인자는 이벤트처리를 위한 루프도는것(메인이라고 볼수도 있다.)
#  메인루프가 다 끝나면 exit로 종료

if __name__ == "__main__":
    start_UI()