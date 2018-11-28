# -*- coding: utf-8 -*-
import face_recognition
import cv2
import os
import string
import sqlite3
from datetime import datetime
#[0] id , [1] matricula e [2] photo_code

def selectTime (var,dateVarString):
	date = [];
	array_times = [[6,8],[8,10],[10,12],[12,14],[14,16],[16,18],[18,20],[20,22],[22,23]]
	date_time = [2]
	date_time.append(datetime.strptime((dateVarString+'-'+str(array_times[var][0])),'%Y-%m-%d-%H'))
	date_time.append(datetime.strptime((dateVarString+'-'+str(array_times[var][1])),'%Y-%m-%d-%H'))
	return date_time

#turma na qual a qual o programa está vinculado.
group_id = 2  #Projeto
lista_id_alunos_registeredgroup = [] #ints e strings

group_list_date_time = [] #lista de ref para  registered_id,date,time,student_id,presença




#Class
# conectando...
conn = sqlite3.connect('../back/db.sqlite3')
# definindo um cursor
cursor = conn.cursor()
#pega as linhas de usuário do banco de dados

cursor.execute("SELECT group_id,student_id,id FROM user_registeredgroup Where group_id="+str(group_id)+";")
for i in cursor.fetchall():
	a = str(i).split(",")
	lar=[]
	lar.append(int(a[1]))
	lar.append(int(a[2][0:-1]))
	lista_id_alunos_registeredgroup.append(lar)

print lista_id_alunos_registeredgroup

cursor.execute("SELECT registered_id,date,time,id FROM user_attendancesheet Where present='Chamada nao realizada';")

for temp in cursor.fetchall():
	temp = str(temp).split(",")
	gr = []
	gr.append(int(temp[0][1:])) #registered_id
	#gr.append(datetime.strptime(temp[1][3:-1],'%Y-%m-%d')) #data
	#gr.append(int(temp[2][3:-2])) #periodo entre 0 a 8
	gr.append(selectTime(int(temp[2][3:-1]),temp[1][3:-1]))

	for ii in lista_id_alunos_registeredgroup:
		if(ii[1]==gr[0]):
			gr.append(ii[0])

	gr.append('Falta')

	gr.append(int(temp[3][1:-1]))

	group_list_date_time.append(gr)
	print temp

#Formato da lista
#registered_id, data e hora aula início e fim, student_id, presente
for ii in group_list_date_time:
	print ii

#lista de alunos para a aula em questão

isGroupTime = False

group_list_date_time_2 = []
date_hoje = datetime.now()


for ii in group_list_date_time:
	if(date_hoje.day==ii[1][1].day and date_hoje.month==ii[1][1].month and date_hoje.year==ii[1][1].year):
		group_list_date_time_2.append(ii)

time_start = []
time_start = group_list_date_time_2[1][1]

for iii in group_list_date_time_2:
	print iii
for iii in time_start:
	print iii

print (datetime.now())
print (group_list_date_time_2 )
print ((datetime.now().hour >=time_start[1].hour and datetime.now().day ==time_start[1].day and datetime.now().minute>=time_start[1].minute))

while(isGroupTime==False):
	if(datetime.now().hour >=time_start[1].hour and datetime.now().day ==time_start[1].day and datetime.now().minute>=time_start[1].minute):
		isGroupTime=True
	print (isGroupTime)

while(isGroupTime):
	#var temporárias
	img_code_list=[]

	# conectando...
	conn = sqlite3.connect('../back/db.sqlite3')
	# definindo um cursor
	cursor = conn.cursor()
	#pega as linhas de usuário do banco de dados
	for ii in group_list_date_time:
			cursor.execute("SELECT user_id,matricula,photo_code FROM user_student WHERE user_id="+str(ii[2])+";")

			#dividir a string obtida da conexão do banco de dados
			for linha in cursor.fetchall():
				#inicia os arrays para cada aluno
			    img_code=[]
			    img_id=[]
			    img_matricula=[]

			    #separa cada linah da resposta em cada e pega matricula e id
			    s = str(linha).split(",")
			    img_id = str(s[0][1:len(s[0])])
			    img_matricula = str(s[1][3:-1])

			    #pegando a string com o código da face da pessoa e transformando
			    #em um array de floats
			    s3 = str(s[2][4:-3]).split(" ")
			    while '' in s3: s3.remove('')
			    t2 = 0.0
			    for t1 in s3:
			        try:
			            t2=float(t1)
			        except ValueError,e:
			            t2=float(t1[0:-2])
			        img_code.append(t2)
			    s=[]
			    s.append(img_id)
			    s.append(str(img_matricula))
			    s.append(img_code)
			    img_code_list.append(s)

	conn.close()

	#array básicos dos nomes e dos códigos dos alunos (ver se coloca tipo dicionário)
	known_face_encodings=[]
	known_face_names=[]

	#add dinâmicamente da lista obtida do banco.
	for r in img_code_list:
	    known_face_names.append(str(r[0]))
	    known_face_encodings.append(r[2])

	#contador de alunos
	len = len(img_code_list)

	#lista por aluno na turma -
	#código - hora de entrada - hora de saida
	attendancesheet_list = [len]

	#criando lista com flags para alunos presentes


	#inicía a web cam
	video_capture = cv2.VideoCapture(0)

	# Initialize some variables
	#código básico do face_recognition.
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	start_time = []
	start_time.append(datetime.now().hour)
	start_time.append(datetime.now().minute)
	end_time = []
	end_time.append(start_time[0]+1)
	end_time.append(start_time[1]+40)

	while (True):#(datetime.now().hour< end_time[0] || (datetime.now().hour == end_time[0] && datetime.now().minute < end_time[1]):
	    # Grab a single frame of video
	    ret, frame = video_capture.read()

	    # Resize frame of video to 1/4 size for faster face recognition processing
	    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

	    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	    rgb_small_frame = small_frame[:, :, ::-1]

	    # Only process every other frame of video to save time
	    if (process_this_frame and isGroupTime):
	        # Find all the faces and face encodings in the current frame of video
	        face_locations = face_recognition.face_locations(rgb_small_frame)
	        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

	        face_names = []
	        for face_encoding in face_encodings:
	            # See if the face is a match for the known face(s)
	            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
	            id = "Estranho"


	            # If a match was found in known_face_encodings, just use the first one.
	            if True in matches:

	                ####marca quando o aluno chegar

					first_match_index = matches.index(True)
					id = known_face_names[first_match_index]
					command = "start cmd /K echo " + id
					os.system(command)


					idd=int(known_face_names[first_match_index])
					for iii in group_list_date_time_2:
						if(iii[2]==idd):
							iii[3]="Presente"

	            face_names.append(id)

	    process_this_frame = not process_this_frame


	    # Display the results
	    for (top, right, bottom, left), name in zip(face_locations, face_names):
	        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
	        top *= 4
	        right *= 4
	        bottom *= 4
	        left *= 4

	        # Draw a box around the face
	        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

	        # Draw a label with a name below the face
	        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
	        font = cv2.FONT_HERSHEY_DUPLEX
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	        #escrever nomes
	        print(name)

	    # Display the resulting image
	    cv2.imshow('Video', frame)

	    # Hit 'q' on the keyboard to quit!
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break

	for iiii in group_list_date_time_2:
		print iiii


	#uPDATE DATABASE
	conn = sqlite3.connect('../back/db.sqlite3')

	cursor = conn.cursor()
	#pega as linhas de usuário do banco de dados
	#registered_id, data e hora aula[início , fim], student_id, presente
	for iii in group_list_date_time_2:
		comando = "UPDATE user_attendancesheet SET present='" + str(iii[3]) + "' WHERE id=" + str(iii[4]) + ";"
		print comando
		cursor.execute(comando);
		conn.commit()

	conn.close()
	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()
