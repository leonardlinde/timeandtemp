# Write a google spreadsheet
# Adapted from Adafruity DHT Driver

import gspread
import datetime

# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email       = 'llinde@gmail.com'
password    = 'qhwgapsdkgocfhop'
spreadsheet = 'TempHumidityandLight'

def addData(now, temp, humidity, light):

  try:
    gc = gspread.login('llinde@gmail.com' , 'qhwgapsdkgocfhop')
  except:
    print "Error logging in to Google"
    return False

  # Open a worksheet from your spreadsheet using the filename
  try:
    worksheet = gc.open(spreadsheet).sheet1
  except:
    print "Error opening sheet "+sheet
    return False

  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [now, temp, humidity, light]
    worksheet.append_row(values)
  except:
    print "Error appending row"
    return False

  return True
