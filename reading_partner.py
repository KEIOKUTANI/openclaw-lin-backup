#!/usr/bin/env python3
"""
Reading Partner - Book discussion and tracking system
"""
import os
import json
from datetime import datetime
from typing import List, Dict

class ReadingPartner:
    """
    Track books, discuss ideas, make recommendations
    """
    
    def __init__(self, library_file="/root/openclaw_data/lin/reading_library.json"):
        self.library_file = library_file
        self.library = self._load_library()
    
    def _load_library(self) -> Dict:
        """Load existing library or create new one"""
        if os.path.exists(self.library_file):
            with open(self.library_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"books": [], "notes": [], "quotes": []}
    
    def _save_library(self):
        """Save library to file"""
        with open(self.library_file, 'w', encoding='utf-8') as f:
            json.dump(self.library, f, indent=2, ensure_ascii=False)
    
    def add_book(self, title: str, author: str, status="reading", rating=None, notes=""):
        """Add a book to library"""
        book = {
            "id": len(self.library["books"]) + 1,
            "title": title,
            "author": author,
            "status": status,  # reading, finished, want_to_read
            "rating": rating,  # 1-5
            "notes": notes,
            "date_added": datetime.now().isoformat(),
            "date_finished": None
        }
        
        self.library["books"].append(book)
        self._save_library()
        
        print(f"✅ Added: '{title}' by {author}")
        return book
    
    def finish_book(self, book_id: int, rating: int, notes: str = ""):
        """Mark book as finished"""
        book = next((b for b in self.library["books"] if b["id"] == book_id), None)
        if book:
            book["status"] = "finished"
            book["rating"] = rating
            book["notes"] += "\n\n" + notes if notes else ""
            book["date_finished"] = datetime.now().isoformat()
            self._save_library()
            print(f"✅ Finished: '{book['title']}' - Rating: {rating}/5")
        else:
            print(f"❌ Book ID {book_id} not found")
    
    def add_quote(self, book_id: int, quote: str, page: int = None):
        """Save a quote from a book"""
        book = next((b for b in self.library["books"] if b["id"] == book_id), None)
        if book:
            quote_entry = {
                "book_id": book_id,
                "book_title": book["title"],
                "quote": quote,
                "page": page,
                "date_added": datetime.now().isoformat()
            }
            self.library["quotes"].append(quote_entry)
            self._save_library()
            print(f"✅ Quote saved from '{book['title']}'")
        else:
            print(f"❌ Book ID {book_id} not found")
    
    def list_books(self, status=None):
        """List books, optionally filtered by status"""
        books = self.library["books"]
        if status:
            books = [b for b in books if b["status"] == status]
        
        if not books:
            print(f"📚 No books found" + (f" with status '{status}'" if status else ""))
            return
        
        print(f"\n📚 Your Library" + (f" ({status})" if status else "") + ":\n")
        print(f"{'='*70}")
        
        for book in books:
            print(f"\n[{book['id']}] {book['title']}")
            print(f"    by {book['author']}")
            print(f"    Status: {book['status']}")
            if book['rating']:
                print(f"    Rating: {'⭐' * book['rating']} ({book['rating']}/5)")
            if book['notes']:
                print(f"    Notes: {book['notes'][:100]}...")
        
        print(f"\n{'='*70}\n")
    
    def recommend(self, mood: str = None, topic: str = None):
        """Recommend books based on mood or topic"""
        print(f"\n💡 Book Recommendations")
        print(f"{'='*70}\n")
        
        # Simple recommendation logic (can be enhanced with AI)
        finished_books = [b for b in self.library["books"] if b["status"] == "finished" and b["rating"] and b["rating"] >= 4]
        
        if not finished_books:
            print("📖 You haven't rated any books yet.")
            print("   Add some books and ratings to get personalized recommendations!")
            return
        
        print(f"Based on your highly-rated books:")
        for book in finished_books[:3]:
            print(f"- {book['title']} by {book['author']} ({'⭐' * book['rating']})")
        
        print(f"\n🎯 You might also enjoy:")
        print("  [AI-powered recommendations would go here]")
        print("  [Consider integrating with Goodreads API or similar]")
        print(f"\n{'='*70}\n")
    
    def discuss(self, book_id: int, question: str):
        """Discuss a book with Lin"""
        book = next((b for b in self.library["books"] if b["id"] == book_id), None)
        if not book:
            print(f"❌ Book ID {book_id} not found")
            return
        
        print(f"\n💬 Discussing: '{book['title']}' by {book['author']}")
        print(f"{'='*70}\n")
        print(f"You: {question}\n")
        
        # This would integrate with OpenAI/Claude for actual discussion
        print(f"Lin: [This would integrate with AI for rich discussion]")
        print(f"      For now, this is a placeholder.")
        print(f"      Your question about '{book['title']}' is noted.\n")
        
        # Save discussion
        discussion_entry = {
            "book_id": book_id,
            "book_title": book["title"],
            "question": question,
            "response": "[AI response would go here]",
            "date": datetime.now().isoformat()
        }
        
        if "discussions" not in self.library:
            self.library["discussions"] = []
        
        self.library["discussions"].append(discussion_entry)
        self._save_library()
        
        print(f"💾 Discussion saved\n")


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Reading Partner - Book tracking & discussion')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add book
    add_parser = subparsers.add_parser('add', help='Add a book')
    add_parser.add_argument('title', help='Book title')
    add_parser.add_argument('author', help='Author name')
    add_parser.add_argument('--status', choices=['reading', 'finished', 'want_to_read'], default='reading')
    add_parser.add_argument('--rating', type=int, choices=[1,2,3,4,5])
    
    # List books
    list_parser = subparsers.add_parser('list', help='List books')
    list_parser.add_argument('--status', choices=['reading', 'finished', 'want_to_read'])
    
    # Finish book
    finish_parser = subparsers.add_parser('finish', help='Mark book as finished')
    finish_parser.add_argument('id', type=int, help='Book ID')
    finish_parser.add_argument('rating', type=int, choices=[1,2,3,4,5])
    finish_parser.add_argument('--notes', default='')
    
    # Add quote
    quote_parser = subparsers.add_parser('quote', help='Save a quote')
    quote_parser.add_argument('id', type=int, help='Book ID')
    quote_parser.add_argument('quote', help='Quote text')
    quote_parser.add_argument('--page', type=int)
    
    # Recommend
    recommend_parser = subparsers.add_parser('recommend', help='Get book recommendations')
    recommend_parser.add_argument('--mood')
    recommend_parser.add_argument('--topic')
    
    # Discuss
    discuss_parser = subparsers.add_parser('discuss', help='Discuss a book')
    discuss_parser.add_argument('id', type=int, help='Book ID')
    discuss_parser.add_argument('question', help='Your question')
    
    args = parser.parse_args()
    
    partner = ReadingPartner()
    
    if args.command == 'add':
        partner.add_book(args.title, args.author, args.status, args.rating)
    elif args.command == 'list':
        partner.list_books(args.status)
    elif args.command == 'finish':
        partner.finish_book(args.id, args.rating, args.notes)
    elif args.command == 'quote':
        partner.add_quote(args.id, args.quote, args.page)
    elif args.command == 'recommend':
        partner.recommend(args.mood, args.topic)
    elif args.command == 'discuss':
        partner.discuss(args.id, args.question)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
