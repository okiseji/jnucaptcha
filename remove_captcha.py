import os
import time

import requests
from PIL import Image, ImageDraw
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def save_img(driver):
    bg_img_src = driver.find_element(By.CLASS_NAME, "yidun_bg-img").get_attribute("src")
    response = requests.get(bg_img_src)
    img_data = response.content
    f = open('image.jpg', 'wb')
    f.write(img_data)


def find_different_area():
    # Load the original image and the most similar image
    img_A = Image.open('image.jpg')
    pixels_A = img_A.convert('L').load()

    filename = find_most_similar()
    # print(filename)
    img_B = Image.open('./Background/' + filename)
    pixels_B = img_B.convert('L').load()

    # Get the size of the images
    width, height = img_A.size

    # Find the position of the first different pixel
    for x in range(width):
        for y in range(height):
            if abs(pixels_A[x, y] - pixels_B[x, y]) > 100:
                img_draw = ImageDraw.Draw(img_A)
                img_draw.line((x, 0, x, img_A.size[1]), 'red')
                img_A.save('drawed.jpg')
                return (x, y)

    # If no different pixel is found, return None
    return None


def find_most_similar():
    # Open the original image and resize it
    img = Image.open('image.jpg')
    img = img.resize((100, 100))

    # Convert the image to grayscale
    gray_img = img.convert('L')
    original_pixels = gray_img.load()

    # Folder path containing the images
    folder_path = './Background'

    # Initialize variables to keep track of the most similar image and its score
    most_similar_filename = None
    highest_score = 0

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        img = Image.open(os.path.join(folder_path, filename))
        img = img.resize((100, 100))
        gray_background = img.convert('L')
        background_pixels = gray_background.load()

        # Compare the pixels of the original image with the pixels of the background image
        score = 0
        for x in range(100):
            for y in range(100):
                if original_pixels[x, y] == background_pixels[x, y]:
                    score += 1

        # Update the most similar image and its score
        if score > highest_score:
            most_similar_filename = filename
            highest_score = score

    # Return the filename of the most similar image
    return most_similar_filename

def remove_captcha(driver):
    times = 0
    while True:
        driver.get('https://libsouthic.jnu.edu.cn/user')
        time.sleep(2.0)
        try:
            save_img(driver)
            distance = find_different_area()
            button_element = driver.find_element(By.CLASS_NAME, 'yidun_slider')
            ActionChains(driver).click_and_hold(button_element).perform()
            ActionChains(driver).move_by_offset(0.75 * distance[0], 0).perform()
            # time.sleep(0.7)
            ActionChains(driver).release().perform()
            time.sleep(2.0)
            times += 1
            try:
                button_element = driver.find_element(By.CLASS_NAME, 'yidun_slider')
                ActionChains(driver).click_and_hold(button_element).perform()
            except:
                print("验证成功 花费" + str(times) + "次")
                break
        except:
            continue
