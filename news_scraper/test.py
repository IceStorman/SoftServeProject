import clr
clr.AddReference("dlls/Custom_Selenium")
from Selenium_right_click import Driver

driver=Driver()

driver.OpenUrl("https://www.espn.com/fantasy/basketball/insider/story/_/id/42388491/fantasy-basketball-2024-25-nba-surprised-jalen-johnson-klay-thompson-buddy-hield")

driver.PerformRightClickByXpath("//div[@class='img-wrap']//img[@class='imageLoaded']")

driver.Quit()