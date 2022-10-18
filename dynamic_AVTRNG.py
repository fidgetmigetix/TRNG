#W- frames width H- frames height
#RGB- red,green,blue
#We only take 8-15 frames of size 320X200 pixels per second
#And the coordinate threshold vt is a filter; if the
#RGB difference between current coordinate and the previous
#coordinate is less than vt, then adopt another coordinate. The
#vt could be set as any image’s half variance; thus, we set vt as
#half variance of the video frame in the 3rd second. And we
#set the discard threshold 𝑡ℎ = 100. If we cannot get available
#RGB (𝑥, 𝑦) coordinate more than th times, then discard this
#frame and go to the next frame.

from datetime import timedelta
import cv2
import numpy as np
import os
from PIL import Image
import glob
import matplotlib.pyplot as plt
from moviepy.editor import *
import array
import wave
from PIL import Image, ImageStat
import pyaudio
import time
from random import randint




def trng():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    i = 0

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 60
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)



    frames_audio = []
    image_list = []

    #working loading audio    
    print("* recording AUDIO for: "+ str(RECORD_SECONDS))
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames_audio.append(data)
    print("* done recording AUDIO")

    #saving audio file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames_audio))
    wf.close()

    #getting audio values
    audiovalues=wave.open('output.wav', 'rb')
    signal = audiovalues.readframes(-1)

    soundwave= np.frombuffer(signal, dtype='int16')

    audiovalues.close()

    os.remove("output.wav")

    timeofwebcam=0
    timeout = time.time() + 60*3 

    for i in range(0, int(RATE / CHUNK * (RECORD_SECONDS+60))):
        #frame- frame of video
        ret, frame = cap.read()

        # This condition prevents from infinite looping
        # incase video ends.
        # if ret == False:
        #     break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("* done recording")
            break

        

        #loading frames from video- working
        #print(frame) 

        # Save Frame by Frame into disk using imwrite method
        #cv2.imwrite('Frame'+str(i)+'.jpg', frame)
        cv2.imshow('frame', frame)
        image_list.append(frame)
        i += 1
        timeofwebcam += 1
    

    stream.stop_stream()
    stream.close()
    p.terminate()
    cap.release()
    cv2.destroyAllWindows()




    W=320
    H=200

    #wspolrzedne image o wymiarach 320x200
    x_start=480
    x_end=800
    y_start=260
    y_end=460






    # cv2.imshow('cropped',image_list(2))

    first_image=image_list[2]
    #format= BGR zamiast RGB
    #9 wartosci rgb wokol srodka image 
    first_color= first_image[159,99].item(2)<<16 + first_image[159,99].item(1)<<8 + first_image[159,99].item(0)
    first_color1= first_image[160,99].item(2)<<16 + first_image[160,99].item(1)<<8 + first_image[160,99].item(0)
    first_color2= first_image[161,99].item(2)<<16 + first_image[161,99].item(1)<<8 + first_image[161,99].item(0)
    first_color3= first_image[159,100].item(2)<<16 + first_image[159,100].item(1)<<8 + first_image[159,100].item(0)
    first_color4= first_image[160,100].item(2)<<16 + first_image[160,100].item(1)<<8 + first_image[160,100].item(0)
    first_color5= first_image[161,100].item(2)<<16 + first_image[161,100].item(1)<<8 + first_image[161,100].item(0)
    first_color6= first_image[159,101].item(2)<<16 + first_image[159,101].item(1)<<8 + first_image[159,101].item(0)
    first_color7= first_image[160,101].item(2)<<16 + first_image[160,101].item(1)<<8 + first_image[160,101].item(0)
    first_color8= first_image[161,101].item(2)<<16 + first_image[161,101].item(1)<<8 + first_image[161,101].item(0)

    color_firstRGB_SUM= (first_color + first_color1 + first_color2 + first_color3 + first_color4 + first_color5 + first_color6 + first_color7 + first_color8)//9


    x_global=color_firstRGB_SUM%(W//2) + W//4
    y_global=color_firstRGB_SUM%(H//2) + H//4
    x=x_global
    y=y_global

    R=first_image[x,y].item(2)
    G=first_image[x,y].item(1)
    B=first_image[x,y].item(0)

    convert_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114]) 
    #setting vt
    vt = convert_to_gray(image_list[33])
    #settig th
    th=100
    #setting watchdog
    watchdog=0


    im = image_list[0]
    vt = np.var(im)/2
    #23
    # print(vt)
    #K=5880
    K=8372

    amountofnum=1000
    #which byte from sound
    j=0
    #which number of frame
    num_frame=2
    #bit 0-7
    i=0
    #runcnt
    runcnt=0
    #list of random numbers
    random_number_generated=bytearray()
    #calculating random bits
    rand_bits_count=0
    #𝑅1, 𝐺1, 𝐵1,𝑅2, 𝐺2, and 𝐵2 be equal to zero firstly
    R1=R2=G1=G2=B1=B2=0

    # &	Bitwise AND	x & y
    # |	Bitwise OR	x | y
    # ~	Bitwise NOT	~x
    # ^	Bitwise XOR	x ^ y
    # >>	Bitwise right shift	x>>
    # <<	Bitwise left shift	x<<

    # SN1= byte_array[j]>>(10+(R*i + (G<<2) + B + runcnt)% ( K/2))
    # SN2= byte_array[j]>>(15+(R*i + (G<<3) + B + runcnt)% ( K/2))
    # SN3= byte_array[j]>>(20+(R*i + (G<<4) + B + runcnt)% ( K/2))
    # SN4= byte_array[j]>>(5+(R*i + (G<<1) + B + runcnt)% ( K/2))
    # SN5= byte_array[j]>>(25+(R*i + (G<<5) + B + runcnt)% ( K/2))
    # SN1= byte_array[j]>>(10+(R2*i + (G2<<2) + B2 + runcnt)% ( K/2))
    # SN2= byte_array[j]>>(15+(R2*i + (G2<<3) + B2 + runcnt)% ( K/2))
    # SN3= byte_array[j]>>(20+(R2*i + (G2<<4) + B2 + runcnt)% ( K/2))
    # SN4= byte_array[j]>>(5+(R2*i + (G2<<1) + B2 + runcnt)% ( K/2))
    # SN5= byte_array[j]>>(25+(R2*i + (G2<<5) + B2 + runcnt)% ( K/2))

    result=1

    #If diff (𝑅𝐺𝐵, last 𝑅𝐺𝐵)2 < vt
    isdiff= True
    #watchdog>th?
    iswatchdogbigger= True
    #randomnumber- number we create
    randomnumber=''
    #random bit we create
    randombit=0
    #stage of getting random bit
    getRandombit=False
    #is thresholdBigger
    tresholdIs=False

    #       SN1 = sound byte𝑗 [10 + (𝑅 ∗ 𝑖 + (𝐺 ≪ 2) + 𝐵 +
    #       runcnt)% (𝐾/2)];
    #       SN2 = sound byte𝑗 [15 + (𝑅 ∗ 𝑖 + (𝐺 ≪ 3) + 𝐵 +
    #       runcnt)% (𝐾/2)];
    #       SN3 = sound byte𝑗 [20 + (𝑅 ∗ 𝑖 + (𝐺 ≪ 4) + 𝐵 +
    #       runcnt)% (𝐾/2)];
    #       SN4 = sound byte𝑗 [5 + (𝑅 ∗ 𝑖 + (𝐺 ≪ 1) + 𝐵 +
    #       runcnt)% (𝐾/2)];
    #       SN5 = sound byte𝑗 [25 + (𝑅 ∗ 𝑖 + (𝐺 ≪ 5) + 𝐵 +
    #       runcnt)% (𝐾/2)];
    #       𝑗 = 𝑗 + 1; move to next 𝐾 sound bytes.
    while amountofnum!=0:
        #If diff (𝑅𝐺𝐵, last 𝑅𝐺𝐵)2 < vt
        if iswatchdogbigger:
            if(j>soundwave.size):
                j=soundwave.size-randint(10, 100)
            SN1= (soundwave.item(j)>>(10+(R*i + (G<<2) + B + runcnt)% ( K//2)))
            SN2= (soundwave.item(j)>>(15+(R*i + (G<<3) + B + runcnt)% ( K//2)))
            SN3= (soundwave.item(j)>>(20+(R*i + (G<<4) + B + runcnt)% ( K//2)))
            SN4= (soundwave.item(j)>>(5+(R*i + (G<<1) + B + runcnt)% ( K//2)))
            SN5= (soundwave.item(j)>>(25+(R*i + (G<<5) + B + runcnt)% ( K//2)))
            j=j+1
            K=K+3000
            j=K
            if rand_bits_count==100000:
                runcnt=runcnt+1 
            isdiff=True
        if isdiff:
            if(num_frame>=len(image_list)):
                num_frame= len(image_list) - randint(50,len(image_list))
            our_frame= image_list[num_frame]
            # print(x)
            # print(y)
            R=our_frame[x,y].item(2)
            G=our_frame[x,y].item(1)
            B=our_frame[x,y].item(0)
            tresholdIs=True
        if tresholdIs==True:
            if ((R-R1)**2 + (G-G1)**2 + (B-B1)**2) < vt:
                x= (x + (R^G)+1)%W
                y= (y + (G^B)+1)%H
                watchdog=watchdog+1
                if watchdog>th:
                    num_frame=num_frame+1
                    iswatchdogbigger=True
                    isdiff=True
                    getRandombit=False
                else:
                    iswatchdogbigger=False
                    isdiff=True
                    getRandombit=False
            else:
                isdiff=False
                getRandombit=True
                iswatchdogbigger=False
                tresholdIs=False

        if getRandombit==True:
            randombit=1&(R^G^B^R1^G1^B1^R2^G2^B2^SN1^SN2^SN3^SN4^SN5)
            # print(randombit)
            randomnumber=randomnumber+str(randombit)
            x=(((R^x)<<4)^(G^y))%W
            y=(((G^x)<<4)^(B^y))%H
            R1=R
            G1=G
            B1=B
            i=i+1
            rand_bits_count=rand_bits_count+1
            iswatchdogbigger=False
            isdiff=True


            if(i==8):
                randomnumber=int(randomnumber,2)
                # print(randomnumber)
                i=0
                #writing numbers to txt file
                # with open('numbers.txt', 'w') as f:
                #     f.write(str(randomnumber)+"\n")
                random_number_generated.append(randomnumber)
                amountofnum=amountofnum-1
                # result *= randomnumber
                
                R2=R
                G2=G
                B2=B
                iswatchdogbigger=True
                isdiff=True

                randomnumber=''

    

    # # Creating histogram
    # fig, ax = plt.subplots(figsize =(10, 7))
    # ax.hist(random_number_generated, bins = 280, range=[1, 280])
    
    # # Show plot
    # plt.show()

    # print(random_number_generated)

    unit8typeList= np.array(random_number_generated)


    # imgg = unit8typeList.astype(np.uint8)
    imgg=unit8typeList.tobytes()

    return imgg

    # with open('data.txt', 'wb') as f:
    #     np.save(f, imgg)

    marg2 = np.histogramdd(np.ravel(random_number_generated), bins = 256)[0]/len(random_number_generated)
    marg2 = list(filter(lambda p: p > 0, np.ravel(marg2)))
    entropy2 = -np.sum(np.multiply(marg2, np.log2(marg2)))
    print ("entropy2", entropy2)
