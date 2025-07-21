def find_size_thresholds(pages_data, n=3):
    # Collect all font sizes, then pick top 3 as H1/H2/H3
    sizes = set()
    for page in pages_data:
        for line in page:
            sizes.add(line["size"])
    sizes = sorted(sizes, reverse=True)
    return sizes[:n] if len(sizes) >= n else sizes + [0]*(n - len(sizes))

def detect_headings(pages_data):
    h1_size, h2_size, h3_size = find_size_thresholds(pages_data)
    headings = []
    for page_num, page in enumerate(pages_data, 1):
        for line in page:
            lvl = None
            if abs(line["size"] - h1_size) < 0.5:
                lvl = "H1"
            elif abs(line["size"] - h2_size) < 0.5:
                lvl = "H2"
            elif abs(line["size"] - h3_size) < 0.5:
                lvl = "H3"
            if lvl:
                headings.append({
                    "level": lvl,
                    "text": line["text"],
                    "page": page_num
                })
    return headings
