import numpy as np
import cv2

class Fig:
    def __init__(
            self, width=320, height=240, 
            margin=20, 
            padding=20, 
            axis=True, axis_color=(64, 64, 64), 
            color_channels=3, window_name='fig') -> None:
        self.width = width
        self.height = height
        self.margin = margin
        self.padding = padding
        self.axis = axis
        self.axis_color = axis_color
        self.color_channels = color_channels
        self.window_name = window_name
        self.clean()

    def clean(self) -> None:
        self.canvas = np.zeros((self.height, self.width, self.color_channels), dtype=np.uint8)
        self.range_set_x = False
        self.range_set_y = False
        self.plotted = False

    def plot(self, x: np.array, y: np.array, color=(255, 0, 0), thickness=1) -> None:
        _y = y * -1
        
        if self.plotted:
            self._plotter(x, _y, color=color, thickness=thickness)
            return
        
        self._recalc_transform(x, _y)

        if self.axis:
            self._draw_axis()
        
        self._plotter(x, _y, color=color, thickness=thickness)
        self.plotted = True
    
    def scatter(self, x: np.array, y: np.array, color=(255, 0, 0), radius=0) -> None:
        _y = y * -1
        
        if self.plotted:
            self._scatterer(x, _y, color=color, radius=radius)
            return
        
        self._recalc_transform(x, _y)

        if self.axis:
            self._draw_axis()
        
        self._scatterer(x, _y, color=color, radius=radius)
        self.plotted = True

    def set_range(self, range_x: tuple, range_y: tuple) -> None:
        if range_x:
            self.minimum_x = min(range_x)
            self.maximum_x = max(range_x)
            self.range_x = self.maximum_x - self.minimum_x
            self.range_set_x = True
        if range_y:
            self.minimum_y = -max(range_y)
            self.maximum_y = -min(range_y)
            self.range_y = self.maximum_y - self.minimum_y
            self.range_set_y = True

    def _recalc_transform(self, x: np.array, y: np.array) -> None:
        if not self.range_set_x:
            self.set_range((np.min(x), np.max(x)), None)
        if not self.range_set_y:
            self.set_range(None, (-np.min(y), -np.max(y)))
        self.scale_x = (self.width - self.margin * 2) / self.range_x
        self.scale_y = (self.height - self.margin * 2) / self.range_y
        self.shift_x, self.shift_y = self.minimum_x, self.minimum_y
    
    def _draw_axis(self) -> None:
        vertical_origin = round(-self.shift_y * self.scale_y)
        horizontal_origin = round(-self.shift_x * self.scale_x)
        cv2.line(self.canvas, 
                 (0, self.margin + vertical_origin), 
                 (self.width, self.margin + vertical_origin), 
                 color=self.axis_color, thickness=1)
        cv2.line(self.canvas, 
                 (self.margin + horizontal_origin, 0), 
                 (self.margin + horizontal_origin, self.height), 
                 color=self.axis_color, thickness=1)
        pass
    
    def _plotter(self, x: np.array, y: np.array, color=(255, 0, 0), thickness=1) -> None:
        color = (color[2], color[1], color[0])

        _x = np.round((x.copy() - self.shift_x) * self.scale_x + self.margin).astype(int)
        _y = np.round((y - self.shift_y) * self.scale_y + self.margin).astype(int)

        previous = np.array([_x[0], _y[0]])
        for next in zip(_x[1:], _y[1:]):
            next = np.array(next)
            cv2.line(self.canvas, previous, next, color=color, thickness=thickness)
            previous = next

    def _scatterer(self, x: np.array, y: np.array, color=(255, 0, 0), radius=1) -> None:
        color = (color[2], color[1], color[0])

        _x = np.round((x.copy() - self.shift_x) * self.scale_x + self.margin).astype(int)
        _y = np.round((y - self.shift_y) * self.scale_y + self.margin).astype(int)

        for next in zip(_x, _y):
            next = np.array(next)
            cv2.circle(self.canvas, next, radius=radius, color=color, thickness=cv2.FILLED)
    
    def _prepare_display_canvas(self):
        if self.padding == 0:
            self.display_canvas = self.canvas
            return
        
        self.display_canvas = np.zeros((self.padding * 2 + self.height, 
                                        self.padding * 2 + self.width, 
                                        self.color_channels), dtype=np.uint8)
        
        cv2.rectangle(self.display_canvas, 
                      (self.padding - 1, self.padding - 1), 
                      (self.padding + self.width + 1, self.padding + self.height + 1), 
                      color=self.axis_color, 
                      thickness=cv2.FILLED)

        self.display_canvas[self.padding: self.padding + self.height, self.padding: self.padding + self.width, :] = self.canvas

    def show(self) -> None:
        self._prepare_display_canvas()
        cv2.imshow(self.window_name, self.display_canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def save(self, path: str):
        self._prepare_display_canvas()
        cv2.imwrite(path, self.display_canvas)

# test code
if __name__ == '__main__':
    save_path = './plot.png'

    # create plot instance
    # you can pass additional parameters for customization
    # X goes left to right, Y goes bottom to top
    plt = Fig()

    # set display range (if not set or given None, range will be calculated automatically)
    # this will not override the margin
    plt.set_range((-10, 15), None)

    x = np.arange(-10, 15, 0.1)
    x_sparse = np.arange(-10, 15, 2)
    
    # plots
    plt.plot(x, (x - 2) * (x - 2) - 30, thickness=3)
    plt.plot(x, np.sin(x) * 15, color=(0, 255, 0))
    
    # plot with points
    plt.plot(x_sparse, x_sparse * 5 + 20, color=(255, 255, 0))
    plt.scatter(x_sparse, x_sparse * 5 + 20, color=(255, 255, 0), radius=3)
    
    # scatter
    plt.scatter(x, np.array([np.random.random() - 0.5 for _ in x]) * 300, color=(0, 255, 255))
    
    plt.show()
    plt.save(save_path)
    print(f'plot saved to {save_path}')