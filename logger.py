import tkinter as tk
import cv2
from datetime import datetime
import pandas as pd
from tkinter import simpledialog



root = tk.Tk()
# hometeam = simpledialog.askstring("Home team", "Input name of home team.", parent = root)
# awayteam = simpledialog.askstring("Away team", "Input name of away team.", parent = root)
# half = simpledialog.askstring("Half", "Which half of play? (Either 1ST or 2ND)", parent = root)

hometeam = 'YL'
awayteam = 'LCS'
half = '1ST'

todaysdate = datetime.today().date()

left_click = cv2.imread("left_click.png")
right_click = cv2.imread("right_click.png")


startstatus = True
def draw_circle(event, x, y, flags, param):
    global startstatus, templist, image, teampos

    f = open(f"{hometeam}-{awayteam} ({todaysdate})-{half}.txt", "a+")

    if event == cv2.EVENT_LBUTTONUP:
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('Log', image)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if startstatus is True:
            templist = []

            print('offensive sequence start')

            previmage = image.copy()

            cv2.putText(image, "start", (x + 6, y + 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 2)

            cv2.putText(image, "|///|   |",
                        (863, 18), cv2.FONT_HERSHEY_PLAIN, 0.5, (3, 127, 252), 2)

            cv2.imshow('Log', image)


            image = previmage
            templist.extend([x,y,current_time])
            startstatus = False
            teampos = 'home'

        else:
            templist.extend([x,y,current_time])
            # print(hometeam, templist, current_time)


            if len(templist) == 6:
                previmage = image.copy()

                cv2.putText(image, "|///|   |",
                            (863, 18), cv2.FONT_HERSHEY_PLAIN, 0.5, (3, 127, 252), 2)

                cv2.imshow('Log', image)

                image = previmage

                print('action before last')

            if len(templist) == 9:
                print('last action')
                print(f"{hometeam},{awayteam},{templist[0]},{templist[1]},{templist[2]},{templist[3]},{templist[4]},{templist[5]},{templist[6]},{templist[7]},{templist[8]}")
                f.write(f"{hometeam},{awayteam},{templist[0]},{templist[1]},{templist[2]},{templist[3]},{templist[4]},{templist[5]},{templist[6]},{templist[7]},{templist[8]}\n")
                f.close()
                startstatus = True
                teampos = 'null'


    if event == cv2.EVENT_RBUTTONUP:
        cv2.circle(image, (x, y), 5, (255, 255, 0), -1)

        cv2.imshow('Log', image)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if startstatus is True:
            templist = []

            print('offensive sequence start')

            previmage = image.copy()

            cv2.putText(image, "|   |///|",
                        (863, 18), cv2.FONT_HERSHEY_PLAIN, 0.5, (3, 127, 252), 2)

            cv2.putText(image, "start", (x + 6, y + 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 0), 2)

            cv2.imshow('Log', image)

            image = previmage
            templist.extend([x, y, current_time])
            startstatus = False
            teampos = 'away'

        else:
            templist.extend([x,y,current_time])
            # print(hometeam, templist, current_time)


            if len(templist) == 6:
                previmage = image.copy()

                cv2.putText(image, "|   |///|",
                            (863, 18), cv2.FONT_HERSHEY_PLAIN, 0.5, (3, 127, 252), 2)

                cv2.imshow('Log', image)

                image = previmage

                print('action before last')

            if len(templist) == 9:
                print('last action')

                f.write(f"{awayteam},{hometeam},{templist[0]},{templist[1]},{templist[2]},{templist[3]},{templist[4]},{templist[5]},{templist[6]},{templist[7]},{templist[8]}\n")
                f.close()
                startstatus = True
                teampos = 'null'


    if event == cv2.EVENT_MBUTTONUP:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if startstatus is True:
            print("Shot happened without defined offensive sequence, please define start x-y")
            previmage = image.copy()
            cv2.putText(image, "start not defined", (1160,799), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1)
            cv2.imshow('Log', image)

            image = previmage

        else:
            templist.extend([x, y, current_time])
            # print(hometeam, templist, current_time)
            cv2.circle(image, (x, y), 5, (255, 255, 255), -1)
            previmage = image.copy()
            cv2.putText(image, "shot", (x+6, y+6), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 2)
            cv2.imshow('Log', image)
            image = previmage

            if teampos == 'home':
                f.write(f"{hometeam},{awayteam},{templist[0]},{templist[1]},{templist[2]},{templist[3]},{templist[4]},{templist[5]},{templist[6]},{templist[7]},{templist[8]},Shot\n")
                f.close()
                startstatus = True

            if teampos == 'away':
                f.write(f"{awayteam},{hometeam},{templist[0]},{templist[1]},{templist[2]},{templist[3]},{templist[4]},{templist[5]},{templist[6]},{templist[7]},{templist[8]},Shot\n")
                f.close()
                startstatus = True




image = cv2.imread('soccer-field-grey-s.png')

cv2.imshow('Log', image)
cv2.setMouseCallback('Log', draw_circle)
cv2.waitKey(0)
cv2.destroyAllWindows()