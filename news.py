import yt_dlp


def scrape_youtube_news(query, max_results=10):
    search_url = f"ytsearch{max_results}:{query}"

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)

    print(f"\n🔍 Top {max_results} results for: {query}\n")
    for i, video in enumerate(info['entries'], 1):
        print(f"{i}. {video['title']}")
        print(f"   📎 URL: https://www.youtube.com/watch?v={video['id']}")
        print(f"   📅 Upload Date: {video.get('upload_date', 'Unknown')}")
        print()


# Example usage:
Sources = ['NDTV', 'Times of India', 'Brut India']
Topics = ['Politics', 'Sports', 'Accidents', 'Events']

for source in Sources:
    for topic in Topics:
        scrape_youtube_news(f"{source} {topic} recent India")
        print('-'*100)