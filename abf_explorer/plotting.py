import pyqtgraph as pg
from itertools import cycle
from pprint import pprint

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
            "A6CEE3ff",
            "1f78b4ff",
            "b2df8aff",
            "33a02cff",
            "fb9a99ff",
            "e31a1cff",
            "fdbf6fff",
            "ff7f00ff",
            "cab2d6ff",
        ]
        self.color_cycler = cycle(self.color_list.copy())
        self.pen_width = 2
        self.set_main_canvas()

    def print_clicked(self, *args):
        print("clicked!")
        print(f"args: {[arg for arg in args]}")

    def _clear_legend(self):
        print("test clear called")
        for sample, label in self.mainPlotWidget.legend.items:
            self.mainPlotWidget.legend.layout.removeItem(sample)
            self.mainPlotWidget.legend.layout.removeItem(label)
        self.mainPlotWidget.legend.items = []
        self.mainPlotWidget.legend.updateSize()

    def set_main_canvas(self):
        self.mainPlotWidget = self.addPlot(title="")
        self.mainPlotWidget.addLegend()

    def update_plot(self, plotdict):
        self.mainPlotWidget.legend.update()
        print(f"leg items {self.mainPlotWidget.legend.items}")
        self.data = pg.PlotDataItem(
            plotdict["x"],
            plotdict["y"],
            name=plotdict["name"],
            pen=pg.mkPen(self.color_cycler.__next__(), clickable=True,),
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
        # self._clear_all_legend()
        self._clear_legend()
        self.mainPlotWidget.clearPlots()
        self.mainPlotWidget.legend.update()
        self.mainPlotWidget.setLabels(left="", bottom="")
        self.color_cycler = cycle(self.color_list.copy())
        print(f"cleared plot")
