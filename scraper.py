# importing the necessary libraries for the web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv

# defining the chromedriver path
path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.maximize_window()
wait = WebDriverWait(driver, 60)

# creating an empty list and dictionary to store the extracted date
data = []
review = {}
end = 1  # variable to determine the end of loop
page = 1   # variable to determine the page

# beginning of the loop
while end:

    # url is updated every time we move to next page, variable 'page' determines the page number
    driver.get("https://www.walmart.com/reviews/product/14898365?page=" + str(page) + "&sort=submission-desc")

    # each page has 20 reviews hence looping for 20 times
    for i in range(1, 21):

        # locating the review in the page using XPATH, variable 'i' determines the review number of the page
        review_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div[6]/div[1]/div[' + str(i) + ']')))

        # extracting the located review as HTML script
        html_review = driver.execute_script("return arguments[0].innerHTML;", review_box)

        # using the unique id's of each element we identify the data using simple string search operations

        # identifying the date when the review was posted
        date_posted = re.search(r'review-date-submissionTime\">(.*?)</span>', html_review).group(1)

        # we need to extract data until we reach December 2020, so creating a condition to exit the loop/ stop extraction when we reach December 2020
        if 'December' in str(date_posted) and '2020' in str(date_posted):
            end = 0
            break

        # identifying the reviewer's name aka nickname
        name = re.search(r'review-footer-userNickname\">(.*?)</span>', html_review).group(1)

        # identifying the title for the review
        # few reviewers don't tend to add any title, hence checking for Nil values and then identifying the content
        if re.search(r'review-title font-bold\">(.*?)<', html_review) is not None:
            title = re.search(r'review-title font-bold\">(.*?)<', html_review).group(1)
        else:
            title = None

        # identifying the description for the review
        if re.search(r'review-text\"><p>(.*?)</p>', html_review) is not None:
            description = re.search(r'review-text\"><p>(.*?)</p>', html_review).group(1)
        else:
            description = ""

        # identifying the ratings given by the reviewer, converting the stars to number rating out of 5
        rating = html_review.count("elc-icon star star-small star-rated elc-icon-star-rating")

        # storing the extracted data in a dictionary
        review['Review date'] = str(date_posted)

        # splitting the date posted to year, month and date for easy analysis and visualization
        year = date_posted.split(', ')[1]
        date = date_posted.split(', ')[0].split()[1]
        month = date_posted.split(', ')[0].split()[0]

        review['Year'] = str(year)
        review['Month'] = str(month)
        review['Date'] = str(date)
        review['Reviewer name'] = str(name)
        review['Review title'] = str(title)
        review['Description'] = str(description)
        review['Rating (out of 5)'] = str(rating)

        # storing the dictionary into a list of dictionary that contains all the reviews
        data.append(review.copy())

    # updating the page
    page = page + 1

# close the website after completing the extraction
driver.close()

# converting the extracted data from list of dictionaries to CSV file
# finding the headers or keys
keys = review.keys()
# converting the data to csv
with open('output.csv', 'w', encoding="utf-8", newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data)
