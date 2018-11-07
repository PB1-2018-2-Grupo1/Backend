import face_recognition
import cv2
import os
import sqlite3
#[0] id , [1] matricula e [2] photo_code

img_code=[]
img_code_list=[]
# conectando...
conn = sqlite3.connect('../back/db.sqlite3')
# definindo um cursor
cursor = conn.cursor()

#pega as linhas de usuário do banco de dados
cursor.execute("""SELECT user_id,matricula,photo_code FROM user_student Where user_id>=21;""")

#dividir a string obtida da conexão do banco de dados
for linha in cursor.fetchall():
    #print(linha)

	#inicia os arrays para cada aluno
    img_code=[]
    img_id=[]
    img_matricula=[]

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

print(len(img_code_list))

#inicía a web cam
video_capture = cv2.VideoCapture(0)

#array básicos dos nomes e dos códigos dos alunos (ver se coloca tipo dicionário)
known_face_encodings=[]
known_face_names=[]


#add dinâmicamente da lista obtida do banco.
for r in img_code_list:
    known_face_names.append(str(r[0]))
    known_face_encodings.append(r[2])

#print (known_face_encodings)
#print (known_face_names)


# Initialize some variables
#código básico do face_recognition.
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Estranho"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                command = "start cmd /K echo " + name
                os.system(command)

            face_names.append(name)

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

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
