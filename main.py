import argparse
from core import get_reader
from core.stats_manager import StatsManager

def main():

    parser = argparse.ArgumentParser(description="Zomboid Inventory CLI")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "xml"],
        default="csv",
        help="Формат даних (за замовчуванням csv)"
    )
    parser.add_argument("--percent_all", action="store_true",
                        help="Показати відсоткове співвідношення станів усіх предметів")
    parser.add_argument("--percent_name", type=str,
                        help="Показати відсоткове співвідношення станів для заданої назви предмета")

    args = parser.parse_args()


    file_path = f"data/items.{args.format}"
    reader = get_reader(file_path)
    items = reader.read_file(file_path)
    stats = StatsManager(items)

 
    if args.percent_all:
        result = stats.get_condition_percentages()
        print(f"\n Відсоткове співвідношення станів ({args.format.upper()}):")
        for cond, perc in result.items():
            print(f"{cond}: {perc}%")

    elif args.percent_name:
        result = stats.get_condition_percentages_for_name(args.percent_name)
        if result:
            print(f"\n Відсоткове співвідношення станів для '{args.percent_name}' ({args.format.upper()}):")
            for cond, perc in result.items():
                print(f"{cond}: {perc}%")
        else:
            print(f"Предмет із назвою '{args.percent_name}' не знайдено.")
    else:
        print(f"=== DATA/ITEMS.{args.format.upper()} ===")
        print(items)

if __name__ == "__main__":
    main()
