def detect_title(pages_data):
    # On page one, find the text with largest size
    if not pages_data or not pages_data[0]:
        return "Untitled Document"
    first_page = pages_data[0]
    largest = max(first_page, key=lambda e: e["size"])
    return largest["text"]
