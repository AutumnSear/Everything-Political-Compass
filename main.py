import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.axhline(0, color="black", linewidth=1)
ax.axvline(0, color="black", linewidth=1)
ax.plot(-0.5, 0.4, "ro", markersize=10, label="Point (-0.5, 0.4)")
ax.set_xlabel("Left - Right")
ax.set_ylabel("Lib - Auth")
ax.set_title("Political Compass")
ax.grid(True, linestyle="--", alpha=0.6)
ax.legend()
plt.show()
