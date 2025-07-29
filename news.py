from youtubesearchpython import VideosSearch

# Trusted news channels
trusted_channels = [
    "NDTV", "India Today", "CNN", "BBC", "Aaj Tak", "ABP", "WION",
    "Hindustan Times", "The Hindu", "Times Now"
]

# --- FILTER FUNCTIONS ---
def no_shorts(video):
    return "/shorts/" not in video.get('url', '') and "shorts" not in video.get('title', '').lower()

def is_trusted_channel(video):
    return any(trusted.lower() in video.get('uploader', '').lower() for trusted in trusted_channels)

def has_valid_view_count(video):
    try:
        return parse_view_count(video.get('views', '0')) is not None
    except:
        return False

def is_ascii(video):
    title = str(video.get('title', ''))
    return all(ord(char) < 128 for char in title)

filters = [no_shorts, is_trusted_channel, has_valid_view_count, is_ascii]

def passes_all_filters(video, filters):
    return all(f(video) for f in filters)

# --- VIEW COUNT PARSER ---
def parse_view_count(view_str):
    if not view_str:
        return 0
    view_str = view_str.lower().replace(" views", "").strip()
    try:
        if "k" in view_str:
            return int(float(view_str.replace("k", "")) * 1_000)
        elif "m" in view_str:
            return int(float(view_str.replace("m", "")) * 1_000_000)
        elif "b" in view_str:
            return int(float(view_str.replace("b", "")) * 1_000_000_000)
        else:
            return int(view_str.replace(",", ""))
    except ValueError:
        return 0

# --- QUERY BUILDER ---
def build_queries(terms, prefix="", suffix=""):
    return [f"{prefix} {term} {suffix}".strip() for term in terms]

# --- SEARCH FUNCTION ---
def search_youtube_news(queries, limit=20, filters=[]):
    grouped_results = {}

    for query in queries:
        print(f"\n🔍 Searching: {query}")
        videos_search = VideosSearch(query, limit=limit)
        results = videos_search.result().get("result", [])
        group = []

        for result in results:
            video = {
                "title": result.get("title", ""),
                "uploader": result.get("channel", {}).get("name", ""),
                "views": result.get("viewCount", {}).get("text", "0"),
                "duration": result.get("duration", ""),
                "url": result.get("link", "")
            }

            if not passes_all_filters(video, filters):
                continue

            video["parsed_views"] = parse_view_count(video["views"])
            group.append(video)

        group.sort(key=lambda x: x["parsed_views"], reverse=True)
        grouped_results[query] = group

    return grouped_results

# --- DISPLAY FUNCTION ---
def display_grouped_results(grouped_results):
    for query, videos in grouped_results.items():
        print(f"\n📌 Results for: {query}")
        if not videos:
            print("   No videos found.\n")
            continue

        for i, video in enumerate(videos, 1):
            print(f"  {i}. {video['title']} - {video['uploader']}")
            #print(f"     {video['url']}")
        print()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    prefix = "India News"
    suffix = "2025"
    terms = ["murder", "cricket", "politics", "riot", "tech AI"]

    queries = build_queries(terms, prefix, suffix)
    grouped_videos = search_youtube_news(queries, limit=50, filters=filters)

    display_grouped_results(grouped_videos)
    #hi
