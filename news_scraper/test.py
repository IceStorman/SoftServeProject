import clr
import os
import sys

dll_path = os.path.join(os.path.dirname(__file__),"dlls")
sys.path.append(dll_path)
clr.AddReference("Custom_Selenium")


from Selenium_right_click import Driver
import pyperclip

driver=Driver()

driver.OpenUrl("https://www.espn.com/fantasy/basketball/insider/story/_/id/42388491/fantasy-basketball-2024-25-nba-surprised-jalen-johnson-klay-thompson-buddy-hield")

driver.PerformRightClickByXpath("//div[@class='img-wrap']//img[@class='imageLoaded']")

driver.Quit()

print(pyperclip.paste())