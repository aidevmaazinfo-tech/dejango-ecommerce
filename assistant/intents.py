from enum import StrEnum


class Intent(StrEnum):
    OPEN_CART = "open_cart"

    ADD_TO_CART = "add_to_cart"

    REMOVE_FROM_CART = "remove_from_cart"

    CLEAR_CART = "clear_cart"

    UPDATE_CART = "update_cart"

    PRODUCT_SEARCH = "product_search"

    PRODUCT_DETAILS = "product_details"

    ORDER_LIST = "order_list"

    ORDER_TRACK = "track_order"

    ORDER_SPECIFIC = "specific_order"

    ORDER_CANCEL = "cancel_order"

    ORDER_DELIVERY = "order_delivery"

    UNKNOWN = "unknown"
