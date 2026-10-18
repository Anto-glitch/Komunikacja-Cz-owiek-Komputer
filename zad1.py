import numpy as np
import matplotlib.pyplot as plt

def average(table):
    new_table = []
    for i in table:
        avg = np.mean(i[2::])*100
        new_table.append([i[0], i[1]/1000, avg])
    return np.array(new_table)

def table_display(table):
    for row in table:
        print(
            f"generation={int(row[0])}, "
            f"effort={int(row[1])}, "
            f"average={np.mean(row[2::]):.4f}"
        )

def plot_table(subplot,table, title, marker,color):
    subplot.plot(table[:, 1], table[:, 2], label=title, marker=marker, markersize=6, markevery=25, color=color)


table = np.loadtxt("1c.csv", delimiter=",", skiprows=1)
boxplot_data1 = table[:, 2:].ravel() * 100
table = average(table)
#table_display(table)


table2 = np.loadtxt("1crs.csv", delimiter=",", skiprows=1)
boxplot_data2 = table2[:, 2:].ravel() * 100
table2 = average(table2)
#table_display(table2)

table3 = np.loadtxt("1ers.csv", delimiter=",", skiprows=1)
boxplot_data3 = table3[:, 2:].ravel() * 100
table3 = average(table3)
#table_display(table3)


table4 = np.loadtxt("2c.csv", delimiter=",", skiprows=1)
boxplot_data4 = table4[:, 2:].ravel() * 100
table4 = average(table4)
#table_display(table4)

table5 = np.loadtxt("2crs.csv", delimiter=",", skiprows=1)
boxplot_data5 = table5[:, 2:].ravel() * 100
table5 = average(table5)
#table_display(table5)

boxplot_data = [boxplot_data3, boxplot_data2, boxplot_data1, boxplot_data5, boxplot_data4]
display_labels = ["1-Evol-RS", "1-Coev-RS", "1-Coev", "2-Coev-RS", "2-Coev"]


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

plot_table(ax1, table3,"1-Evol-RS","o","blue")
plot_table(ax1, table2, "1-Coev-RS","^","green")
plot_table(ax1, table, "1-Coev","s", "black")
plot_table(ax1, table5,"2-Coev-RS","D","red")
plot_table(ax1, table4,"2-Coev","d","pink")


ax1.set_xlabel(r"Liczba rozegranych gier ($\times 1000$)")
ax1.set_xlim(0,500)
ax1.set_ylabel(r"Odsetek wygranych gier ($\%$)")
ax1.set_ylim(60, 100)
upperax = ax1.twiny()
upperax.set_xlabel(r"Pokolenie ($g$)")
upperax.set_xlim(0, 200)

ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(loc="lower right")

ax2.boxplot(
    boxplot_data,
    notch=True,
    widths=0.3,
    boxprops={"color": "blue"},
    whiskerprops={"color": "blue", "linestyle": "--"},
    medianprops={"color": "red", "linewidth": 2},
    meanprops={
        "marker": "o",
        "markerfacecolor": "black",
        "markeredgecolor": "blue",
        "markersize": 6,
    },
    showmeans=True,
    showfliers=False,
)
ax2.set_xticklabels(display_labels)
ax2.grid(True,linestyle='--', alpha=0.3)
ax2.set_ylim(60, 100)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")


fig.tight_layout()
fig.savefig('myplot.pdf')
plt.show()
plt.close()
