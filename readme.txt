How does the code work?

- I used python selenium web driver to perform the task of data extraction from the Walmart product website.
- There exists a pattern in reviews, every review follows the same syntax and we can uniquely identify the rating, reviewer name, heading, description using the class of the div tag.
- After extracting the HTML for each review, I used simple python string functions to pick the data placed between the HTML tags.
- After identifying the syntax of the URL we see that there exists a pattern for each page. I used this pattern to navigate around the pages with ease and speed rather than using the next page button.
- The collected data was stored as a list of dictionaries and then processed to CSV format.

What challenges did I face?

- The only challenge I faced was to convert the star rating into the numeric rating, which I was able to solve by understanding the CSS of the rating.

What else I can improve?

- We can try to understand the emotion of the rating description using NLP.
- We can also understand the data using Tableau for visualization to understand which month has more 5 star ratings etc.

How to make it work on other retailers as well?

- The method in which I wrote the code was simple to use and applicable for all the other retailers as well, all we need to do is update the URL with the new product link.
