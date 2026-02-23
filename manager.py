import tkinter as tk
from tkinter import ttk
import time

full_width = 800
full_height = 480

t = 0

# books.txt안에 있는 책 리스트를 읽어오고 
def allBooks():
    f = open('books.txt', 'r', encoding='utf-8')               # 텍스트 파일 읽기
    t = f.readlines()                         # 파일에서 텍스트 받아오기
    books = []                                # 책 리스트
    temp = []
    for i in range(0, len(t), 5):
        temp = [line.strip() for line in t[i:i+4]]
        books.append(temp)
    
    return books

bookslist = allBooks()

# k (0 = 제목, 1 = 지은이)
# a = 대여 가능 유무 (false이면 대여 불가여도 뜸) true는 대여 불가 시 안뜸
# 13주차에 사용한 Naive String Matching Algorithm 을 손 봐 만든 검색 함수
def searching(b, t, k, a):
    books = []
    
    for i in range (len(b)):
        if (a == True and int(b[i][2])-int(b[i][3]) < 1):
            pass
        else:
            if (not t):
                books.append(b[i])
            else:
                for j in range (len(b[i][k]) - len(t) + 1):
                    p = 0
                    if (b[i][k][j] == t[0]):
                        for ii in range(len(t)):
                            if (b[i][k][j+ii] != t[ii]):
                                break
                            elif (ii == len(t) - 1):
                                books.append(b[i])
                                p = 1
                                break
                        if (p != 0): break
    return books
    






class bookManager(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        books = tk.Frame(self)
        books.place(x=0, y=0, width = full_width, height=full_height)

        self.frames = {}

        for F in (main_screen, search_page):
            page_name = F.__name__
            frame = F(parent=books, controller=self)
            self.frames[page_name] = frame
            
            frame.place(x=0, y=0, width=full_width, height=full_height)

        self.show_frame("main_screen")


    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
# 페이지 클래스
# 메인 페이지
class main_screen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.configure(bg="#FAEBD7")    # 배경 기본 색
        
        # 상단 파란색 바
        topF = tk.Frame(self, bg = "#0072BC", width=full_width, height=full_height//5)
        topF.place(x=0, y=0)
        
        # 가운데 프로그램 명
        tk.Label(self, text="도서관리 시스템",bg="#FAEBD7" ,font= "Helvetica 30 bold", fg ="black").place(x=full_width//2, y=full_height*0.4, anchor="center")
        
        # 왼쪽 위 이름
        tk.Label(self, text="Book Manager | 이연주",bg="#0072BC" ,font= "Helvetica 24 bold", fg ="white").place(x=(full_height//5)//2, y=(full_height//5)//2, anchor="w")

        # 메인 페이지 시작 버튼
        Ma_startB = tk.Button(self, text="start", font= "Helvetica 24 bold", bg="white", fg ="black", bd=1,
                              command=lambda: controller.show_frame("search_page"))
        Ma_startB.place(x=full_width//2, y=full_height*0.6, anchor="center")

        # 메인 페이지 종료 버튼
        Ma_exitB = tk.Button(self, text="Exit", font= "Helvetica 14 bold", bg="white", fg ="deep sky blue",command=lambda:exit())
        Ma_exitB.place(x=full_width-(full_height//5)//2, y=(full_height//5)//2,anchor='e')
        


# 검색창 페이지
class search_page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.configure(bg="#FAEBD7")
        
        def on_book_select(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                book_info = bookslist[index]
                rental = True
                if (int(book_info[2])-int(book_info[3]) < 1):
                    rental = False
                try:
                    
                    bookInfo.config(text=f"제목: {book_info[0]}\n저자: {book_info[1]}\n남은 수량: {int(book_info[2])-int(book_info[3])}\n대여 가능: {rental}")
                except:
                    bookInfo.config(text="선택된 책 없음")
        
        able = tk.BooleanVar()
        
        def refresh():
            global bookslist
            bookslist = allBooks()
            book_listbox.delete(0, tk.END)
            for i in range(len(bookslist)):
                book_listbox.insert(tk.END, f"| {bookslist[i][0]} |    | 저자: {bookslist[i][1]} |    |총 {bookslist[i][2]}권|    |대여중: {bookslist[i][3]}권|")
                book_listbox.bind("<<ListboxSelect>>", on_book_select)
            able.set(False)
        
        def search():
            global bookslist, t
            bookslist = allBooks()
            if('저자' == search_type.get()):
                k=1
            else:
                k=0
            st = time.time()    # 타이머 시작
            bookslist = searching(bookslist, search_entry.get(), k, able.get()) # 검색
            et = time.time()    # 타이머 종료
            t = et - st         # 걸린 시간
            book_listbox.delete(0, tk.END)
            for i in range(len(bookslist)):
                book_listbox.insert(tk.END, f"| {bookslist[i][0]} |    | 저자: {bookslist[i][1]} |    |총 {bookslist[i][2]}권|    |대여중: {bookslist[i][3]}권|")
                book_listbox.bind("<<ListboxSelect>>", on_book_select)
            popup = tk.Toplevel()   # 걸린 시간 팝업창
            popup.title('검색 시간')
            popup.geometry("200x100")
            timeL = tk.Label(popup, text='검색 시 걸린 시간: %f초' %t)
            timeL.pack(pady=10)
        
        
        topF = tk.Frame(self, bg="#0072BC", width=full_width, height=full_height//5)
        topF.place(x=0, y=0)
        
        back_btn = tk.Button(topF, text="back", width=5, command=lambda: controller.show_frame("main_screen"))
        back_btn.place(x=(full_height//5)//2+full_width//3, y=(full_height//5)//2,anchor='w')
        
        f5_btn = tk.Button(topF, text="F5", width=5, command=lambda: refresh())
        f5_btn.place(x=(full_height//5)//2+full_width//3+full_width//10, y=(full_height//5)//2,anchor='w')
        
        searchF = tk.Frame(topF, bg='white', width=full_width//3+(full_height//10), height=full_height//5-(full_height//5//7*2))
        searchF.place(x=full_width-(full_height//5//7), y=(full_height//5//7), anchor='ne')
        searchF.pack_propagate(False)
        
        search_type = ttk.Combobox(searchF, values=["제목", "저자"], state="readonly", width=5)
        search_type.set("제목")
        search_type.pack(side='left', padx=5)
        
        search_label = tk.Label(searchF, text="검색 :", bg='white')
        search_label.pack(side='left', padx=5)
        
        search_entry = tk.Entry(searchF)
        search_entry.pack(side='left', padx=5)
        
        search_button = tk.Button(searchF, text="🔍", bg='light gray', command=lambda: search())
        search_button.pack(side='left', padx=5)
        
        infoF = tk.Frame(self, bg='lightgray', width=full_width//3, height=full_height)
        infoF.place(x=0, y=0)
        
        bookInfo = tk.Label(self, text="선택된 책 없음",bg="lightgray")
        bookInfo.place(x=(full_width//3)//2, y=full_height//2, anchor="center")
        
        tool_bar = tk.Frame(self, bg='white', width=full_width-full_width//3, height=(full_height//5)//3)
        tool_bar.place(x=full_width, y=(full_height//5), anchor='ne')
        tool_bar.pack_propagate(False)
                
        able_btn = tk.Checkbutton(tool_bar, bg='white', variable=able)
        able_btn.pack(side='right', padx=5)
        
        tk.Label(tool_bar, bg='white', text='대여 가능한 책만 표시').pack(side='right', padx=5)
        
        rightF = tk.Frame(self, bg="#FAEBD7", width=full_width-full_width//3, height=full_height-(full_height//5)-(full_height//5)//3)
        rightF.place(x=full_width, y=full_height, anchor='se')
        rightF.pack_propagate(False)
        
        book_listbox = tk.Listbox(rightF)
        book_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(rightF, command=book_listbox.yview)
        scrollbar.pack(side='right', fill='y')

        book_listbox.config(yscrollcommand=scrollbar.set)
        
        for i in range(len(bookslist)):
            book_listbox.insert(tk.END, f"| {bookslist[i][0]} |    | 저자: {bookslist[i][1]} |    |총 {bookslist[i][2]}권|    |대여중: {bookslist[i][3]}권|")
        book_listbox.bind("<<ListboxSelect>>", on_book_select)
        
        
        
if __name__=='__main__':        
    app = bookManager()
    app.geometry(f'{full_width}x{full_height}')
    app.resizable(0,0)
    app.mainloop()