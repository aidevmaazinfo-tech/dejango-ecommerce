from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order

from .parser import parse_command
from .tools import ToolCall, execute_tool


# ============================================================
# ORDER PARSER TESTS
# ============================================================

class OrderParserTest(TestCase):

    def test_list_orders(self):
        result = parse_command("show my orders")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "list",
            },
        )

    def test_view_orders(self):
        result = parse_command("view orders")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "list",
            },
        )

    def test_track_order(self):
        result = parse_command("track order 123")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "track",
                "order_id": 123,
            },
        )

    def test_track_order_with_hash(self):
        result = parse_command("track order #123")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "track",
                "order_id": 123,
            },
        )

    def test_where_is_order(self):
        result = parse_command("where is order 123")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "track",
                "order_id": 123,
            },
        )

    def test_specific_order(self):
        result = parse_command("show order 123")

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "specific",
                "order_id": 123,
            },
        )

    def test_specific_order_details(self):
        result = parse_command(
            "order 123 details"
        )

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "specific",
                "order_id": 123,
            },
        )

    def test_cancel_order(self):
        result = parse_command(
            "cancel order 123"
        )

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "cancel",
                "cancel_order_id": 123,
            },
        )

    def test_cancel_order_with_hash(self):
        result = parse_command(
            "cancel order #123"
        )

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "cancel",
                "cancel_order_id": 123,
            },
        )

    def test_roman_urdu_track_order(self):
        result = parse_command(
            "order 123 kahan hai"
        )

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "track",
                "order_id": 123,
            },
        )

    def test_roman_urdu_cancel_order(self):
        result = parse_command(
            "order 123 ko cancel karo"
        )

        self.assertEqual(
            result.name,
            "get_user_orders_tool",
        )

        self.assertEqual(
            result.arguments,
            {
                "action": "cancel",
                "cancel_order_id": 123,
            },
        )


# ============================================================
# ORDER EXECUTION TESTS
# ============================================================

class OrderExecutionTest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="order-test-user",
            email="order-test@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            username="other-order-user",
            email="other-order@example.com",
            password="test-password",
        )

        self.order = Order.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            email="order-test@example.com",
            address="Test Address",
            postal_code="40100",
            city="Sargodha",
            total_price="50000.00",
            payment_status=Order.PaymentStatus.COMPLETED,
            order_status=Order.OrderStatus.PROCESSING,
        )

        self.other_order = Order.objects.create(
            user=self.other_user,
            first_name="Other",
            last_name="User",
            email="other-order@example.com",
            address="Other Address",
            postal_code="40100",
            city="Lahore",
            total_price="60000.00",
            payment_status=Order.PaymentStatus.COMPLETED,
            order_status=Order.OrderStatus.PROCESSING,
        )

    def test_list_orders(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "list",
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["action"],
            "list",
        )

        self.assertEqual(
            len(result["orders"]),
            1,
        )

        self.assertEqual(
            result["orders"][0]["id"],
            self.order.id,
        )

    def test_specific_order(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "specific",
                    "order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["action"],
            "specific",
        )

        self.assertEqual(
            result["order"]["id"],
            self.order.id,
        )

        self.assertEqual(
            result["order"]["status"],
            "PROCESSING",
        )

    def test_track_order(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "track",
                    "order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertTrue(
            result["success"]
        )

        self.assertEqual(
            result["action"],
            "track",
        )

        self.assertEqual(
            result["order"]["id"],
            self.order.id,
        )

    def test_cancel_order_requires_confirmation(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertTrue(
            result["success"]
        )

        self.assertTrue(
            result["confirmation_required"]
        )

        self.assertTrue(
            result["auto_open_cancel"]
        )

        self.assertEqual(
            result["order_id"],
            self.order.id,
        )

        self.assertEqual(
            result["redirect_url"],
            f"/orders/{self.order.id}/?cancel=1",
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.order_status,
            Order.OrderStatus.PROCESSING,
        )

    def test_other_users_order_is_not_accessible(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "specific",
                    "order_id": self.other_order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Order not found.",
        )

    def test_other_users_order_cannot_be_cancelled(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": self.other_order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Order not found.",
        )

        self.other_order.refresh_from_db()

        self.assertEqual(
            self.other_order.order_status,
            Order.OrderStatus.PROCESSING,
        )

    def test_cancelled_order_cannot_be_cancelled_again(self):
        self.order.order_status = (
            Order.OrderStatus.CANCELLED
        )

        self.order.save(
            update_fields=["order_status"]
        )

        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            f"Order #{self.order.id} is already cancelled.",
        )

    def test_shipped_order_cannot_be_cancelled(self):
        self.order.order_status = (
            Order.OrderStatus.SHIPPED
        )

        self.order.save(
            update_fields=["order_status"]
        )

        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertIn(
            "can no longer be cancelled",
            result["message"],
        )

    def test_delivered_order_cannot_be_cancelled(self):
        self.order.order_status = (
            Order.OrderStatus.DELIVERED
        )

        self.order.save(
            update_fields=["order_status"]
        )

        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                    "cancel_order_id": self.order.id,
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertIn(
            "can no longer be cancelled",
            result["message"],
        )

    def test_missing_order_id_for_specific_order(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "specific",
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Please provide an order ID.",
        )

    def test_missing_order_id_for_tracking(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "track",
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Please provide an order ID.",
        )

    def test_missing_order_id_for_cancel(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "cancel",
                },
            ),
            request=None,
            user=self.user,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Please provide an order ID to cancel.",
        )

    def test_unauthenticated_order_access(self):
        result = execute_tool(
            ToolCall(
                name="get_user_orders_tool",
                arguments={
                    "action": "list",
                },
            ),
            request=None,
            user=None,
        )

        self.assertFalse(
            result["success"]
        )

        self.assertEqual(
            result["message"],
            "Please log in to view your orders.",
        )


# ============================================================
# COMMAND API TESTS
# ============================================================

class CommandAPITest(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="command-api-user",
            email="command-api@example.com",
            password="test-password",
        )

        self.client.force_login(
            self.user
        )

    # --------------------------------------------------------
    # POST
    # --------------------------------------------------------

    def test_post_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": "show my orders",
            },
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["status"],
            "success",
        )

        self.assertEqual(
            data["tool_call"]["name"],
            "get_user_orders_tool",
        )

        self.assertEqual(
            data["tool_call"]["arguments"],
            {
                "action": "list",
            },
        )

    # --------------------------------------------------------
    # PROMPT ALIAS
    # --------------------------------------------------------

    def test_post_prompt_alias(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "prompt": "show my orders",
            },
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["tool_call"]["name"],
            "get_user_orders_tool",
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def test_get_command(self):
        response = self.client.get(
            "/assistant/command/",
            {
                "q": "show my orders",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["tool_call"]["name"],
            "get_user_orders_tool",
        )

    # --------------------------------------------------------
    # EMPTY BODY
    # --------------------------------------------------------

    def test_empty_post_body(self):
        response = self.client.post(
            "/assistant/command/",
            data="",
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.json()

        self.assertFalse(
            data["success"]
        )

        self.assertEqual(
            data["message"],
            "Request body cannot be empty.",
        )

    # --------------------------------------------------------
    # INVALID JSON
    # --------------------------------------------------------

    def test_invalid_json(self):
        response = self.client.post(
            "/assistant/command/",
            data="{invalid json}",
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.json()

        self.assertFalse(
            data["success"]
        )

        self.assertEqual(
            data["message"],
            "Invalid JSON request body.",
        )

    # --------------------------------------------------------
    # JSON ARRAY
    # --------------------------------------------------------

    def test_json_array_rejected(self):
        response = self.client.post(
            "/assistant/command/",
            data='["show my orders"]',
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.json()

        self.assertFalse(
            data["success"]
        )

        self.assertEqual(
            data["message"],
            "JSON body must be an object.",
        )

    # --------------------------------------------------------
    # EMPTY COMMAND
    # --------------------------------------------------------

    def test_empty_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": "",
            },
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.json()

        self.assertFalse(
            data["success"]
        )

        self.assertEqual(
            data["message"],
            "Command cannot be empty.",
        )

    # --------------------------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------------------------

    def test_unknown_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": (
                    "xyz something completely unknown"
                ),
            },
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        data = response.json()

        self.assertFalse(
            data["success"]
        )

        self.assertEqual(
            data["status"],
            "unknown",
        )

        self.assertEqual(
            data["tool_call"]["name"],
            "unknown",
        )

    # --------------------------------------------------------
    # CART COMMAND
    # --------------------------------------------------------

    def test_cart_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": "open cart",
            },
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertTrue(
            data["success"]
        )

        self.assertEqual(
            data["tool_call"]["name"],
            "get_cart_tool",
        )

        self.assertEqual(
            data["navigation"],
            "cart",
        )

    # --------------------------------------------------------
    # PRODUCT SEARCH COMMAND
    # --------------------------------------------------------

    def test_product_search_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": "find laptop",
            },
            content_type="application/json",
        )

        self.assertIn(
            response.status_code,
            {200, 400},
        )

        data = response.json()

        self.assertEqual(
            data["tool_call"]["name"],
            "search_products_tool",
        )

    # --------------------------------------------------------
    # PRODUCT DETAILS COMMAND
    # --------------------------------------------------------

    def test_product_details_command(self):
        response = self.client.post(
            "/assistant/command/",
            data={
                "command": "iphone 15 details",
            },
            content_type="application/json",
        )

        self.assertIn(
            response.status_code,
            {200, 400},
        )

        data = response.json()

        self.assertEqual(
            data["tool_call"]["name"],
            "get_product_description_tool",
        )