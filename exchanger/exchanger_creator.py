from .stream import Flow
from .parts import Assembly
from .exchanger_types import ExchangerEqualCells


def auto_create_exchanger(flow_1: Flow = None, flow_2: Flow = None, assembly: Assembly = None):
    """
    Automatically create an instance of ExchangerEqualCells (with two Flows) based on the provided parameters.

    Args:
        flow_1 (Flow): The first flow for the exchanger.
        flow_2 (Flow): The second flow for the exchanger.
        assembly (Assembly): The assembly object containing all constructive parameters for the exchanger.

    Returns:
        ExchangerEqualCells: An instance of ExchangerEqualCells.

    Raises:
        ValueError: If the number of baffles and tube passes are both available.

    """
    flow_order_1, flow_order_2 = assembly.flow_orders

    baffles = assembly.baffles
    if baffles is NotImplemented:
        layout_cols = 1
    else:
        layout_cols = baffles.number_baffles + 1
    layout_rows = assembly.tube_passes

    if layout_cols == 2 and layout_rows == 1:
        raise ValueError("number of baffle and tube passes are available")

    layout_shape = layout_rows, layout_cols

    ex = ExchangerEqualCells(layout_shape, 'CrossFlowOneRow',
                             flow_1=flow_1, flow_order_1=flow_order_1,
                             flow_2=flow_2, flow_order_2=flow_order_2,
                             assembly=assembly)
    return ex
