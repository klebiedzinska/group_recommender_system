from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

from yellowbrick.cluster import KElbowVisualizer

class myKElbowVisualizer(KElbowVisualizer):
    def finalize(self):
        """
        Prepare the figure for rendering by setting the title as well as the
        X and Y axis labels and adding the legend.

        """
        # Get the metric name
        metric = self.scoring_metric.__name__.replace("_", " ").title()

        # Set the title
        self.set_title("Wartość odchylenia wewnątrzklastrowego klastrowania k-średnich")

        # Set the x and y labels
        self.ax.set_xlabel("liczba klastrów")
        self.ax.set_ylabel("odchylenie wewnątrzklastrowe")

        # set the legend if locate_elbow=True
        if self.locate_elbow is True and self.elbow_value_ is not None:
            self.ax.legend(loc="best", fontsize="medium", frameon=True)

        # Set the second y axis labels
        if self.timings:
            self.axes[1].grid(False)
            self.axes[1].set_ylabel("fit time (seconds)", color=self.timing_color)
            self.axes[1].tick_params("y", colors=self.timing_color)

    def draw(self):
        """
        Draw the elbow curve for the specified scores and values of K.
        """
        # Plot the silhouette score against k
        self.ax.plot(self.k_values_, self.k_scores_, marker="D", c=self.metric_color)
        if self.locate_elbow is True and self.elbow_value_ is not None:
            elbow_label = "łokieć w $k={}$, $wartość={:0.3f}$".format(
                self.elbow_value_, self.elbow_score_
            )
            self.ax.axvline(
                self.elbow_value_, c=self.vline_color, linestyle="--", label=elbow_label
            )

        # If we're going to plot the timings, create a twinx axis
        if self.timings:
            self.axes = [self.ax, self.ax.twinx()]
            self.axes[1].plot(
                self.k_values_,
                self.k_timers_,
                label="fit time",
                c=self.timing_color,
                marker="o",
                linestyle="--",
                alpha=0.75,
            )

        return self.ax   

X, y = make_blobs(n_samples=1000, n_features=12, centers=8, random_state=42)


model = KMeans()
visualizer = myKElbowVisualizer(model, k=(4,12), timings=False)


visualizer.fit(X)        
visualizer.show()        