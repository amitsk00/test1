import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import seaborn

list1 = ["Country", "SummerGames", "SummerGold",
         "SummerSilver", "SummerBronze", "SummerTotal"]
list2 = ["WinterGames", "WinterGold",
         "WinterSilver", "WinterBronze", "WinterTotal"]
list3 = ["TotalGames", "TotalGold",
         "TotalSilver", "TotalBronze", "GrandTotal"]

my_colz = list1 + list2 + list3

file = pd.read_csv("olympics.csv", skiprows=1)
df = pd.DataFrame(file)
df.columns = my_colz

dfSummer = df[["Country", "SummerGames", "SummerGold",
               "SummerSilver", "SummerBronze", "SummerTotal"]]
dfWinter = df[["Country", "WinterGames", "WinterGold",
               "WinterSilver", "WinterBronze", "WinterTotal"]]
dfGrand = df[["Country", "TotalGames", "TotalGold",
              "TotalSilver", "TotalBronze", "GrandTotal"]]
dfTotal = df[["Country", "SummerTotal", "WinterTotal", "GrandTotal"]]

print(dfTotal["SummerTotal"])
mpl.xlabel("Country")
mpl.ylabel("Totals")
mpl.plot(dfTotal["Country"], dfTotal["SummerTotal"], label="Summer")
mpl.plot(dfTotal["Country"], dfTotal["WinterTotal"], label="Winter")
mpl.legend()
mpl.show()
