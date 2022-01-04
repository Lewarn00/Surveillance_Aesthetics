import pandas as pd
import datetime
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt  

#Please open binge_website.html before running this script for an example of my finished visualiztion
#This program generates new images for the website
#Input the path to your ViewingActivity.csv file here:
path = '/Users/lewisarnsten/desktop/data_downloads/netflix/netflix-report/CONTENT_INTERACTION/ViewingActivity.csv'
#Input the name of the Neflix profile you would like to visualize here:
profile = 'Lewis'
#Input the start date for the years visualization here:
start = '2020-06-01'

#Reading in the csv, and isolating the data we will use
df = pd.read_csv(path)
named_df = df[df['Profile Name'] == profile]
start_datetime = datetime.datetime.fromisoformat(start)
end = start_datetime + datetime.timedelta(weeks=52) - datetime.timedelta(days=1)
dates = pd.date_range(start=start, end=str(end)[:10])

#Creating a dictionary of dates to keep track of time spent watching Netflix on each day 
dates = [str(x).split(' ')[0] for x in dates]
dct = dict(zip(dates, [0]*len(dates)))
all_shows_watched = [] 

for index, row in named_df.iterrows():
	d = row['Start Time'].split(' ')[0]
	duration_hours = int(row['Duration'].split(':')[0])
	duration_minutes = int(row['Duration'].split(':')[1])
	duration_seconds = int(row['Duration'].split(':')[2])
	#Finding total duration of all shows on a given day
	if d in dct:
		duration_in_minutes = duration_hours * 60 + duration_minutes + int(duration_seconds/60)
		dct[d] = dct[d] + duration_in_minutes
		#Finding start and end times for all shows (for binge visualization)
		start_time = datetime.datetime.fromisoformat(row['Start Time']) 
		#5 minutes added to duration to allow for time between shows during a binge
		end_time = start_time + datetime.timedelta(hours=duration_hours, minutes=(duration_minutes + 5), seconds=duration_seconds)
		all_shows_watched.append([start_time, end_time, duration_in_minutes])

#Sorting start and end times for all shows
all_shows_watched.sort(key=lambda x: x[0])

#Dictionary of start date of each week
weeks = [[str(dates[x]).split(' ')[0]] for x in range(0,len(dates),7)]
just_weeks = [str(dates[x]).split(' ')[0] for x in range(0,len(dates),7)]

#Trackers to check if a show was watched in a certain week
week_tracker_start = datetime.datetime.fromisoformat(start) 
week_tracker_end = week_tracker_start + datetime.timedelta(weeks=1)

#Loop to find length of every binge session in a given week
curr_binge = all_shows_watched[0][2]
for s in range(len(all_shows_watched)-1):
	if all_shows_watched[s][0] >= week_tracker_start and all_shows_watched[s][1] < week_tracker_end:
		if all_shows_watched[s][1] > all_shows_watched[s+1][0]:
			curr_binge = curr_binge + all_shows_watched[s+1][2]
		else:
			for d in weeks:
				this_week = str(week_tracker_start)[:10]
				if this_week == d[0]:
					d.append(curr_binge)
			curr_binge = all_shows_watched[s+1][2]
	else:
		week_tracker_start = week_tracker_end
		week_tracker_end = week_tracker_end + datetime.timedelta(weeks=1)	
		curr_binge = all_shows_watched[s+1][2]	

#Setting up main visualization
visualizer = np.zeros((52, 7, 3), dtype=np.uint8)

col = 0
row = 0
for i in dct:
	#Assigning pixel values based on amout of tv watched
	if row <= 51:
		if dct[i] > 300:
			visualizer[row][col] = [75,0,0]
		elif dct[i] > 200:
			visualizer[row][col] = [125,0,0]
		elif dct[i] > 90:
			visualizer[row][col] = [175,0,0]
		elif dct[i] > 60:
			visualizer[row][col] = [220,0,0] 
		elif dct[i] > 30:
			visualizer[row][col] = [255,0,0]
		else:
			visualizer[row][col] = [255,255,255]

		col = col + 1

		if col >= 7:
			col = 0
			row = row + 1

#Saving visualization	
visualizer = visualizer.repeat(24, axis=0).repeat(24, axis=1)
img = Image.fromarray(np.array(visualizer), 'RGB')
img = img.rotate(90, Image.NEAREST, expand = 1)
img.save('binge.png')

#Setting up binge visualization
counter = 0
for weeknum in just_weeks:

	counter = counter + 1

	weeknum_datetime = datetime.datetime.fromisoformat(weeknum)
	next_weeknum_datetime = weeknum_datetime + datetime.timedelta(weeks=1)

	for w in weeks:
		if weeknum in w:
			if len(w[1:]) > 0:
				if len(w[1:]) >= 5:
					binges = sorted(w[1:])[-5:]
					objects = ('Binge 5', 'Binge 4', 'Binge 3', 'Binge 2', 'Binge 1')
				else:
					binges = sorted(w[1:])[-len(binges):]
					objects = ('Binge 5', 'Binge 4', 'Binge 3', 'Binge 2', 'Binge 1')[-len(binges):]

				#Creating binge bar graph
				y_pos = np.arange(len(objects))
				plt.bar(objects, binges, align='center', alpha=0.5)
				plt.xticks(y_pos, objects)
				plt.ylabel('Binge length (minutes)')
				plt.title('Longest Binges During Week of {}'.format(weeknum))
				plt.savefig('./binge_figures/bar{}.png'.format(counter))
				plt.close()
			else:
				white_image = np.zeros([480, 640, 3],dtype=np.uint8)
				white_image.fill(255)
				image = Image.fromarray(white_image, 'RGB')
				image.save('./binge_figures/bar{}.png'.format(counter))

	#Pie chart of time spent on Netflix vs. off Netflix for fun
	on_net = 0
	for i in dct:
		if datetime.datetime.fromisoformat(i) >= weeknum_datetime and datetime.datetime.fromisoformat(i) < next_weeknum_datetime:
			on_net = on_net + dct[i]
	not_on_net = 10080 - on_net
	piey = np.array([on_net, not_on_net])
	mylabels = ["Minutes on Netflix", "Minutes not on Netflix"]
	mycolors = ["Red", "Blue"]

	def absolute_value(val):
	    a  = np.round(val/100.*piey.sum(), 0)
	    return a

	plt.pie(piey, labels = mylabels, autopct=absolute_value, colors = mycolors)
	plt.savefig('./binge_figures/pie{}.png'.format(counter))
	plt.close()
