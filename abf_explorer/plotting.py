import pyqtgraph as pg
from itertools import cycle

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

# each thing plotted needs to be a distinct https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotdataitem.html plotdataitem, added to the plotitem https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html
# TODO (tonight) implement the filtering checkbox and mean all sweeps checkbox and a plot all sweeps checkbox..
# TODO (saturday) implement the select region feature for analysis of field potentials.Allow manual region specification and save the data from the selected region for later automated analysis. Think of what data you need for each experiment (i.e. for IO, axon refract, and 83Hz)
#


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
        self.mainPlotWidget = self.addPlot(title="")

    def update_plot(self, plotdict):
        self.data = pg.PlotDataItem(
            plotdict["x"],
            plotdict["y"],
            name=plotdict["name"],
            pen=pg.mkPen(self.color_cycler.__next__(), clickable=True),
        )

        self.data.sigClicked.connect(self.print_clicked)
        self.mainPlotWidget.addItem(self.data)
        # self.proxy = pg.SignalProxy(self.mainPlotWidget.scene().sigMouseMoved, rateLimit=60,slot=self.print_clicked)
        self.mainPlotWidget.setLabels(
            left=plotdict["y_units"], bottom=plotdict["x_units"]
        )

        #        self.item_refs append each item to item refs and attach the signal
        print("Plotting called")
        print(
            f"plot items are: {[(i.name(), type(i)) for i in self.mainPlotWidget.items]}"
        )
        print(f"type {self.mainPlotWidget}")

    def clear_plot(self, *args):
        self.mainPlotWidget.clear()
        self.mainPlotWidget.setLabels(left="", bottom="")
        self.color_cycler = cycle(self.color_list.copy())
        print(f"cleared plot")
