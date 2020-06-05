import pyqtgraph as pg
from itertools import cycle

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

# each thing plotted needs to be a distinct https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotdataitem.html plotdataitem, added to the plotitem https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html

class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.color_list = [
            "440154ff",
            "482878ff",
            "3e4989ff",
            "31688eff",
            "26828eff",
            "1f9e89ff",
            "35b779ff",
            "6ece58ff",
            "b5de2bff",
        ]
        self.color_cycler = cycle(self.color_list.copy())
        self.pen_width = 2
        self.set_main_canvas()

    def print_clicked(self, *args):
        print("clicked!")
        print(f"args: {[arg for arg in args]}")

    def set_main_canvas(self):
        self.mainPlotItem = self.addPlot(title="")

    def update_plot(self, plotdict):
        self.mainPlotWidget.plot(
            plotdict["x"],
            plotdict["y"],
            name=plotdict["name"],
            pen=pg.mkPen(self.color_cycler.__next__()),
        )
        self.mainPlotWidget.setLabels(
            left=plotdict["y_units"], bottom=plotdict["x_units"]
        )

#        self.item_refs append each item to item refs and attach the signal
        print("Plotting called")
        print(f"plot items are: {[(i.name(), type(i)) for i in self.mainPlotWidget.items]}")

    def clear_plot(self, *args):
        self.mainPlotWidget.clear()
        self.mainPlotWidget.setLabels(left="", bottom="")
        self.color_cycler = cycle(self.color_list.copy())
        print(f"cleared plot")
