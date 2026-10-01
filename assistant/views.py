import json
import logging

from django.http import JsonResponse

from .normalizer import normalize_command
from .parser import parse_command
from .tools import execute_tool


logger = logging.getLogger(__name__)


# ============================================================
# ASSISTANT COMMAND API
# ============================================================

def command_api(request):
    """
    Deterministic conversational command endpoint with Contextual Memory support.
    """

    logger.info(
        "[ASSISTANT COMMAND] "
        "Method=%s | User=%s",
        request.method,
        request.user,
    )

    # ========================================================
    # METHOD VALIDATION
    # ========================================================

    if request.method not in {"GET", "POST"}:
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "Only GET and POST requests are allowed.",
            },
            status=405,
        )

    # ========================================================
    # GET COMMAND
    # ========================================================

    command = ""

    if request.method == "GET":
        command = request.GET.get("q", "")

    # ========================================================
    # POST COMMAND
    # ========================================================

    else:
        raw_body = (
            request.body.decode("utf-8")
            if request.body
            else ""
        )

        if not raw_body:
            return JsonResponse(
                {
                    "success": False,
                    "status": "error",
                    "message": "Request body cannot be empty.",
                },
                status=400,
            )

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "success": False,
                    "status": "error",
                    "message": "Invalid JSON request body.",
                },
                status=400,
            )

        if not isinstance(payload, dict):
            return JsonResponse(
                {
                    "success": False,
                    "status": "error",
                    "message": "JSON body must be an object.",
                },
                status=400,
            )

        command = payload.get(
            "command",
            payload.get("prompt", ""),
        )

    # ========================================================
    # COMMAND VALIDATION & NORMALIZATION
    # ========================================================

    if command is None:
        command = ""

    if not isinstance(command, str):
        command = str(command)

    command = command.strip()

    if not command:
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "Command cannot be empty.",
            },
            status=400,
        )

    normalized_command = normalize_command(command)

    if not normalized_command:
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "Command cannot be empty.",
            },
            status=400,
        )

    logger.info(
        "[ASSISTANT COMMAND] Original='%s' | Normalized='%s'",
        command,
        normalized_command,
    )

    # ========================================================
    # RETRIEVE SESSION CONTEXT (For "first one", "second one")
    # ========================================================

    context = {
        "last_search_results": request.session.get("last_search_results", [])
    }

    # ========================================================
    # PARSE COMMAND WITH CONTEXT
    # ========================================================

    try:
        tool_call = parse_command(
            normalized_command,
            context=context
        )

    except Exception:
        logger.exception("[ASSISTANT COMMAND] Parser failed.")
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "I couldn't understand that command.",
            },
            status=400,
        )

    # ========================================================
    # UNKNOWN COMMAND
    # ========================================================

    if tool_call.name == "unknown":
        return JsonResponse(
            {
                "success": False,
                "status": "unknown",
                "message": "I couldn't understand that command.",
                "command": command,
                "normalized_command": normalized_command,
                "tool_call": {
                    "name": tool_call.name,
                    "arguments": tool_call.arguments,
                },
            },
            status=400,
        )

    logger.info(
        "[ASSISTANT COMMAND] Tool=%s | Arguments=%s",
        tool_call.name,
        tool_call.arguments,
    )

    # ========================================================
    # EXECUTE TOOL
    # ========================================================

    try:
        result = execute_tool(
            tool_call,
            request=request,
            user=request.user,
        )

    except Exception:
        logger.exception("[ASSISTANT COMMAND] Tool execution failed.")
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "Something went wrong while executing your command.",
            },
            status=500,
        )

    if not isinstance(result, dict):
        logger.error("[ASSISTANT COMMAND] Tool returned non-dict result: %r", result)
        return JsonResponse(
            {
                "success": False,
                "status": "error",
                "message": "The command returned an invalid result.",
            },
            status=500,
        )

    # ========================================================
    # UPDATE SESSION CONTEXT (If search tool returned products)
    # ========================================================
    
    if tool_call.name == "search_products_tool" and "products" in result:
        # Save search results to session so pronouns/ordinals work next turn
        request.session["last_search_results"] = result["products"]
        request.session.modified = True

    tool_success = result.get("success", False)

    # ========================================================
    # RESPONSE BUILDER
    # ========================================================

    response_payload = {
        "success": tool_success,
        "status": "success" if tool_success else "error",
        "command": command,
        "normalized_command": normalized_command,
        "tool_call": {
            "name": tool_call.name,
            "arguments": tool_call.arguments,
        },
        "data": result,
        "message": result.get("message", ""),
    }

    # Preserve dynamic navigation/data fields
    for field in (
        "action",
        "navigation",
        "redirect",
        "redirect_url",
        "confirmation_required",
        "auto_open_cancel",
        "product",
        "products",
        "orders",
        "order",
        "profile",
    ):
        if field in result:
            response_payload[field] = result[field]

    logger.info(
        "[ASSISTANT COMMAND] Completed | Tool=%s | Success=%s",
        tool_call.name,
        tool_success,
    )

    return JsonResponse(
        response_payload,
        status=200 if tool_success else 400,
    )