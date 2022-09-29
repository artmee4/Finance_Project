import expenses
from categories import Categories
from itertools import islice


ExpensesInMounth = expenses.get_all_statistics_per_month_notstring()
Dict_AllExpenses = expenses.get_all_AllExpenses()

categories = Categories().get_all_categories()
categories = ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
listofcategories = categories.split('\n*')
listofcategories = [s.replace(')', '') for s in listofcategories]

Dict_Categories = {}
for i in range(len(listofcategories)):
    af = listofcategories[i].split('(')
    Dict_Categories[af[0]] = af[1]

Dict_Categories = {x.replace(' ', ''): v
     for x, v in Dict_Categories.items()}

#print(Dict_Categories)



AllExpensesForRec = Dict_AllExpenses.copy()
Dict_CategoriesForRec = Dict_Categories.copy()
del AllExpensesForRec['квартира']
del Dict_CategoriesForRec['квартира']


dictforrec = {}

ExpensesInMounth = dict(sorted(ExpensesInMounth.items(), key=lambda item: item[1]))
AllExpensesForRec = dict(sorted(AllExpensesForRec.items(), key=lambda item: item[1]))

#first2pairs = {k: ExpensesInMounth[k] for k in list(ExpensesInMounth)[:2]}
first2pairs = {k: AllExpensesForRec[k] for k in list(AllExpensesForRec)[:2]}

print(ExpensesInMounth)
print(AllExpensesForRec)
print(Dict_CategoriesForRec.keys())

# new_list = list(first2pairs.keys())
new_list = []
for cat in list(Dict_CategoriesForRec.keys()):
    if cat not in list(ExpensesInMounth.keys()):
        new_list.append(cat)



print(new_list)

new_list2 = []

for cat in new_list:
    if cat not in list(AllExpensesForRec.keys()):
        new_list2.append(cat)

print(new_list2)

[new_list2.append(x) for x in list(first2pairs.keys())]


print('kyky', new_list2[0:3])
