from PIL import Image, ImageDraw, ImageFont

import textwrap

from datetime import date

import sys
import os

from workalendar.asia import Singapore
import calendar

year = input("Year?")

year = int(year)

cal = Singapore()

try:
	public_holidays = cal.holidays(year)
except Exception:
	sys.exit("Error getting calendar for year " + str(year) + ".")

os.mkdir("calendars/"+str(year))

c = calendar.Calendar(firstweekday=6)

arial_black = os.getcwd()+"/assets/arial-black.ttf"
mfont = ImageFont.truetype(arial_black, 75)
yfont = ImageFont.truetype(arial_black, 40)
dfont = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', 16)

smfont =  ImageFont.truetype(arial_black, 15)
sdfont = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', 10)

box_size = {'x':129,'y':93}

month_images = []

width, height = int(8.27 * 72), int(11.7 * 72) # A4 at 300dpi

on_holiday = 0

for i in range(1,13):

	cal_image = Image.open(os.getcwd()+'/assets/calformat.png')
	drawn = ImageDraw.Draw(cal_image)

	drawn.text((28, -5), calendar.month_name[i].upper(), (255,30,30), font=mfont)
	drawn.text((812, 0), str(year), (255,30,30), font=yfont)

	x = 29
	y = 127
	last_blank_dates = False
	for j in c.itermonthdays2(year, i):
		if j[0] == 0 and not last_blank_dates:
			drawn.rectangle([x+1,y+1,x+box_size['x']-2,y+box_size['y']-2],(230,230,230))
		elif j[0] != 0:
			drawn.rectangle([x+1,y+1,x+box_size['x']-2,y+box_size['y']-2],(242,242,242))
			if public_holidays[on_holiday][0] == date(year, i, j[0]):
				drawn.text((x+7,y+5), str(j[0]), (255,30,30), font=dfont)
				lines = textwrap.wrap(public_holidays[on_holiday][1], width=25)
				y_text = y+20
				for line in lines:
					wid, hei = sdfont.getsize(line)
					drawn.text((x+7, y_text), line, (255,30,30), font=sdfont)
					y_text += hei
				if on_holiday < len(public_holidays)-1:
					on_holiday += 1
			elif j[1] == 6 or j[1] == 5:
				drawn.text((x+7,y+5), str(j[0]), (255,30,30), font=dfont)
			else:
				drawn.text((x+7,y+5), str(j[0]), (77,77,77), font=dfont)

		x += box_size['x']
		if x > 900:
			x = 29
			if y > 450:
				y = 127
				last_blank_dates = True
			else:
				y += box_size['y']

	if i == 1:
		y1 = year - 1
		m1 = 12
	else:
		y1 = year
		m1 = i - 1

	if i == 12:
		y2 = year + 1
		m2 = 1
	else:
		y2 = year
		m2 = i + 1

	skip = (36,14)

	y_pos = 595
	
	start_x = 419
	txt = calendar.month_name[m1] + " " + str(y1)
	drawn.text((528-5*len(txt), y_pos), txt, (0,0,0), font=smfont)
	x = start_x
	y = 635
	for j in c.itermonthdays2(y1, m1):
		if j[0] != 0:
			if j[1] == 6 or j[1] == 5:
				drawn.text((x-len(str(j[0]))*5,y), str(j[0]), (255,30,30), font=sdfont)
			else:
				drawn.text((x-len(str(j[0]))*5,y), str(j[0]), (77,77,77), font=sdfont)

		x += skip[0]
		if x > 640:
			x = start_x
			y += skip[1]

	start_x = 699
	txt = calendar.month_name[m2] + " " + str(y2)
	drawn.text((804 - 5*len(txt), y_pos), txt, (0,0,0), font=smfont)
	x = start_x
	y = 635
	for j in c.itermonthdays2(y2, m2):
		if j[0] != 0:
			if j[1] == 6 or j[1] == 5:
				drawn.text((x-len(str(j[0]))*5,y), str(j[0]), (255,30,30), font=sdfont)
			else:
				drawn.text((x-len(str(j[0]))*5,y), str(j[0]), (77,77,77), font=sdfont)

		x += skip[0]
		if x > 920:
			x = start_x
			y += skip[1]

	cal_image = cal_image.resize((780,585),Image.ANTIALIAS)
	month_images.append(cal_image)
		
	cal_image.save(os.getcwd()+'/calendars/'+str(year)+'/'+calendar.month_abbr[i]+'.png')
'''
for i in range(12):
	page = Image.new('RGB', (height, width), 'white')
	page.paste(month_images[i],box=(10,10))

	page.save('to print/'+calendar.month_abbr[i+1]+str(year)+'.png')
'''













