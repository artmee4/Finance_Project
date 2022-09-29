import pandas as pd
import expenses
from categories import Categories


ExpensesInMounth = expenses.get_all_statistics_per_month()
Dict_AllExpenses = expenses.get_all_AllExpenses()

categories = Categories().get_all_categories()
categories = ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
listofcategories = categories.split('\n*')
listofcategories = [s.replace(')', '') for s in listofcategories]

Dict_Categories = {}
for i in range(len(listofcategories)):
    af = listofcategories[i].split('(')
    Dict_Categories[af[0]] = af[1]

print(Dict_Categories.keys())
print(Dict_AllExpenses.keys())
print(ExpensesInMounth)




# for i in range(len(listofcategories)):
#     az = listofcategories[i].split('(')




# listnames = []
# listaliases = []
# az = []



#ListRecomend = [", ".join(c.aliases) for c in categories]

