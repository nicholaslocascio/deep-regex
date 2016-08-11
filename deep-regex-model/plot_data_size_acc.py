import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
np.random.seed(sum(map(ord, "aesthetics")))
# sns.set_style("white")

x = [650, 1625, 3250, 4875, 6500]
y = [38.04, 50.28, 54.76, 56.72, 61.20]
y2 = [20.92, 31.08, 35.70, 40.16, 41.76]

plt.plot(x, y, marker='o', markersize=12, linewidth=4)
plt.plot(x, y2, marker='o', markersize=12, linewidth=4)
plt.xlabel('Number of Training Examples', fontsize=24)
plt.ylabel('Model Accuracy (%)', fontsize=26)
plt.title('DeepRegex Performance vs. Data Size', fontsize=32)
plt.legend(['DFA-Equal', 'String-Equal'], loc='upper left')

leg = plt.gca().get_legend()
ltext  = leg.get_texts()
plt.setp(ltext, fontsize=18) 

plt.tick_params(labelsize=16)
plt.tick_params(labelsize=16)
plt.show()