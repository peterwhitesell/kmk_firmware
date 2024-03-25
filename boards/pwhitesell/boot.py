from kmk.bootcfg import bootcfg
import board

bootcfg(
    sense=board.D8, # column
    source=board.A3,  # row
    storage=False,
    # cdc=False,
    # pan=True,
)