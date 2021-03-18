import telebot
import os.path

bot = telebot.TeleBot('Bot Token')


re_text_file = ""
chat_id_global = ""


print("Start")

@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
	check_file = os.path.exists(str(message.chat.id)+".txt")
	if check_file == True:
		print("Файл есть")
	else:
		f = open(str(message.chat.id)+".txt", "w")
		f.close()

	print(message.new_chat_members[0].id)
	user_name = message.new_chat_members[0].first_name
	user_id = message.new_chat_members[0].id
	print()
	with open(str(message.chat.id)+".txt", "r") as f:
		for line in f:  #iterate over the file one line at a time(memory efficient)
			print("Just line: " + line)
			print("Split Line: " + line.split()[0])
			if line.split()[0] == str(user_id):    #if string found is in current line then print it
				print("Search append")
				try:
					bot.kick_chat_member(message.chat.id, user_id) #Кик пользователя
				except:
					bot.send_message(message.chat.id, "У бота недостаточно прав чтобы выгнать пользователя.")

	bot.send_message(message.chat.id, "Добро пожаловать")	#Приветсвие новых пользователей (можно убрать)

@bot.message_handler(content_types=["left_chat_member"])
def leave_member(message):
	check_file = os.path.exists(str(message.chat.id)+".txt")
	if check_file == True:
		print("Файл есть")
	else:
		f = open(str(message.chat.id)+".txt", "w")
		f.close()

	id_boolean_num = 0
	print(message.left_chat_member.id)
	user_name = message.left_chat_member.first_name
	user_id = message.left_chat_member.id

	#Проверям есить ли этот пользователь в бд или нет
	with open(str(message.chat.id)+".txt", "r") as f:
		for line in f:
			print(line)
			print(line.split()[0])
			file_count = line.split()
			id_boolean = file_count.count(str(user_id))
			if id_boolean >= 1:
				id_boolean_num = 1 

	#Если нет, то добавляем
	f = open(str(message.chat.id)+".txt", "a")
	if id_boolean_num == 0:
		if user_name != " ":
			f.write(str(user_id) + " " + user_name + "\n")
		else:
			f.write(str(user_id) + "\n")
	f.close()

@bot.message_handler(commands=['unban'])
def unban(message):
	global chat_id_global
	chat_id_global = message.chat.id

	check_file = os.path.exists(str(message.chat.id)+".txt")
	if check_file == True:
		print("Файл есть")
	else:
		f = open(str(message.chat.id)+".txt", "w")
		f.close()

	msg = bot.reply_to(message, "Выбирите пользователя чтобы убрать его из черного списка.")
	i = 1
	list_id = ""
	with open(str(message.chat.id)+".txt", "r") as f:
		for line in f:  #iterate over the file one line at a time(memory efficient)	
			try:
				list_id = list_id + str(i) + "." + " " + str(line.split()[0])  + " " + str(line.split()[1] + "\n")
			except:
				list_id = list_id + str(i) + "." + " " + str(line.split()[0] + "\n")
			i = i + 1
	bot.send_message(message.chat.id, list_id)

	
	bot.register_next_step_handler(msg, un_ban_step)

def un_ban_step(message):
	global chat_id_global
	global re_text_file
	i = 0
	now_line = 0
	try:
		id_clear = int(message.text)
	except:
		id_clear = message.text

	f = open(str(chat_id_global)+".txt", "r")
	for line in f:  #iterate over the file one line at a time(memory efficient)	
		i = i + 1
	f.close()

	if type(id_clear) == type(2) and id_clear <= i:
		with open(str(message.chat.id)+".txt", "r") as f:
			for line in f:  #iterate over the file one line at a time(memory efficient)
				now_line = now_line + 1
				re_text_file = re_text_file + line
				if now_line == id_clear:
					line_replace = line
	else: 
		bot.send_message(message.chat.id, "Ошибка. Неверное число")

	re_text_file = re_text_file.replace(line_replace, "", 1)
	print(line_replace)

	f = open(str(chat_id_global)+".txt", "w")
	f.write(re_text_file)
	f.close()

	chat_id_global = ""
	re_text_file = ""

bot.polling()