from youtubesearchpython import VideosSearch
from datetime import datetime, timedelta
import re

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


def published_within_days(video, max_age_days=1):
    published = video.get("published", "")
    if not published:
        return False

    match = re.match(r"(\d+)\s+(\w+)\s+ago", published.lower())
    if not match:
        return False

    value, unit = int(match.group(1)), match.group(2)

    # Convert time to minutes
    minutes = 0
    if "minute" in unit:
        minutes = value
    elif "hour" in unit:
        minutes = value * 60
    elif "day" in unit:
        minutes = value * 1440
    elif "week" in unit:
        minutes = value * 10080
    else:
        return False  # Ignore months/years etc

    return minutes <= (max_age_days * 1440)


max_age_days = 7  # Change this to 2 or 3 if needed
filters = [

    no_shorts,
    is_trusted_channel,
    has_valid_view_count,
    is_ascii,
    lambda v: published_within_days(v, max_age_days)
]


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
def search_youtube_news(queries, limit=200, filters=[]):
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
                "url": result.get("link", ""),
                "published": result.get("publishedTime", "")  # <- this is crucial
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
    terms = [
        "Politics",
        "Business",
        "Technology",
        "Sports",
        "Entertainment",
        "Health",
        "Education",
        "Science",
        "Environment",
        "Crime",
        "World",
        "India",
        "Economy",
        "Weather",
        "Travel",
        "Culture",
        "Law and Order",
        "Defense",
        "Elections",
        "Social Issues"
    ]

    queries = build_queries(terms, prefix, suffix)
    grouped_videos = search_youtube_news(queries, limit=500, filters=filters)

    display_grouped_results(grouped_videos)
    #hi
