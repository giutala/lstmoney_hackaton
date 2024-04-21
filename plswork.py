import streamlit as st
import json
import matplotlib.pyplot as plt
from helpers import query_spendsis,query_finbro

st.title("User case Demonstration")
st.divider()
st.subheader("User profile:")

###--- PRETTY PIE CHARTS
def calculate_by_category(transactions, keyname):
    by_category = {}
    for transaction in transactions:
        category = transaction[keyname]
        amount = int(transaction['amount'])
        if category in by_category:
            by_category[category] = by_category[category] + amount
        else:
            by_category[category] = amount
    return by_category

def display_data(data):
    for key, value in data.items():
        if isinstance(value, list):
            st.markdown(f"**{key.capitalize()}**:")
            with st.markdown(""):
                for item in value:
                    st.write("- " + str(item))
        else:
            st.markdown(f"**{key.capitalize()}**: {value}")

# File selection
f = open("./FinBro.Users.json")
data = json.load(f)
display_data(data)

# File selection for expenses
fexpenses = open("./FinBro.Expenses.json")
fexpenses_data = json.load(fexpenses)

finvest = open("./FinBro.Investment.json")
finvest_data = json.load(finvest)
# Calculate expenses by category
expenses_by_category = calculate_by_category(fexpenses_data['transactions'], 'category')
investments_by_category = calculate_by_category(finvest_data['investments'], 'bond')
# Create pie chart
labels_exp = expenses_by_category.keys()
sizes_exp = expenses_by_category.values()
labels_inv = investments_by_category.keys()
sizes_inv = investments_by_category.values()


fig_exp, ax_exp = plt.subplots()
ax_exp.pie(sizes_exp, labels=labels_exp, autopct='%1.1f%%', startangle=90)
ax_exp.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
my_circle_exp = plt.Circle((0, 0), 0.7, color='white')
p_exp = plt.gcf()
p_exp.gca().add_artist(my_circle_exp)

fig_inv, ax_inv = plt.subplots()
ax_inv.pie(sizes_inv, labels=labels_inv, autopct='%1.1f%%', startangle=90)
ax_inv.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
my_circle_inv = plt.Circle((0, 0), 0.7, color='white')
p_inv = plt.gcf()
p_inv.gca().add_artist(my_circle_inv)

###--- ML MAGIC
st.divider()
st.write("Let's test how good our Finbros really are.")
st.write("This pie chart displays Kathleen expences.")
st.write("We'll give our model the user profile and tis chart, see what they're capable of:")
st.pyplot(fig_exp)

if st.button('Interpret'):
    st.write(query_spendsis())
    
st.divider()

st.pyplot(fig_inv)

if st.button('Interpret this'):
    st.write(query_finbro())


