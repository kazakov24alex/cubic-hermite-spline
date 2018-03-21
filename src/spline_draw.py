
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys
sys.path.append(".")
from spline_math import get_free_spline, get_hermite_spline

# GRAPH PROPERTY
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_axisbelow(True)
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
      ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), shadow=True, ncol=2)

fig.canvas.mpl_connect('key_press_event', key_event)



def draw_free_spline(points):
    # source = [[4.,0.],[0.,3.],[0.,0.]]
    x_polynomes_arr, y_polynomes_arr = get_free_spline(points_arr[1:len(points_arr)-1])

    plt.plot(x_polynomes_arr[0], y_polynomes_arr[0], color='blue', lw=2, label="Free Spline")
    for i in range(1, len(x_polynomes_arr)):
        plt.plot(x_polynomes_arr[i], y_polynomes_arr[i], color='blue', lw=2)
        fig.canvas.draw_idle()


def draw_hermite_spline(points):
    x_polynomes_arr, y_polynomes_arr = get_hermite_spline(points_arr[1:len(points_arr)-1], [1.5,1.5],[-2.,1.])#points_arr[0], points_arr[len(points_arr)-1])

    style = "Simple,tail_width=0.5,head_width=4,head_length=8"
    kw = dict(arrowstyle=style, color="k", lw=2)
    arrow1 = patches.FancyArrowPatch(points_arr[1], points_arr[0], **kw)
    arrow2 = patches.FancyArrowPatch(points_arr[len(points_arr) - 2], points_arr[len(points_arr) - 1], **kw)

    plt.gca().add_patch(arrow1)
    plt.gca().add_patch(arrow2)

    plt.plot(x_polynomes_arr[0], y_polynomes_arr[0], color='orange', lw=2, label="Hermite Spline")
    for i in range(1, len(x_polynomes_arr)):
        plt.plot(x_polynomes_arr[i], y_polynomes_arr[i], color='orange', lw=2)
    fig.canvas.draw_idle()

plt.show()



