"""Optional Matplotlib plots; import this module only when plotting is requested."""
def plot_trajectory(result,show=True,save_path=None):
    try: import matplotlib.pyplot as plt
    except ImportError as exc: raise RuntimeError("Install the plot extra: pip install .[plot]") from exc
    fig,ax=plt.subplots()
    ax.plot(result.downrange/1000.,result.altitudes/1000.,label="Ascent")
    ax.set_xlabel("Downrange distance (km)"); ax.set_ylabel("Altitude (km)")
    ax.set_title(result.config.vehicle.name); ax.grid(True); ax.legend()
    if save_path: fig.savefig(save_path,dpi=160,bbox_inches="tight")
    if show: plt.show()
    return fig,ax
def plot_time_history(result,show=True,save_path=None):
    try: import matplotlib.pyplot as plt
    except ImportError as exc: raise RuntimeError("Install the plot extra: pip install .[plot]") from exc
    fig,axes=plt.subplots(3,1,sharex=True,figsize=(9,8))
    axes[0].plot(result.times,result.altitudes/1000.); axes[0].set_ylabel("Altitude (km)")
    axes[1].plot(result.times,result.speeds); axes[1].set_ylabel("Speed (m/s)")
    axes[2].plot(result.times,[s.dynamic_pressure/1000. for s in result.samples]); axes[2].set_ylabel("Dynamic pressure (kPa)")
    axes[2].set_xlabel("Time (s)")
    for ax in axes: ax.grid(True)
    fig.tight_layout()
    if save_path: fig.savefig(save_path,dpi=160,bbox_inches="tight")
    if show: plt.show()
    return fig,axes
