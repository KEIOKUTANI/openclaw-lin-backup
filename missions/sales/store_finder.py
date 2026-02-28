#!/usr/bin/env python3
"""
Google Maps API を使用して店舗を検索し、Webサイト未設定店舗を抽出
"""
import os
import json
import csv
import requests
from datetime import datetime
import argparse

# API設定
API_KEY = "AIzaSyA9U8vz3LGSdKcTFDbYYaudtRwqi2XDnIE"
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

def search_places(location, radius=5000, place_type="restaurant", keyword=None):
    """指定エリアで店舗を検索"""
    params = {
        "location": location,
        "radius": radius,
        "type": place_type,
        "key": API_KEY,
        "language": "ja"
    }
    
    if keyword:
        params["keyword"] = keyword
    
    results = []
    next_page_token = None
    
    while True:
        if next_page_token:
            params["pagetoken"] = next_page_token
        
        response = requests.get(PLACES_API_URL, params=params)
        data = response.json()
        
        if data.get("status") != "OK":
            print(f"API Error: {data.get('status')}")
            break
        
        results.extend(data.get("results", []))
        next_page_token = data.get("next_page_token")
        
        if not next_page_token:
            break
        
        # APIレート制限対策（次ページトークンが有効になるまで待機）
        import time
        time.sleep(2)
    
    return results

def get_place_details(place_id):
    """店舗の詳細情報を取得"""
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,rating,user_ratings_total",
        "key": API_KEY,
        "language": "ja"
    }
    
    response = requests.get(DETAILS_API_URL, params=params)
    data = response.json()
    
    if data.get("status") == "OK":
        return data.get("result", {})
    return {}

def filter_no_website_stores(places):
    """Webサイト未設定の店舗を抽出"""
    no_website_stores = []
    
    for place in places:
        place_id = place.get("place_id")
        name = place.get("name")
        
        print(f"Checking: {name}...")
        
        details = get_place_details(place_id)
        
        # Webサイトが設定されていない店舗のみ抽出
        if not details.get("website"):
            store_info = {
                "name": details.get("name", name),
                "address": details.get("formatted_address", ""),
                "phone": details.get("formatted_phone_number", ""),
                "rating": details.get("rating", 0),
                "reviews": details.get("user_ratings_total", 0),
                "place_id": place_id,
                "website": None
            }
            no_website_stores.append(store_info)
            print(f"  ✓ No website found")
        
        # APIレート制限対策
        import time
        time.sleep(0.5)
    
    return no_website_stores

def save_to_csv(stores, filename):
    """CSV形式で保存"""
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        if stores:
            writer = csv.DictWriter(f, fieldnames=stores[0].keys())
            writer.writeheader()
            writer.writerows(stores)
    
    print(f"\nSaved to: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(description="Google Maps店舗検索・Webサイト未設定店舗抽出")
    parser.add_argument("--location", required=True, help="検索中心座標 (lat,lng)")
    parser.add_argument("--radius", type=int, default=5000, help="検索半径（メートル）")
    parser.add_argument("--type", default="restaurant", help="店舗タイプ")
    parser.add_argument("--keyword", help="検索キーワード")
    
    args = parser.parse_args()
    
    print(f"Searching places near {args.location}...")
    places = search_places(args.location, args.radius, args.type, args.keyword)
    print(f"Found {len(places)} places")
    
    print("\nFiltering stores without website...")
    no_website_stores = filter_no_website_stores(places)
    print(f"\n{len(no_website_stores)} stores without website found")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stores_no_website_{timestamp}.csv"
    save_to_csv(no_website_stores, filename)
    
    # サマリー表示
    print("\n=== Summary ===")
    print(f"Total places: {len(places)}")
    print(f"No website: {len(no_website_stores)}")
    print(f"Ratio: {len(no_website_stores)/len(places)*100:.1f}%")

if __name__ == "__main__":
    main()
