import pyqtgraph as pg

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.mainPlot = self.addPlot(title="")

    def update_plot(self, plotdict):
        self.mainPlot.plot(plotdict["x"], plotdict["y"], name=plotdict["name"])
        self.mainPlot.setTitle(plotdict["name"])
        # self.mainPlot.addLegend()
        print("Plotting called")

    def clear_plot(self, e=None):
        self.mainPlot.clear()
        self.mainPlot.setTitle("")
        print(f"cleared plot")
