# import re

# def parse_user_prompt(prompt_text):
#     """
#     EXTRACTOR: Converts natural language inputs into structured tool parameters.
    
#     Examples:
#     - "Laptops under 500 dollars" -> query: "laptops", max_price: 500.0
#     - "Shoes between 50 and 150" -> query: "shoes", min_price: 50.0, max_price: 150.0
#     - "Dell laptops over 800"    -> query: "dell laptops", min_price: 800.0
#     """
#     if not prompt_text:
#         return {
#             "tool_call": "search_products_tool",
#             "arguments": {"query": None, "min_price": None, "max_price": None}
#         }

#     text = prompt_text.lower()
#     min_price = None
#     max_price = None

#     # 1. Matches price ranges: "between 50 and 150", "50 to 150", "50-150"
#     range_match = re.search(r'(?:between|range)?\s*\$?(\d+(?:\.\d+)?)\s*(?:to|and|-)\s*\$?(\d+(?:\.\d+)?)', text)
#     if range_match:
#         val1 = float(range_match.group(1))
#         val2 = float(range_match.group(2))
#         min_price, max_price = min(val1, val2), max(val1, val2)

#     # 2. Matches upper bound: "under 500", "below 300", "less than 200", "max 400"
#     under_match = re.search(r'(?:under|below|less than|cheap|max)\s*\$?(\d+(?:\.\d+)?)', text)
#     if under_match and max_price is None:
#         max_price = float(under_match.group(1))

#     # 3. Matches lower bound: "over 100", "above 200", "more than 300", "min 50"
#     over_match = re.search(r'(?:over|above|more than|min)\s*\$?(\d+(?:\.\d+)?)', text)
#     if over_match and min_price is None:
#         min_price = float(over_match.group(1))

#     # 4. Strip out price tokens and structural stop words to clean the query string
#     stop_words = [
#         r'\$?(\d+(?:\.\d+)?)', r'between', r'range', r'under', r'below', 
#         r'less than', r'over', r'above', r'more than', r'to', r'and', 
#         r'dollars?', r'bucks?', r'in', r'for', r'cheap', r'show', r'me',
#         r'find', r'search', r'looking', r'want'
#     ]
    
#     clean_query = text
#     for pattern in stop_words:
#         clean_query = re.sub(r'\b' + pattern + r'\b', '', clean_query)

#     clean_query = ' '.join(clean_query.split()).strip()

#     return {
#         "tool_call": "search_products_tool",
#         "arguments": {
#             "query": clean_query if clean_query else None,
#             "min_price": min_price,
#             "max_price": max_price
#         }
#     }