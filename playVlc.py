import time, vlc, os, random, youtube_dl, requests, json
from bs4 import BeautifulSoup
import urllib3
import threading, sys
import urllib.parse, re, requests
import socket
from urllib.error import URLError
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
import csv

kill1=1
tr=0
volume=50
max_song=0
is_stop=0
Checky1=None
set_rand=0
new_open=0
selecting=0
nowa=0
player = None
mix_list=None
ready=0
title_list=None
yt_init='https://www.youtube.com/watch?v='
yt_ops={'quiet': True}            
controls_frame = None 

headers = {
                        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.115', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'}
rand_num=[]
play_button = None
now_song = None
text = None
tex1 = None
text2 = None
list_box = None
kk=0
d=0
k=0
error=0

def get_media(url,name):
    h=0
    while True:
        if(h>2):
            print("Unable to extract URL with")
            text2.set("로그: 재생할 수 없는 노래 발견 제목: " + name)

            return "Unable"
        info=None
        with youtube_dl.YoutubeDL(yt_ops) as ydl:
            try:
                info = ydl.extract_info(url, download=False)['formats']
            except youtube_dl.utils.DownloadError as e:
                h+=1
                continue
        
        for myInfo in info:
            #if 'mp4a' in myInfo['acodec'] and myInfo['vcodec']=='none':
            if myInfo['format_id'] == '140':
                #print(myInfo)
                urls = myInfo['url']
                if(urls.split() == ""):
                    h+=1
                    continue
                if(chk(urls)=="200"):
                    return urls
                else:
                    continue

def video(source):
    global nowa, player, rand_title, text, vlc_instance, title_list, k, selecting, text1, volume, play_button
    

    #vlc_instance.log_set(log_callback, None)
    
    
     
    # creating a media player
    player = vlc_instance.media_player_new()
    player.audio_set_volume(volume)
    my_event_manger = player.event_manager()
    #my_event_manger.event_attach(vlc.EventType.MediaPlayerMediaChanged, media_change)
    my_event_manger.event_attach(vlc.EventType.MediaPlayerEndReached, media_finish)
    if(set_rand==0):
        print("playing: " + title_list[nowa])
    else:
        print("playing: " + title_list[rand_num[nowa]])
     
    # creating a vlc instance
    
    # creating a media
    if('http' in source):
        media = vlc_instance.media_new(source)
    else:
        media = vlc_instance.media_new("D:/mp3/"+source)

     
    # setting media to the player
    player.set_media(media)
    player.play()
    back_btn_img = tk.PhotoImage(file=resource_path("play-fill.png"))
    
    play_button.configure(image=back_btn_img)
    play_button.image = back_btn_img
    for selected in range(len(list_box.curselection())):
        list_box.select_clear(list_box.curselection()[selected])
    if(set_rand==0):
        text1.set(title_list[nowa])
        k=0
        list_box.selection_set(nowa)
        list_box.see(nowa)
    else:
        text1.set(title_list[rand_num[nowa]])

        list_box.selection_set(rand_num[nowa])
        list_box.see(rand_num[nowa])
def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)
class App2(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()


    def run(self):
        global player, text, kk, d, selecting, list_box, error, tr, kill1
        while True:
            if(error==1):
                time.sleep(2)
                continue
            else:
                if(player.get_state() == vlc.State.Playing):
                    

                    duration = player.get_length()
                    if(duration==-1):
                        continue

                    #print("duration: " + str(min)+":"+str(sec))
            

                    if(d==0 and is_stop==0):
                        
                        

                        kk = int(player.get_time()/1000)
                        if(kk==0):
                            continue
                        if(kk==int(player.get_length()/1000)):
                            continue
                        
                        if(kk!=-1):
                            d=1

                    if(kk!=-1):
                        min1=kk/60
                        sec1=kk%60  
                    else:
                        min1=0
                        sec1=0

                    min = int(duration/60000)
                    sec = int((duration/1000)%60)
                    text.set(str('%02d'%min1) + ":" + str('%02d'%sec1)+" | " + str('%02d'%min) + ":" + str('%02d'%sec))
                
                    kk+=1
                    if(tr==1):
                        for selected in range(len(list_box.curselection())):
                            list_box.select_clear(list_box.curselection()[selected])
                        if(set_rand==0):
                            list_box.selection_set(nowa)
                            list_box.see(nowa)
                        else:
                            list_box.selection_set(rand_num[nowa])
                            list_box.see(rand_num[nowa])  
                        tr=0
                    time.sleep(1)
                    if(len(list_box.curselection())>1):
                        for selected in range(len(list_box.curselection())):
                            list_box.select_clear(list_box.curselection()[selected])
                        if(set_rand==0):
                            list_box.selection_set(nowa)
                            list_box.see(nowa)
                        else:
                            list_box.selection_set(rand_num[nowa])
                            list_box.see(rand_num[nowa])    
            if(kill1==0):
                text.set(str("00:00 | 00:00"))    
                kill1=1

def onselect():
    global list_box, player, mix_list, nowa, d, k, kk, selecting, error

    player.stop()
    if(len(list_box.curselection())>0):
        nowa=list_box.curselection()[0]
        serr=0
        while True:
        
            if(set_rand==1):
                o=0
                for chka in rand_num:
                    
                    if chka == nowa:
                        nowa=o
                        break
                    o+=1
                media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])
            else:
                media = get_media(mix_list[nowa],title_list[nowa])

            if(media=="Unable"):
                serr+=1
                nowa+=1
                if(nowa==max_song):
                    nowa=0
                if(serr>3):
                    messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                    return False
                continue
            else:
                error=0
                video(media)
                d=0
                kk=0
                selecting=1
                serr=0
                return False 
    else:
        messagebox.showerror("오류", "재생할 곡이 없습니다.")
def delete_all():
    global player, list_box,title_list,mix_list,max_song, text, text1
    player.stop()

    list_box.delete(0, tk.END)
    max_song=0
    title_list = []
    mix_list = []
    text.set("")
    text1.set("")
    messagebox.showinfo("안내", "모든 노래를 삭제하였습니다.")
def onselect_delete():
    global player,d,rand_num,list_box,title_list,mix_list,nowa,max_song,set_rand, error, d, is_stop
    if(len(list_box.curselection())>0):
        selection=list_box.curselection()[0]
        if(nowa==selection):
            player.stop()
        list_box.delete(selection)
        max_song-=1
        #del(rand_num[rand_num[selection]])
        del(title_list[selection])
        del(rand_num[selection])
        del(mix_list[selection])
        if(nowa==selection):
            d=0
            is_stop=0
            serr=0
            while True:
                if(set_rand==0):
                    media = get_media(mix_list[nowa],title_list[nowa])
                else:
                    media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])

                if(media=="Unable"):
                    serr+=1
                    nowa+=1
                    if(nowa==max_song):
                        nowa=0
                    if(serr>3):
                        messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                        return False
                    continue
                else:
                    error=0
                    video(media)
                    return False
    else:
        messagebox.showerror("오류", "삭제할 곡이 없습니다.")
def openReal(yturl):
    global player, rand_num, list_box, title_list,mix_list, nowa, max_song,d,kk,ready, new_open, error
    #mix_init = requests.get('https://www.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m', headers=headers)
    #init_plid=str(mix_init.text).split('videoId":"')[1].split('"')[0]
    title_list1, mix_list1 = get_pl(yturl)
    if(title_list1 == False):
        messagebox.showerror("오류", '올바른 플레이리스트 URL인지 확인하여주세요.')
    else:

        title_list = title_list + title_list1
        mix_list = mix_list + mix_list1

        max_song=len(mix_list)

        a = random.sample(range(0,max_song),max_song)

        num=len(mix_list1)
        for cu in a:
            rand_num.append(cu)
           
        new_open=1

        for i in range(len(title_list1)):
            list_box.insert(tk.END, title_list1[i])
        messagebox.showinfo("안내", "성공적으로 %s개의 곡을 추가하였습니다."%(str(num)))




    #print(mix_list)
    #print(rand_num[nowa])

    d=0
    kk=0
def add_top100():
    global title_list, mix_list
    try:
        mix_init = requests.get('https://www.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m', headers=headers)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("no internets")
    init_plid=str(mix_init.text).split('videoId":"')[1].split('"')[0]
    openReal('https://www.youtube.com/watch?v=%s&list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m'%(init_plid))
def openYT():
    global player, rand_num, list_box, title_list,mix_list, nowa, max_song,d,kk,ready, new_open, error
    if(ready==0):
        return False
    yturl = simpledialog.askstring(title = "open YT Playlist",
                                    prompt = "유튜브 플레이 리스트 URL")
    if(yturl==None):
        return False

    openReal(yturl)
def load_list():
    global title_list, mix_list, max_song, o
    filename = filedialog.askopenfilename(initialfile='playlist', defaultextension='.csv', initialdir="./preset", title="재생목록 불러오기",
                                          filetypes=(("CSV", "*.csv"), 
                                          ("all files", "*.*")))
    if not filename:
        messagebox.showerror("오류", "재생목록 열기 실패")
    else:
        print(filename)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                line = f.readline()
                num=0
                while line:
                    val1 = line.split(",")[0].replace(";", ",")
                    val2 = line.split(",")[1]
                    title_list.append(val1)
                    mix_list.append(val2)

                    list_box.insert(tk.END, val1)
                    
                    line = f.readline()
                    num+=1
                max_song=len(mix_list)
                a = random.sample(range(0,max_song),max_song)
                o=0
                for cu in a:
                    #print(cu)
                    rand_num.append(cu)
                
            messagebox.showinfo("안내", str(num)+"개의 곡을 추가하였습니다.")
            
        except PermissionError as e:
            messagebox.showerror("오류", "재생목록 불러오기 실패")
        except Exception as e:
            messagebox.showerror("오류", "재생목록 불러오기 실패, 올바른 재생목록인지 확인해주세요.")
            print(e)
def save_list():
    global title_list, mix_list
    filename = filedialog.asksaveasfilename(initialfile='playlist', defaultextension='.csv', initialdir="./preset", title="재생목록 저장",
                                          filetypes=(("CSV", "*.csv"), 
                                          ("all files", "*.*")))
    if not filename:
        messagebox.showerror("오류", "재생목록 저장 실패")
    else:
        print(filename)
        try:
            num=0
            with open(filename, 'w', encoding='utf-8-sig') as f:
                for i in range(len(title_list)):
                    num+=1
                    title_list[i] = str(title_list[i]).replace(',', ';')
                    f.write(title_list[i]+','+mix_list[i]+'\n')
            messagebox.showinfo("안내", "%s개의 곡을 저장목록에 저장하였습니다."%(str(num)))
        except PermissionError as e:
            messagebox.showerror("오류", "재생목록 저장 실패, 다른 이름으로 저장해주세요.")
        except Exception as e:
            messagebox.showerror("오류", "재생목록 저장 실패")
def openYT_txt():
    global title_list, mix_list, max_song
    filename = filedialog.askopenfilename(initialfile='playlist', defaultextension='.csv', initialdir="./preset", title="재생목록 불러오기",
                                          filetypes=(("TXT", "*.txt"), 
                                          ("all files", "*.*")))
    if not filename:
        messagebox.showerror("오류", "재생목록 열기 실패")
    else:
        print(filename)
        openYTR_txt(filename)

def openYTR_txt(filename):
    f = open(filename, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    openReal(text)
    
def openYT_URL():
    global player, rand_num, list_box, title_list,mix_list, nowa, max_song,d,kk,ready, new_open
    if(ready==0):
        return False
    yturl = simpledialog.askstring(title = "open YT URL",
                                    prompt = "유튜브 URL 추가")
    if(yturl==None):
        return False
    add1url(yturl)


def openYT1(self):
    global player,rand_num, list_box, title_list,mix_list, nowa, max_song,d,kk,ready, new_open, error
    if(ready==0):
        return False
    yturl = simpledialog.askstring(title = "open YT Playlist",
                                    prompt = "유튜브 플레이 리스트 URL")
    if(yturl==None):
        return False
    openReal(yturl)

def ttk_slider_callback(value):
    global volume
    volume = int(float(value))
    player.audio_set_volume(volume)
def set_random():
    global Checky1, set_rand, nowa, max_song, rand_num
    set_rand=(Checky1.get())
    if(max_song>0):
        if(set_rand==0):
            nowa=rand_num[nowa]
        if(set_rand==1):

            rand_num=[]
            a = random.sample(range(0,max_song),max_song)
            o=0
            for cu in a:
                #print(cu)
                rand_num.append(cu)
            if(nowa == cu):
                nowa=o
def on10forward():
    global player,d
    d=0
    player.set_time(player.get_time()+10000)
def on10back():
    global player,d
    d=0
    if(player.get_time()>10001):
        player.set_time(player.get_time()-10000)
    else:
        player.set_time(0)

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()
    def on_closing(self):
        MsgBox = tk.messagebox.askquestion ('안내','종료하시겠습니까?',icon = 'error')
        if MsgBox == 'yes':
            quit()
    def ondouble_play(self, event):
        global list_box, player, mix_list, nowa, d, k, kk, selecting, error, tr,play_button,is_stop
        
        player.stop()
        if(len(list_box.curselection())>0):
            nowa=list_box.curselection()[0]
            serr=0
            while True:
                
                if(set_rand==1):
                    o=0
                    for chka in rand_num:
                        
                        if chka == nowa:
                            nowa=o
                            break
                        o+=1

                    media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])
                else:
                    media = get_media(mix_list[nowa],title_list[nowa])

                if(media=="Unable"):
                    serr+=1
                    nowa+=1
                    if(nowa==max_song):
                        nowa=0
                    if(serr>3):
                        messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                        return False
                    continue
                else:
                    error=0
                    video(media)
                    k=1
                    d=0
                    is_stop=0
                    kk=0
                    selecting=1
                    serr=0
                    tr=1
                    back_btn_img = tk.PhotoImage(file=resource_path("play-fill.png"))
                    
                    play_button.configure(image=back_btn_img)
                    play_button.image = back_btn_img
            

                    return False 
 
    def chk(self):
        time.sleep(5)
        try:
            mix_init = requests.get('https://www.youtube.com/playlist?list=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m', headers=headers)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("no internets")
            messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요. 플레이어를 종료합니다.")
            self.root.destroy()
    def onEsc_key(self, event):
        global list_box
        for selected in range(len(list_box.curselection())):
            list_box.select_clear(list_box.curselection()[selected])
        if(set_rand==0):
            list_box.selection_set(nowa)
            list_box.see(nowa)
        else:
            list_box.selection_set(rand_num[nowa])
            list_box.see(rand_num[nowa])    
    def ondelete_key(self, event):
        global player,d,rand_num,list_box,title_list,mix_list,nowa,max_song,set_rand, error, d, is_stop
        if(len(list_box.curselection())>0):
            selection=list_box.curselection()[0]
            if(nowa==selection):
                player.stop()
            list_box.delete(selection)
            max_song-=1
            #del(rand_num[rand_num[selection]])
            del(title_list[selection])
            del(rand_num[selection])
            del(mix_list[selection])
            if(nowa==selection):
                serr=0
                d=0
                is_stop=0
                while True:
                    if(set_rand==0):
                        media = get_media(mix_list[nowa],title_list[nowa])
                    else:
                        media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])

                    if(media=="Unable"):
                        serr+=1
                        nowa+=1
                        if(nowa==max_song):
                            nowa=0
                        if(serr>3):
                            messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                            return False
                        continue
                    else:
                        error=0
                        video(media)

                        return False
        else:
            messagebox.showerror("오류", "삭제할 곡이 없습니다.")
        
    def run(self):
        global play_button, controls_frame, now_song, text, list_box, Checky1, text1, text2


        self.root = tk.Tk()
        self.root.title('Youtube Music Player')
        self.root.iconbitmap(resource_path("player.ico"))
        self.root.geometry("650x400")
        self.root.resizable(False, False)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.root.bind('<Control-o>', openYT1)

        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        editmenu = tk.Menu(menubar, tearoff=0)
        savemenu = tk.Menu(menubar, tearoff=0)
        

        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Edit", menu=editmenu)

        menubar.add_cascade(label="MYList", menu=savemenu)
        filemenu.add_command(label="유튜브 플레이리스트 추가 (txt 파일)", command=openYT_txt)
        filemenu.add_command(label="유튜브 플레이리스트 URL 추가", command=openYT)
        
        filemenu.add_command(label="유튜브 URL 추가", command=openYT_URL)
        editmenu.add_command(label="선택한 곡 삭제", command=onselect_delete)
        editmenu.add_command(label="모든 곡 삭제", command=delete_all)
        
        savemenu.add_command(label="저장된 재생목록 가져오기", command=load_list)
        savemenu.add_command(label="현재 재생목록을 파일로 저장", command=save_list)
        frm = tk.Frame(self.root)
        frm.grid(row=0, column=0, sticky=tk.N+tk.S)
        #window.rowconfigure(1, weight=1)
        #window.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(1, weight=1)




        text = tk.StringVar()
        text1 = tk.StringVar()
        text2 = tk.StringVar()
        text2.set("로그: 문제없음")


        scrollbar = tk.Scrollbar(frm,orient="vertical")		# 스크롤바 생성
        scrollbar.pack(side=tk.RIGHT, fill = "y")
        

        list_box = tk.Listbox(frm, width=40, height=20,yscrollcommand=scrollbar.set, activestyle=tk.NONE)
        list_box.pack(expand=True, fill=tk.Y, padx=10, pady=15)
        list_box.bind("<Double-Button-1>", self.ondouble_play)
        list_box.bind("<Delete>", self.ondelete_key)
        list_box.bind("<Escape>", self.onEsc_key)
        #list_box.bind('<<ListboxSelect>>', onselect)

        scrollbar.config(command = list_box.yview)


        back_btn_img = tk.PhotoImage(file=resource_path("rewind-fill.png"))
        
        forward_btn_img = tk.PhotoImage(file=resource_path("speed-fill.png"))
        play_btn_img = tk.PhotoImage(file=resource_path("play-fill.png"))
        stop_btn_img = tk.PhotoImage(file=resource_path("stop-fill.png"))


        forward_btn=tk.Button(self.root, text="10초 >>",command=on10forward)
        forward_btn.place(x=480, y=120)

        back_btn=tk.Button(self.root, text="<< 10초",command=on10back)
        back_btn.place(x=410, y=120)


        want_btn=tk.Button(self.root, text="선택한 곡 재생",command=onselect)
        want_btn.place(x=470, y=200, anchor="center")

        now_song = tk.Label(self.root, textvariable=text, font=("맑은고딕", 13, "italic"))
        now_song1 = ttk.Label(self.root, textvariable=text1, wraplength=250, font=("맑은고딕", 11, "italic"))
        error_label = tk.Label(self.root, textvariable=text2, wraplength=200)

        back_button = tk.Button(self.root, image=back_btn_img, borderwidth=0, command=pre_song, state=tk.NORMAL)
        forward_button = tk.Button(self.root, image=forward_btn_img, borderwidth=0, command=next_song)
        play_button = tk.Button(self.root, image=play_btn_img, borderwidth=0, command=control_play_pause)
        stop_button = tk.Button(self.root, image=stop_btn_img, borderwidth=0, command=stop_song)
        Checky1=tk.IntVar()
        checkbutton1=tk.Checkbutton(self.root, text="Shuffle", variable=Checky1, command=set_random)

        checkbutton1.place(x=440, y=330)
        
        actual_slider = ttk.Scale(self.root, from_=0, to=100,
                                command=ttk_slider_callback, value=50)

        actual_slider.place(x=470, y=300,anchor="center")
        now_song.place(x=430, y=20)
        now_song1.place(x=480, y=80,anchor="center")
        error_label.place(x=470, y=250, anchor="center")
        
        back_button.place(x=390, y=150)
        play_button.place(x=440, y=150)
        stop_button.place(x=490, y=150)
        forward_button.place(x=540, y=150)


        
        
        # self.root.protocol("WM_DELETE_WINDOW", self.callback)

        # label = tk.Label(self.root, text="Hello World")
        # label.pack()
        self.root.config(menu=menubar)
        t = threading.Thread(target=self.chk)
        t.start()
        self.root.mainloop()



def chk(na):
    req = urllib.request.Request(urllib.parse.unquote(na))
    try:
        res = urllib.request.urlopen(req, timeout=2)
        print(res.status)
        if(res.status!=200):
            return "Forbidden"

        else:
            return "200"
    except urllib.error.HTTPError as e:
        return "Forbidden"
    except URLError as error:
        print(error.reason)
        if isinstance(error.reason, socket.timeout):

            return "200"

        elif(len(str(error.reason).split("Errno"))>0):
            if str(error.reason).split("Errno")[1].split("]")[0].strip()=="101":

                return "200"
        else:
            print("other error")
            return "Forbidden"



def next_song():
    global player, nowa,kk,d, list_box, mix_list,rand_num,max_song, error,play_button,is_stop

    
    player.stop()
    if(max_song>0):
        kk=0
        d=0
        is_stop=0
        nowa+=1
        if(nowa==max_song):
            print("초기화")
            nowa=0
        #print(rand_num[nowa])
        serr=0
        while True:
            if(set_rand==0):
                media = get_media(mix_list[nowa],title_list[nowa])
            else:
                media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])

            if(media=="Unable"):
                serr+=1
                nowa+=1
                if(nowa==max_song):
                    nowa=0
                if(serr>3):
                    messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                    return False
                continue
            else:
                error=0
                video(media)

        
                return False

    #player.set_position(0.7)




def pre_song():
    global player, nowa,kk,d, list_box, mix_list,rand_num, error

    if(max_song>0):
        kk=0
        d=0
        if(nowa==0):
            print("초기화")
            nowa=max_song-1
        else:
            nowa-=1
        player.stop()
        #print(rand_num[nowa])
        serr=0
        while True:
            if(set_rand==0):
                media = get_media(mix_list[nowa],title_list[nowa])
            else:
                media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])
            if(media=="Unable"):
                serr+=1
                nowa+=1
                if(nowa==0):
                    nowa=max_song-1
                if(serr>3):
                    messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                    return False
                continue
            else:
                error=0
                video(media)
                d=0
                return False
    #player.set_position(0.7)


def stop_song():
    global player, nowa, d, is_stop, play_button, kill1

    vlc_status = player.get_state()
    if(vlc_status == vlc.State.Playing):
        player.stop()
        d=0
        is_stop=1
        kill1=0
        back_btn_img = tk.PhotoImage(file=resource_path("pause-fill.png"))
        
        play_button.configure(image=back_btn_img)
        play_button.image = back_btn_img


def control_play_pause():
    global player, play_button, controls_frame, is_stop, d
    while True:
        vlc_status = player.get_state()
        if(vlc_status == vlc.State.Playing):
            player.pause()
            is_stop=1

            back_btn_img = tk.PhotoImage(file=resource_path("pause-fill.png"))
            
            play_button.configure(image=back_btn_img)
            play_button.image = back_btn_img
            

            return "stop"
        else:
            player.play()
            is_stop=0
            d=0

            back_btn_img = tk.PhotoImage(file=resource_path("play-fill.png"))
            
            play_button.configure(image=back_btn_img)
            play_button.image = back_btn_img
            return "start"


def pause():
    global player
    while True:
        vlc_status = player.get_state()
        if(vlc_status == vlc.State.Playing):
            player.pause()
            return "stop"


def play():
    global player
    while True: 
        vlc_status = player.get_state()
        if(vlc_status == vlc.State.Paused):
            player.pause()
            return "play"

def default():
    return "hello"
def add1url(url):
    global title_list, mix_list, max_song,rand_num,list_box
    h=0
    if(str(url).find('youtube.com')==-1 and str(url).find('youtu.be')==-1):
        url='https://www.youtube.com/watch?v='+url
    while True:
        if(h>3):
            print("adding error")
            messagebox.showerror("오류", "음악 추가 실패")
            return "Error"
        try:
            with youtube_dl.YoutubeDL(yt_ops) as ydl:
                info_dict = ydl.extract_info(url, download=False)
        except youtube_dl.utils.DownloadError as e:
            messagebox.showerror("오류안내", "재생할 수 없는 유튜브 URL입니다.")
            return False
        video_id = info_dict.get("id", None)
        video_title = info_dict.get('title', None)
        if(video_title.strip() == ""):
            h+=1
            continue
        
        astral = re.compile(r'([^\u0000-\uffff])')
        new_subject = ""
        for j, ss in enumerate(re.split(astral, video_title)):
            if not j%2:
                new_subject += ss
            else:
                new_subject += '?' 
        
        mix_list.append(yt_init+video_id)
        title_list.append(video_title)
        list_box.insert(tk.END, video_title)
        max_song+=1
        a = random.sample(range(0,max_song),max_song)
        for cu in a:
            #print(cu)
            rand_num.append(cu)
        messagebox.showinfo("안내", "성공적으로 음악을 추가하였습니다.")
        return True

 


def get_pl(url):
    mix = None
    while True:
        try:
            if(url.find('playlist?list=')!=-1 or url.find('&list=')!=-1):
                mix = requests.get(url, timeout=5, headers=headers)
            else:
                return False, False
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("no internet")
        
        except Exception as e:
            time.sleep(2)
            continue

        soup = BeautifulSoup(mix.content, 'html.parser', from_encoding="utf8")
        search_results = str(soup.findAll("script"))

        if ("var ytInitialData = " in str(search_results)):

            str1 = search_results.strip().split('var ytInitialData = ')[1].split(';</script>')[0]
            j1 = json.loads(str1, encoding='utf8', strict=False)
            #f=open("C:/bin/0919.txt", 'w', encoding='utf-8')
            #f.write(str1)
            #f.close()
            toGet = []
            titleList = []
            try:
                if(url.find('playlist?list=')!=-1):
                    u = str(j1['contents']['twoColumnBrowseResultsRenderer']).split("playlistVideoRenderer")
                    l_num = len(u)
                    print(len(u))
                    for i in range(1, l_num):
                        my = str(u[i])
                        
                        vid = my.split(r"videoId': ")[1][1:].split(",")[0][:-1]
                        print(vid)
                        tit= my.split(r"[{'text': ")[1][1:].split('}')[0][:-1]
                        if(vid.split() !='' and vid.split()):
                            astral = re.compile(r'([^\u0000-\uffff])')
                            new_subject = ""
                            for j, ss in enumerate(re.split(astral, tit)):
                                if not j%2:
                                    new_subject += ss
                                else:
                                    new_subject += '?' 
                            toGet.append(yt_init+vid)
                            titleList.append(tit)
                    return titleList, toGet
                elif(url.find('&list=')!=-1):
                    #print(j1['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents'][0]['playlistPanelVideoRenderer']) ==> debug용
                    for i in j1['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents']:
                        if 'unplayableText' not in i['playlistPanelVideoRenderer']:

                            
                            astral = re.compile(r'([^\u0000-\uffff])')
                            old =  i['playlistPanelVideoRenderer']['title']['simpleText']
                            new_subject = ""
                            for j, ss in enumerate(re.split(astral, old)):
                                if not j%2:
                                    new_subject += ss
                                else:
                                    new_subject += '?' 
                            titleList.append(new_subject)
                            
                            toGet.append(yt_init+i['playlistPanelVideoRenderer']['videoId'])
                    return titleList, toGet

            except:
                messagebox.showerror("오류", "올바른 플레이리스트 URL이 아닙니다")
                return False, False

        else:
            print("에러")
            return False, False

def media_change(event):
    global player
    time.sleep(3)
    vlc_status = player.get_state()
    s=0
    
    while s==0:
        if(vlc_status == vlc.State.Playing):
            duration = player.get_length()

            min = int(duration/60000)
            sec = int((duration/1000)%60)
            print("duration: " + str(min)+":"+str(sec))
        
            s=1
        
        vlc_status = player.get_state()


def media_finish(event):
    
    global nowa, player,d,list_box,kk, error
    kk=0
    print("미디어 종료")
    nowa+=1
    if(nowa==max_song):
        print("초기화")
        nowa=0
    serr=0
    while True:
        if(set_rand==0):
            media = get_media(mix_list[nowa],title_list[nowa])
        else:
            media = get_media(mix_list[rand_num[nowa]],title_list[rand_num[nowa]])

        if(media=="Unable"):
            serr+=1
            nowa+=1
            if(nowa==max_song):
                nowa=0
            if(serr>3):
                messagebox.showerror("오류", "인터넷에 연결이 되어있는지 확인해주세요.")
                return False
            continue
        else:
            error=0
            video(media)
            d=0
            return False

vlc_instance = vlc.Instance('--verbose -1')
player = vlc_instance.media_player_new()

if __name__ == "__main__":
    
    app1 = App()
    app2 = App2()
    ready=1
    title_list=[]
    mix_list=[]