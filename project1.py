#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
After eating chocolate bars your whole life, you’ve decided to go on a quest to
find the greatest chocolate bar in the world.

You’ve found a website that has over 1700 reviews of chocolate bars from all 
around the world. It’s displayed in the web browser on this page.

The data is displayed in a table, instead of in a csv or json. Thankfully, we
have the power of BeautifulSoup that will help us transform this webpage into
a DataFrame that we can manipulate and analyze.

The rating scale is from 1-5, as described in this review guide. A 1 is 
“unpleasant” chocolate, while a 5 is a bar that transcends “beyond the ordinary
limits”.

Some questions we thought about when we found this dataset were: Where are the
best cocoa beans grown? Which countries produce the highest-rated bars? What’s
the relationship between cocoa solids percentage and rating?

Can we find a way to answer these questions, or uncover more questions, using
BeautifulSoup and Pandas?
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


'''
Let’s make a request to this site to get the raw HTML, which we can later turn
into a BeautifulSoup object.

The URL is:

https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html
'''
webpage = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html')

'''
Create a BeautifulSoup object called soup to traverse this HTML.

Use "html.parser" as the parser, and the content of the response you got from
your request as the document.
'''
soup = BeautifulSoup(webpage.content, 'html.parser')

'''
How many terrible chocolate bars are out there? And how many earned a perfect 5?
Let’s make a histogram of this data.

The first thing to do is to put all of the ratings into a list.

Use a command on the soup object to get all of the tags that contain the ratings.
'''
ratings_tags = soup.find_all(attrs={'class':'Rating'})

'''
Create an empty list called ratings to store all the ratings in.
'''
ratings = []

'''
Loop through the ratings tags and get the text contained in each one. Add it to
the ratings list.

As you do this, convert the rating to a float, so that the ratings list will be
numerical. This should help with calculations later.
'''
#the first line of ratings_tags contains the header. That's why we skipped this position
for tag in ratings_tags[1:]:
    tag_content = tag.get_text()
    tag_content = float(tag_content)
    ratings.append(tag_content)

'''
Using Matplotlib, create a histogram of the ratings values
'''
plt.hist(ratings)
plt.title('Distribution of Chocolate Ratings')
plt.show()
plt.clf()

'''
We want to now find the 10 most highly rated chocolatiers. One way to do this
is to make a DataFrame that has the chocolate companies in one column, and the
ratings in another. Then, we can do a groupby to find the ones with the highest
average rating.
'''
company_tags = soup.select('.Company')
company_names = []
# We have to ignore header here as well
for tag in company_tags[1:]:
    company_names.append(tag.get_text())

'''
Create a DataFrame with a column “Company” corresponding to your companies 
list, and a column “Ratings” corresponding to your ratings list.
'''
dictionary = {'Company':company_names, 'Ratings':ratings}
df_1 = pd.DataFrame.from_dict(dictionary)
# getting the ten best company ratings
ten_best = df_1.groupby('Company').Ratings.mean().nlargest(10)
print(ten_best)

'''
We want to see if the chocolate experts tend to rate chocolate bars with higher
levels of cacao to be better than those with lower levels of cacao.

It looks like the cocoa percentages are in the table under the Cocoa Percent
column.

Using the same methods you used in the last couple of tasks, create a list that
contains all of the cocoa percentages. Store each percent as a float, after 
stripping off the % character.
'''
cocoa_percent_tags = soup.select('.CocoaPercent')
cocoa_percent = []
for tag in cocoa_percent_tags[1:]:
    percent = float(tag.get_text().strip('%'))
    cocoa_percent.append(percent)
# Updating the dataframe
df_1['CocoaPercentage'] = np.array(cocoa_percent)

'''
Make a scatterplot of ratings (your_df.Rating) vs percentage of cocoa
(your_df.CocoaPercentage).Is there any correlation here? We can use some numpy
commands to draw a line of best-fit over the scatterplot.
'''
plt.scatter(df_1.CocoaPercentage, df_1.Ratings)
plt.title('Ratings vs Percentage of Cocoa')
plt.xlabel('Percentage')
plt.ylabel('Rating')
z = np.polyfit(df_1.CocoaPercentage, df_1.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df_1.CocoaPercentage, line_function(df_1.CocoaPercentage), "r--")
plt.show()
    