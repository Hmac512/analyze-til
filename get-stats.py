import json
import os
from datetime import datetime


folders = [
    "TIL/"
]


files = []
for fdir in folders:
    json_files = [os.path.join(fdir, pos_json) for pos_json in os.listdir(
        fdir) if pos_json.endswith('.json')]
    files.extend(json_files)


all_items = []
total_comments = 0
post_ids = set()
for file in files:
    with open(file, "r") as f:
        raw = f.read()
    data = json.loads(raw)
    posts = data["data"]["postFeed"]["elements"]["edges"]
    for edge in posts:
        node = edge["node"]
        if node["__typename"] == "AdPost":
            continue
        if not node["id"] in post_ids:
            post = {
                "id": node["id"],
                "createdAt": node["createdAt"],
                "title": node["title"],
                "score": node["score"],
                "commentCount": node["commentCount"]
            }
            total_comments += node["commentCount"]
            all_items.append(post)
            post_ids.add(node["id"])


sorted_items = sorted(all_items, key=lambda x: x["createdAt"], reverse=False)
with open(f"til-posts.json", "w") as f:
    f.write(json.dumps(sorted_items, indent=4))


num_posts = len(sorted_items)
avg_comments = total_comments / num_posts

first_date = datetime.strptime(
    sorted_items[0]["createdAt"], "%Y-%m-%dT%H:%M:%S.%f%z")
last_date = datetime.strptime(
    sorted_items[-1]["createdAt"], "%Y-%m-%dT%H:%M:%S.%f%z")
print(f"Num posts {num_posts}")
print(f"Avg comments per post {avg_comments}")

delta = last_date - first_date
print(f"Num days of posts collected {delta.days}")
print(f"Comments per day {total_comments/delta.days}")
print(f"Posts per day {num_posts/delta.days}")
