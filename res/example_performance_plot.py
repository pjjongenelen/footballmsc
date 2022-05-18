"""
Small experiment with SA for player performance analysis. 
Will generate a graph for 'Antony' during Ajax - PSV. 
His grades were: 7.5 (AD), 8.0 (VI), and 8.4 (FotMob), so an 8.0 on average. 
Now let's see what twitter says
"""
#%%
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

# metadata
# start_time = "2021-10-24 14:45"
# half_time = "2021-10-24 15:30"
# half_time_end = "2021-10-24 15:45"
# goal_antony = "2021-10-24 16:06"
# end_time = "2021-10-24 16:30"

#%%
# hand-coded fifteen-minute interval scores for Anotony during Ajax-PSV on October 24, 2021
minutes =       np.array([0,  15,    30,  45,    60,  75,    90])
antony_scores = np.array([0,  -0.3,  0,   -0.3,  1,   0.36,  0.27])
num_tweets =    np.array([0,  1,     0,   2,     1,   12,    7])

# make smoothed score
score_smooth = gaussian_filter1d(antony_scores, sigma=0.5)

# create figure
fig, ax = plt.subplots()

# plot raw and smooth sentiment score
ax.plot(minutes, score_smooth, color='crimson')
ax.plot(minutes, antony_scores, color='lightsalmon')
ax.set_ylabel('Sentiment Score', color='crimson')
ax.set_ylim(-1.1, 1.1)

# plot number of tweets
ax2 = ax.twinx()
ax2.plot(minutes, num_tweets, color='lightgrey')
ax2.set_ylabel('Number of tweets', color='grey')

# add vertical lines at key moments
plt.axvline(75, lw=0.5, color="green")  # goal

# draw plot
ax.set_xlabel('Playing time, interval = 15 min')
plt.xticks(minutes)
plt.title('Performance of Antony during #ajapsv according to Twitter sentiment')
plt.show()