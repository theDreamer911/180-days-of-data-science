# Data-Flair
## Step 1: Import required model
import matplotlib.pyplot as plt
from tkinter import filedialog
from PIL import ImageTk, Image 
from tkinter import *
import tkinter as tk
import numpy as np
import easygui
import imageio
import cv2
import sys
import os

## Step 2: Building File Box to choose a particular file
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    ## STEP 3: Way of storing image
    # Reading the image
    original_image = cv2.imread(ImagePath)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # print(image) # iamge is stored in form of numbers

    # Confirming the choosen image
    if original_image is None:
        print("Can't find any image. Choose appropriate files")
        sys.exit()

    Resized1 = cv2.resize(original_image, (960, 540))
    # plt.imshow(Resized1, cmap="gray")

    ## STEP 4: Transforeming an image to grayscale
    # Converting an image to grayscale
    gray_scale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    Resized2 = cv2.resize(gray_scale_image, (960, 540))
    # plt.imshow(Resized2, cmap = "gray")

    ## STEP 5: Smoothing the grayscale image
    # applying median blur to smoothen an image
    smooth_gray_scale = cv2.medianBlur(gray_scale_image, 5)
    Resized3 = cv2.resize(smooth_gray_scale, (960, 540))
    # plt.imshow(Resized3, cmap='gray')

    ## STEP 6: Retrieving the edges of the image
    # Retrieving the edges for cartoon effect using threshold technique
    getEdge = cv2.adaptiveThreshold(smooth_gray_scale, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY, 9, 9)
    Resized4 = cv2.resize(getEdge, (960, 540))
    # plt.imshow(Resized4, cmap='gray')

    # STEP 7: Preparing a mask image
    # Applying bilateral filter to remove noise and keeping the edge sharp
    colorImage = cv2.bilateralFilter(original_image, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960, 540))
    # plt.imshow(Resized5, cmap='gray')

    # STEP &: Giving a cartoon effect
    # Masking edged image with our "Beautify" image
    cartoon_image = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    Resized6 = cv2.resize(cartoon_image, (960, 540))
    # plt.imshow(Resized6, cmap='gray')
    
    # STEP 9: Plotting all the transitions together
    # Plotting the whole transition
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={"xticks":[], "yticks":[]},
                gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    # Saving button code
    ## STEP 13: Adding save button in the main window
    save1 = Button(top, text="Save cartoon image", command=lambda:save(ImagePath, Resized6),
                    padx=30, pady=5)
    save1.configure(background="#364156", foreground="white", font=("calibri", 10, 'bold'))
    save1.pack(side=TOP, pady=50)
                    
    plt.show()

## STEP 10: Functionally of save button
def save(Resized6, ImagePath):
    # Saving image using imwrite
    new_name = "cartoonified_image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, new_name + extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_BGR2BGR))
    i = "Image saved: " + new_name + " at " + path
    tk.messagebox.showinfo(title=None, message=I)

## STEP 11: Making the main window
top = tk.Tk()
top.geometry('400x400')
top.title("Cartoonify Your Image !")
top.configure(background="white")
label = Label(top, background="#CDCDCD", font=("calibri", 20, 'bold'))

## STEP 12: Making button for cartoonify
upload=Button(top, text="Cartoonify the Image", command=upload, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)


## STEP 14: Main Function
top.mainloop()