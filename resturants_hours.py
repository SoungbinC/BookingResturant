import json
from collections import Counter

with open("scraped_restaurants.json", "r", encoding="utf-8") as f:
    data = json.load(f)

hours_counter = Counter()
example_snippets = []

for entry in data:
    hours = entry.get("hours", "").strip()
    if hours:
        hours_counter[hours] += 1
        if len(example_snippets) < 10:
            example_snippets.append(hours)

# Print top patterns
print("🔢 Most Common Patterns:")
for hrs, count in hours_counter.most_common(10):
    print(f"({count}x) {hrs}")

print("\n🧪 Sample Hours:")
for h in example_snippets:
    print("-", h)
