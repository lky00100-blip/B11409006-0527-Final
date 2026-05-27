import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional

BOOKS_FILE = "books.json"
LEGACY_FILE = "lib_data.txt"

@dataclass
class Book:
    title: str
    isbn: str
    status: str

    def to_dict(self):
        return asdict(self)


class LibraryManager:
    def __init__(self, storage_path: str = BOOKS_FILE):
        self.storage_path = storage_path
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.books = [Book(**item) for item in data if self._valid_book_data(item)]
            except (json.JSONDecodeError, OSError) as exc:
                print(f"[Warning] 無法讀取 JSON 檔案: {exc}. 將使用空的書籍資料。")
                self.books = []
        elif os.path.exists(LEGACY_FILE):
            self.books = self._load_legacy_file(LEGACY_FILE)
            self.save_books()
        else:
            self.books = []

    def _valid_book_data(self, item: dict) -> bool:
        return all(key in item for key in ("title", "isbn", "status"))

    def _load_legacy_file(self, path: str) -> List[Book]:
        books: List[Book] = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "@@" not in line:
                        continue
                    title, rest = line.split("@@", 1)
                    parts = rest.split("##")
                    if len(parts) != 2:
                        continue
                    isbn, status = parts
                    books.append(Book(title=title, isbn=isbn, status=status))
        except OSError as exc:
            print(f"[Warning] 讀取舊資料檔案失敗: {exc}")
        return books

    def save_books(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=2)
        except OSError as exc:
            print(f"[Error] 無法寫入書籍檔案: {exc}")

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        return next((book for book in self.books if book.isbn == isbn), None)

    def add_book(self, title: str, isbn: str, status: str) -> bool:
        if self.find_by_isbn(isbn) is not None:
            return False
        self.books.append(Book(title=title, isbn=isbn, status=status))
        return True

    def borrow_book(self, isbn: str) -> Optional[str]:
        book = self.find_by_isbn(isbn)
        if book is None:
            return None
        if book.status == "borrowed":
            return "already_borrowed"
        book.status = "borrowed"
        return "updated"

    def list_books(self) -> List[str]:
        return [f"書名: {book.title}, ISBN: {book.isbn}, 狀態: {book.status}" for book in self.books]


def parse_add_command(command: str) -> Optional[tuple[str, str, str]]:
    try:
        payload = command[4:].strip()
        title, isbn, status = [part.strip() for part in payload.split("/", 2)]
        if not title or not isbn or not status:
            return None
        return title, isbn, status
    except ValueError:
        return None


def print_help():
    print("可用指令：")
    print("  add <title>/<isbn>/<status>  - 新增書籍")
    print("  show                       - 顯示所有書籍")
    print("  borrow <isbn>              - 借閱書籍")
    print("  exit                       - 儲存並離開")


def main():
    library = LibraryManager()
    print("=== 圖書管理系統 v0.2 (Modern) ===")
    print_help()

    while True:
        try:
            op = input("> ").strip()
        except EOFError:
            print("\n輸入中止。系統關閉。")
            library.save_books()
            break

        if op == "exit":
            library.save_books()
            print("系統關閉")
            break

        if op == "show":
            for line in library.list_books():
                print(line)
            continue

        if op.startswith("add "):
            parsed = parse_add_command(op)
            if parsed is None:
                print("Format Error")
                continue
            title, isbn, status = parsed
            if library.add_book(title, isbn, status):
                print("Success")
            else:
                print("ISBN Exist")
            continue

        if op.startswith("borrow "):
            isbn = op[7:].strip()
            if not isbn:
                print("Format Error")
                continue
            result = library.borrow_book(isbn)
            if result is None:
                print("ISBN Not Found")
            elif result == "already_borrowed":
                print("Already Borrowed")
            else:
                print("Updated")
            continue

        if op == "help":
            print_help()
            continue

        print("Unknown Command")


if __name__ == "__main__":
    main()
