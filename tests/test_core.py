import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import tempfile
import xml.etree.ElementTree as ET

from core import get_reader
from core.csv_reader import CSVReader
from core.json_reader import JSONReader
from core.xml_reader import XMLReader
from core.stats_manager import StatsManager


def test_get_reader_csv():
    reader = get_reader("data/items.csv")
    assert isinstance(reader, CSVReader)


def test_get_reader_json():
    reader = get_reader("data/items.json")
    assert isinstance(reader, JSONReader)


def test_get_reader_xml():
    reader = get_reader("data/items.xml")
    assert isinstance(reader, XMLReader)


def test_csv_reader(tmp_path):
    csv_content = """ID,Name,Type,Condition,Amount
1,Hummer,Tool,Mint,10
2,Nails,Fasteners,Good,450
"""
    file_path = tmp_path / "items.csv"
    file_path.write_text(csv_content, encoding="utf-8")

    reader = CSVReader()
    data = reader.read_file(str(file_path))

    assert len(data) == 2
    assert data[0]["Name"] == "Hummer"
    assert data[1]["Condition"] == "Good"


def test_json_reader(tmp_path):
    json_data = [
        {"ID": "1", "Name": "Hummer", "Type": "Tool", "Condition": "Mint", "Amount": "10"},
        {"ID": "2", "Name": "Nails", "Type": "Fasteners", "Condition": "Good", "Amount": "450"},
    ]
    file_path = tmp_path / "items.json"
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    reader = JSONReader()
    data = reader.read_file(str(file_path))

    assert len(data) == 2
    assert data[1]["Name"] == "Nails"


def test_xml_reader(tmp_path):
    xml_root = ET.Element("items")
    ET.SubElement(xml_root, "item", ID="1")
    child1 = ET.SubElement(xml_root, "item")
    ET.SubElement(child1, "Name").text = "Knife"
    ET.SubElement(child1, "Type").text = "Weapon"
    ET.SubElement(child1, "Condition").text = "Good"
    ET.SubElement(child1, "Amount").text = "5"

    file_path = tmp_path / "items.xml"
    ET.ElementTree(xml_root).write(file_path, encoding="utf-8")

    reader = XMLReader()
    data = reader.read_file(str(file_path))
    assert isinstance(data, list)


def test_stats_manager_all():
    items = [
        {"Name": "Hummer", "Condition": "Mint"},
        {"Name": "Nails", "Condition": "Good"},
        {"Name": "Nails", "Condition": "Bad"},
        {"Name": "Knife", "Condition": "Average"},
    ]

    stats = StatsManager(items)
    result = stats.get_condition_percentages()

    assert result["Mint"] == 25.0
    assert result["Good"] == 25.0
    assert result["Bad"] == 25.0
    assert result["Average"] == 25.0


def test_stats_manager_for_name():
    items = [
        {"Name": "Nails", "Condition": "Good"},
        {"Name": "Nails", "Condition": "Bad"},
        {"Name": "Hummer", "Condition": "Mint"},
    ]

    stats = StatsManager(items)
    result = stats.get_condition_percentages_for_name("Nails")

    assert "Good" in result
    assert "Bad" in result
    assert sum(result.values()) == 100.0
