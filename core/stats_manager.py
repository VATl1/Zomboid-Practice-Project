from collections import Counter

class StatsManager:
    def __init__(self, items):
        self.items = items

    def get_condition_percentages(self):
       
        total = len(self.items)
        if total == 0:
            return {}

        counts = Counter(item['Condition'] for item in self.items)
        return {cond: round(count / total * 100, 2) for cond, count in counts.items()}

    def get_condition_percentages_for_name(self, name):
      
        filtered = [item for item in self.items if item['Name'].lower() == name.lower()]
        total = len(filtered)
        if total == 0:
            return {}

        counts = Counter(item['Condition'] for item in filtered)
        return {cond: round(count / total * 100, 2) for cond, count in counts.items()}
