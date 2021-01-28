from tkinter import *
import tkinter as tk
import pymysql


window = Tk() #创建窗口
window.title("酒店预订系统") #给窗口命名
window.geometry("500x800+300+200")
#在窗口画布

def displayone():
	sql_1=Tk()
	sql_1.title("第一题结果")
	db=pymysql.connect(
        host='localhost',
            port=3306,
            user='root',
            passwd='123123',
            db='hotel',
            charset='utf8')
	cursor=db.cursor()  #创建游标对象
	sql ="select hotel_name,room_name from hotel natural join room_type;"
	cursor.execute(sql) #执行SQL语句
	results=cursor.fetchall()   #返回结果
	count=len(results)
	canvas = Canvas(sql_1, width = 300, height = 200, bg = "white")
	for i in range(len(results)):
		canvas.create_text(60,30+20*i,text=results[i])
	canvas.pack()
	db.close()

def click2():
	date=date_text.get()
	sql_2=Tk()
	sql_2.title("第二题结果")
	db=pymysql.connect(
         host='localhost',
            port=3306,
            user='root',
            passwd='123123',
            db='hotel',
            charset='utf8')
	cursor=db.cursor()  #创建游标对象
	sql ="select hotel_name,date,avg(price) \
	from hotel natural join room_type natural join room_info \
    where date='%s' \
    group by hotel_name \
    order by avg(price)" %(date)
	cursor.execute(sql) #执行SQL语句
	results=cursor.fetchall()   #返回结果
	count=len(results)
	canvas = Canvas(sql_2, width = 300, height = 200, bg = "white")
	for i in range(len(results)):
		canvas.create_text(100,30+20*i,text=results[i])
	canvas.pack()
	db.close()

def click3():
	start_date=start_date_text.get()
	leave_date=leave_date_text.get()
	num=int(num_text.get())
	print(start_date)
	print(leave_date)
	sql_3=Tk()
	sql_3.title("第三题结果")
	db=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123123',
            db='hotel',
            charset='utf8')
	cursor=db.cursor()  #创建游标对象
	sql ="select hotel_name,room_name,avg(price) \
    from hotel natural join room_type natural join room_info \
    where date<='%s' and date>='%s' \
    group by room_id having min(remain)>=%d \
    order by avg(price)" %(leave_date,start_date,num)
	cursor.execute(sql) #执行SQL语句
	results=cursor.fetchall()   #返回结果
	print(results)
	count=len(results)
	canvas = Canvas(sql_3, width = 300, height = 200, bg = "white")
	for i in range(len(results)):
		canvas.create_text(100,30+20*i,text=results[i])
	canvas.pack()
	db.close()

def click4():
	start_date=start_date_text4.get()
	leave_date=leave_date_text4.get()
	num=int(num_text4.get())
	roomid=int(room_id_text4.get())
	sql_4=Tk()
	sql_4.title("第四题结果")
	db=pymysql.connect(
         host='localhost',
            port=3306,
            user='root',
            passwd='123123',
            db='hotel',
            charset='utf8')
	cursor=db.cursor()  #创建游标对象
	sql1="UPDATE room_info SET remain=remain-%d where date>='%s' and date<='%s' and room_id=%d; "%(num,start_date,leave_date,roomid)
	cursor.execute(sql1)
	sql ="select * from room_info where remain<0;"    #判断是否有remain<0的情况，这种情况是要去除的
	cursor.execute(sql)
	canvas = Canvas(sql_4, width = 300, height = 200, bg = "white")
	results=cursor.fetchall()
	#print(results)
	if results!=():
		canvas.create_text(100,30,text="预订失败，没有这么多空房")
		canvas.pack()
		db.rollback()   #数据库回滚，相当于没有update进行操作
	else:    #当前面的操作成功时，才向order表中插入新的信息
		canvas.create_text(100,30,text="预订成功")
		canvas.pack()
		sql2="INSERT INTO `order` VALUES ('%d','%d','%s','%s','%d',2400,'2018-11-01')"%(5,roomid,start_date,leave_date,num)
		cursor.execute(sql2)
		db.commit()
    
	db.close()

def click5():
	start_date=start_date_text5.get()
	leave_date=leave_date_text5.get()
	print(start_date)
	print(leave_date)
	sql_5=Tk()
	sql_5.title("第五题结果")
	db=pymysql.connect(
         host='localhost',
            port=3306,
            user='root',
            passwd='123123',
            db='hotel',
            charset='utf8')
	cursor=db.cursor()  #创建游标对象
	sql ="select hotel_name,create_date,room_name,amount \
    from `order` join room_type \
    using(room_id) join hotel \
    using(hotel_id) \
    where start_date>='%s' and leave_date<='%s'" %(start_date,leave_date)
	cursor.execute(sql) #执行SQL语句
	results=cursor.fetchall()   #返回结果
	print(results)
	count=len(results)
	canvas = Canvas(sql_5, width = 300, height = 200, bg = "white")
	for i in range(len(results)):
		canvas.create_text(100,30+20*i,text=results[i])
	canvas.pack()
	db.close()


s1=Label(window,text="第一题：").grid(row=0,column=0,pady=10)
s1=Label(window,text="对房间类型查询").grid(row=1,column=0)
B1 = Button(window, text="查询房间类型", command = displayone).grid(row=1,column=1)

s2 = Label(window, text="第二题：").grid(row=2,column=0,pady=10)
s2 = Label(window, text="请输入日期：").grid(row=3,column=0)
date_text = StringVar()
dateBox = Entry(window, textvariable = date_text).grid(row=3,column=1,padx=15)
date_text.set(" ")
Button(window, text="确定", command = click2).grid(row=3,column=2)

s3 = Label(window, text="第三题：").grid(row=4,column=0,pady=10)
s3 = Label(window, text="请输入开始日期：").grid(row=5,column=0)
start_date_text = StringVar()
dateBox3_start = Entry(window, textvariable = start_date_text).grid(row=5,column=1)
s3 = Label(window, text="请输入离开日期：").grid(row=6,column=0)
leave_date_text = StringVar()
dateBox3_leave = Entry(window, textvariable = leave_date_text).grid(row=6,column=1)
s3 = Label(window, text="请输入房间数：").grid(row=7,column=0)
num_text = StringVar()
dateBox3_num = Entry(window, textvariable = num_text).grid(row=7,column=1)
Button(window, text="确定", command = click3).grid(row=7,column=2)

s4 = Label(window, text="第四题：").grid(row=8,column=0,pady=10)
s4 = Label(window, text="请输入开始日期：").grid(row=9,column=0)
start_date_text4 = StringVar()
dateBox4_start = Entry(window, textvariable = start_date_text4).grid(row=9,column=1)
s4 = Label(window, text="请输入离开日期：").grid(row=10,column=0)
leave_date_text4 = StringVar()
dateBox4_leave = Entry(window, textvariable = leave_date_text4).grid(row=10,column=1)
s4 = Label(window, text="请输入房间数：").grid(row=11,column=0)
num_text4 = StringVar()
dateBox4_num = Entry(window, textvariable = num_text4).grid(row=11,column=1)
s4 = Label(window, text="请输入房间号：").grid(row=12,column=0)
room_id_text4 = StringVar()
dateBox4_room = Entry(window, textvariable = room_id_text4).grid(row=12,column=1)
Button(window, text="确定", command = click4).grid(row=12,column=2)


s5 = Label(window, text="第五题：").grid(row=13,column=0,pady=10)
s5 = Label(window, text="请输入开始日期：").grid(row=14,column=0)
start_date_text5 = StringVar()
dateBox5_start = Entry(window, textvariable = start_date_text5).grid(row=14,column=1)
s5 = Label(window, text="请输入离开日期：").grid(row=15,column=0)
leave_date_text5 = StringVar()
dateBox5_leave = Entry(window, textvariable = leave_date_text5).grid(row=15,column=1)
Button(window, text="确定", command = click5).grid(row=15,column=2)

canvas = tk.Canvas(window,bg = 'blue', height=295,width=295)
image_file = tk.PhotoImage(file = 'C:/Users/Administrator/Desktop/tkinter/hotel.gif')
image = canvas.create_image(0,0,anchor = 'nw',image = image_file)
canvas.grid(row=16,column=1)
#创建事件循环直到关闭主窗口
window.mainloop()

