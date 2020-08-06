"""plotting widget"""
from itertools import cycle
import pyqtgraph as pg
from abf_explorer.abf_logging import make_logger

pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

# each thing plotted needs to be a distinct plotdataitem added to the plotitem
# https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotdataitem.html
# https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/plotitem.html

logger = make_logger(__name__)


class PlotWidget(pg.GraphicsWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.color_list = [
            "#e41a1cff",
            "#377eb8ff",
            "#4daf4aff",
            "#984ea3ff",
            "#ff7f00ff",
            "#ffff33ff",
            "#a65628ff",
            "#f781bfff",
            "#999999ff",
        ]
        self.linear_region = None
        self.data = None
        self.color_cycler = cycle(self.color_list.copy())
        self.pen_width = 2
        self.set_main_canvas()
        self.var_linear_region_x_bounds = [None, None]

    def print_clicked(self, *args):
        logger.debug("Clicked")
        logger.debug(f"args: {[arg for arg in args]}")

    def _clear_legend(self):
        logger.debug("called")
        for sample, label in self.main_plot_widget.legend.items:
            self.main_plot_widget.legend.layout.removeItem(sample)
            self.main_plot_widget.legend.layout.removeItem(label)
        self.main_plot_widget.legend.items = []
        self.main_plot_widget.legend.updateSize()

    def _clear_plot_items(self):
        logger.debug("clearing items from plot")
        while self.main_plot_widget.items:
            self.main_plot_widget.removeItem(self.main_plot_widget.items[0])

    def set_main_canvas(self):
        self.main_plot_widget = self.addPlot(title="")
        self.main_plot_widget.addLegend()

    def update_plot(self, plotdict):
        self.main_plot_widget.legend.update()
        logger.debug(f"called. legend items are {self.main_plot_widget.legend.items}")
        self.data = pg.PlotDataItem(
            plotdict["x"],
            plotdict["y"],
            name=plotdict["name"],
            pen=pg.mkPen(self.color_cycler.__next__(), width=1,),
        )

        self.data.sigClicked.connect(self.print_clicked)
        self.main_plot_widget.addItem(self.data)
        self.main_plot_widget.setLabels(
            left=plotdict["y_units"], bottom=plotdict["x_units"]
        )

    def make_linear_region(self, bounds):
        self.linear_region = pg.LinearRegionItem(bounds, movable=True, swapMode="block")
        self.main_plot_widget.addItem(self.linear_region)
        self.linear_region.sigRegionChangeFinished.connect(
            self._emit_linear_region_x_bounds
        )
        self.var_linear_region_x_bounds = self._emit_linear_region_x_bounds()
        logger.debug(f"adding linear region with bounds {bounds}")

    def _emit_linear_region_x_bounds(self):
        logger.debug(
            f"linear region signal called, data bounds: {self.linear_region.dataBounds(axis=0)}"
        )
        self.var_linear_region_x_bounds = self.linear_region.dataBounds(axis=0)

    def reset_linear_region(self, bounds):
        logger.debug(f"resetting region to {bounds}")
        self.linear_region.setRegion(bounds)
        self.var_linear_region_x_bounds = self._emit_linear_region_x_bounds()

    def clear_plot(self, *args):
        logger.debug("called")
        self._clear_plot_items()
        logger.debug(f"main_plot items: {[i for i in self.main_plot_widget.items]}")
        self.linear_region = None
        self.data = None
        self.var_linear_region_x_bounds = [None, None]
        self._clear_legend()
        self.main_plot_widget.clearPlots()
        self.main_plot_widget.legend.update()
        self.main_plot_widget.setLabels(left="", bottom="")
        self.color_cycler = cycle(self.color_list.copy())
