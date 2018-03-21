import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(".")
from spline_math import get_free_spline, get_hermite_spline

# GRAPH PROPERTY
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xlim([-5,5])
plt.ylim([-5,5])
plt.title('Spline')
plt.grid(True)

global points_arr
points_arr = []

# POINT PICKER
def on_mouse_click(event):
    try:
        on_mouse_click.a = on_mouse_click.a + 1
    except AttributeError:
        on_mouse_click.a = 0

    global ix, iy
    ix, iy = event.xdata, event.ydata
    # print(ix, iy)
    points_arr.append([ix, iy])
    plt.plot(ix, iy, marker='o', color='r', ls='')
    ax.annotate('A' + str(on_mouse_click.a), xy=(ix, iy), xytext=(0, 5), textcoords='offset points')
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', on_mouse_click)


def key_event(e):
  try:
      key_event.a = key_event.a + 1
  except AttributeError:
      key_event.a = 0

  if (e.key == 'p'):
      print("draw")
      draw_free_spline(points_arr)
      draw_hermite_spline(points_arr)

fig.canvas.mpl_connect('key_press_event', key_event)



def draw_free_spline(points):
    # source = [[4.,0.],[0.,3.],[0.,0.]]
    x_polynomes_arr, y_polynomes_arr = get_free_spline(points_arr[1:len(points_arr)-1])

    for i in range(0, len(x_polynomes_arr)):
        plt.plot(x_polynomes_arr[i], y_polynomes_arr[i], color='blue')
        fig.canvas.draw_idle()


def draw_hermite_spline(points):
    x_polynomes_arr, y_polynomes_arr = get_hermite_spline(points_arr[1:len(points_arr)-1], [1.5,1.5],[-2.,1.])#points_arr[0], points_arr[len(points_arr)-1])

    for i in range(0, len(x_polynomes_arr)):
        plt.plot(x_polynomes_arr[i], y_polynomes_arr[i], color='orange')
        #plt.plot([vector1[0],points[0][0]],[vector1[1],points[0][1]], color='black')
        fig.canvas.draw_idle()

plt.show()



