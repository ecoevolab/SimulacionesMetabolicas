import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk


# Create some dummy data for plotting (e.g., a bar chart)
categories = ['Category A', 'Category B']
values = [10, 15]

fig, ax = plt.subplots()

# Plot the bars (optional, but good for context)
ax.bar(categories, values, color=['skyblue', 'lightcoral'])

# Create custom patches with hatches for the legend
# Patch for 'Category A' with '/' hatch
patch_a = mpatches.Patch(facecolor='skyblue', hatch='/', label='Category A')
# Patch for 'Category B' with 'x' hatch (as an example of another pattern)
patch_b = mpatches.Patch(facecolor='lightcoral', hatch='x', label='Category B')

# Create the legend using the custom patches
ax.legend(handles=[patch_a, patch_b])

plt.title('Bar Chart with Hatched Legend')
plt.show()



root = tk.Tk()

# Create a label with red text
label = tk.Label(root, text="This text is red!", fg="red")
label.pack()

root.mainloop()