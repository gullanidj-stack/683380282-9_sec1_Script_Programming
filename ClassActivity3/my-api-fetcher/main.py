"""
main.py
โปรแกรมหลัก Interactive CLI สำหรับทดสอบการเชื่อมต่อ Web API
สัปดาห์ที่ 10: Interacting with Web APIs: Fetching and Processing JSON Data

เมนู 1-3 : โค้ดตัวอย่างจากห้องเรียน
เมนู 4-6 : งานที่ได้รับมอบหมาย (Task 1-3) + Input Validation (Task 4)
"""

import sys
from typing import Optional

# ปรับปรุงการแสดงผลภาษาไทยและ Emoji บน Windows Console
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.api_client import APIClient, export_to_json_file

OUTPUT_DIR = "output"  # โฟลเดอร์เก็บไฟล์ JSON ที่ export


def display_menu() -> None:
    """แสดงเมนูตัวเลือกการทำงานของโปรแกรม"""
    print("\n" + "=" * 45)
    print("   🌐 Web API Data Fetcher CLI (Week 10)")
    print("=" * 45)
    print("  1. ดึงข้อมูลงานเดี่ยว (Fetch Single TODO)")
    print("  2. ดึงรายการโพสต์ทั้งหมด (Fetch All Posts)")
    print("  3. ดึงรายการ TODO ตามรหัสผู้ใช้ (Fetch User TODOs)")
    print("  4. ดึงข้อมูลโปรไฟล์ผู้ใช้ (Fetch User Profile)")
    print("  5. ดึงคอมเมนต์ใต้โพสต์ (Fetch Post Comments)")
    print("  6. ดึงข้อมูลแล้วบันทึกเป็นไฟล์ JSON (Fetch & Export to JSON)")
    print("  7. ออกจากโปรแกรม (Exit)")
    print("=" * 45)


def ask_positive_int(prompt: str, label: str) -> Optional[int]:
    """
    ถามตัวเลขจำนวนเต็มบวกจากผู้ใช้ พร้อมตรวจสอบความถูกต้อง (Input Validation)
    :return: ตัวเลขที่ถูกต้อง หรือ None หากป้อนไม่ถูกต้อง (แสดงข้อความแจ้งเตือนแล้ว)
    """
    raw_input = input(prompt).strip()
    try:
        value = int(raw_input)
    except ValueError:
        print(f"❌ ข้อผิดพลาด: '{raw_input}' ไม่ใช่ตัวเลขที่ถูกต้อง กรุณาป้อนเฉพาะตัวเลขจำนวนเต็ม")
        return None
    if value <= 0:
        print(f"❌ ข้อผิดพลาด: {label} ต้องเป็นตัวเลขจำนวนเต็มบวกที่มากกว่า 0")
        return None
    return value


def handle_fetch_single_todo(client: APIClient) -> None:
    """ฟังก์ชันจัดการการดึงข้อมูล TODO รายการเดี่ยว"""
    todo_id = ask_positive_int("กรุณาป้อนรหัส TODO ID ที่ต้องการค้นหา (เช่น 1, 5, 10): ", "รหัส TODO ID")
    if todo_id is None:
        return

    todo_item = client.fetch_single_todo(todo_id)
    if todo_item:
        print("\n📋 --- ข้อมูลงาน TODO รายการเดี่ยว ---")
        print(f"  • รหัสงาน (ID)       : {todo_item.get('id')}")
        print(f"  • รหัสผู้รับผิดชอบ (User ID): {todo_item.get('userId')}")
        print(f"  • หัวข้องาน (Title)  : {todo_item.get('title')}")
        status_text = "เสร็จสิ้น (Completed) ✅" if todo_item.get("completed") else "รอดำเนินการ (Pending) ⏳"
        print(f"  • สถานะงาน (Status)  : {status_text}")
        print("----------------------------------------")
    else:
        print(f"⚠️ ไม่พบข้อมูล TODO สำหรับ ID: {todo_id}")


def handle_fetch_all_posts(client: APIClient) -> None:
    """ฟังก์ชันจัดการการดึงและแสดงรายการโพสต์"""
    posts = client.fetch_all_posts()
    if posts:
        total_posts = len(posts)
        display_limit = 5  # แสดงเฉพาะ 5 รายการแรกเพื่อความกระชับในเทอร์มินัล
        print(f"\n📝 --- แสดง {display_limit} รายการแรก (จากทั้งหมด {total_posts} รายการ) ---")

        for index, post in enumerate(posts[:display_limit], start=1):
            print(f"\n[{index}] Post ID: {post.get('id')} | User ID: {post.get('userId')}")
            print(f"    หัวข้อ (Title): {post.get('title')}")
            body_snippet = post.get("body", "").replace("\n", " ")[:60]
            print(f"    เนื้อหา (Body) : {body_snippet}...")

        if total_posts > display_limit:
            print(f"\n... และยังมีอีก {total_posts - display_limit} โพสต์ที่ไม่ได้แสดงบนหน้าจอ")
        print("-" * 45)
    else:
        print("⚠️ ไม่สามารถดึงรายการโพสต์ได้ในขณะนี้")


def handle_fetch_user_todos(client: APIClient) -> None:
    """ฟังก์ชันจัดการการดึงงาน TODO ของผู้ใช้ตามรหัสผู้ใช้"""
    user_id = ask_positive_int("กรุณาป้อนรหัสผู้ใช้งาน User ID (เช่น 1, 2, 3): ", "User ID")
    if user_id is None:
        return

    user_todos = client.fetch_user_todos(user_id)
    if user_todos is None:
        print(f"⚠️ เกิดข้อผิดพลาด ไม่สามารถดึงงานของ User ID {user_id} ได้")
    elif len(user_todos) == 0:
        print(f"ℹ️ ไม่พบรายการงาน TODO ของ User ID {user_id}")
    else:
        print(f"\n📋 --- รายการงาน TODO ทั้งหมดของ User ID {user_id} (รวม {len(user_todos)} รายการ) ---")
        completed_count = 0
        for todo in user_todos:
            is_done = todo.get("completed", False)
            if is_done:
                completed_count += 1
            status_icon = "✅" if is_done else "⏳"
            print(f"  [{todo.get('id'):03d}] {status_icon} {todo.get('title')}")

        print("-" * 45)
        print(f"สรุป: เสร็จแล้ว {completed_count}/{len(user_todos)} งาน | รอดำเนินการ {len(user_todos) - completed_count} งาน")


def handle_user_profile(client: APIClient) -> None:
    """Task 1: แสดงข้อมูลโปรไฟล์ผู้ใช้ (รวมข้อมูลแบบ Nested Dictionary)"""
    user_id = ask_positive_int("กรุณาป้อนรหัสผู้ใช้งาน User ID (เช่น 1, 2, 5): ", "User ID")
    if user_id is None:
        return

    user = client.fetch_user_profile(user_id)
    if user:
        # เข้าถึง Nested Dictionary อย่างปลอดภัยด้วย .get() ซ้อนกัน
        company_name = user.get("company", {}).get("name", "ไม่ระบุ")
        city = user.get("address", {}).get("city", "ไม่ระบุ")
        print("\n👤 --- ข้อมูลโปรไฟล์ผู้ใช้งาน ---")
        print(f"  • รหัสผู้ใช้ (ID)       : {user.get('id')}")
        print(f"  • ชื่อ-นามสกุล (Name)   : {user.get('name')}")
        print(f"  • ชื่อผู้ใช้ (Username) : {user.get('username')}")
        print(f"  • อีเมล (Email)         : {user.get('email')}")
        print(f"  • เบอร์โทรศัพท์ (Phone) : {user.get('phone')}")
        print(f"  • บริษัท (Company)      : {company_name}")
        print(f"  • เมืองที่อยู่ (City)   : {city}")
        print("----------------------------------------")
    else:
        print(f"⚠️ ไม่พบข้อมูลโปรไฟล์สำหรับ User ID {user_id}")


def handle_post_comments(client: APIClient) -> None:
    """Task 2: แสดงคอมเมนต์ใต้โพสต์"""
    post_id = ask_positive_int("กรุณาป้อนรหัสโพสต์ Post ID (เช่น 1, 2, 3): ", "Post ID")
    if post_id is None:
        return

    comments = client.fetch_post_comments(post_id)
    if comments is None:
        print(f"⚠️ เกิดข้อผิดพลาดในการดึงคอมเมนต์ของ Post ID {post_id}")
    elif len(comments) == 0:
        print(f"ℹ️ ไม่พบคอมเมนต์สำหรับ Post ID {post_id}")
    else:
        display_limit = 5
        print(f"\n💬 --- พบคอมเมนต์ทั้งหมด {len(comments)} รายการสำหรับ Post ID {post_id} ---")
        for index, comment in enumerate(comments[:display_limit], start=1):
            print(f"\n[{index}] ผู้เขียน (Name): {comment.get('name')}")
            print(f"    อีเมล (Email) : {comment.get('email')}")
            body_snippet = comment.get("body", "").replace("\n", " ")[:70]
            print(f"    ข้อความ (Body): {body_snippet}...")

        if len(comments) > display_limit:
            print(f"\n... และยังมีอีก {len(comments) - display_limit} คอมเมนต์ที่ไม่ได้แสดงบนหน้าจอ")
        print("-" * 45)


def handle_export_to_json(client: APIClient) -> None:
    """Task 3: ดึงข้อมูลแล้วบันทึกลงไฟล์ JSON"""
    print("\n📦 เลือกประเภทข้อมูลที่ต้องการดึงและบันทึก:")
    print("  A. งานเดี่ยว (Single TODO)")
    print("  B. โปรไฟล์ผู้ใช้ (User Profile)")
    print("  C. คอมเมนต์ใต้โพสต์ (Post Comments)")
    sub_choice = input("กรุณาเลือก (A/B/C): ").strip().upper()

    if sub_choice == "A":
        item_id = ask_positive_int("ป้อน TODO ID ที่ต้องการ: ", "รหัส TODO ID")
        fetch, default_name = client.fetch_single_todo, f"todo_{item_id}.json"
    elif sub_choice == "B":
        item_id = ask_positive_int("ป้อน User ID ที่ต้องการ: ", "User ID")
        fetch, default_name = client.fetch_user_profile, f"user_{item_id}_profile.json"
    elif sub_choice == "C":
        item_id = ask_positive_int("ป้อน Post ID ที่ต้องการ: ", "Post ID")
        fetch, default_name = client.fetch_post_comments, f"post_{item_id}_comments.json"
    else:
        print("⚠️ ตัวเลือกไม่ถูกต้อง ยกเลิกการส่งออกข้อมูล")
        return

    if item_id is None:
        return

    data = fetch(item_id)
    if not data:
        print("⚠️ ไม่พบข้อมูลที่จะนำไปบันทึกลงไฟล์")
        return

    typed_name = input(f"ระบุชื่อไฟล์ที่ต้องการบันทึก (กด Enter เพื่อใช้ '{default_name}'): ").strip()
    file_name = typed_name or default_name
    if not file_name.lower().endswith(".json"):
        file_name += ".json"
    export_to_json_file(f"{OUTPUT_DIR}/{file_name}", data)


def main() -> None:
    """ฟังก์ชันหลักในการควบคุม Flow การทำงานของโปรแกรม"""
    client = APIClient()

    while True:
        display_menu()
        choice = input("กรุณาเลือกเมนู (1-7): ").strip()

        if choice == "1":
            handle_fetch_single_todo(client)
        elif choice == "2":
            handle_fetch_all_posts(client)
        elif choice == "3":
            handle_fetch_user_todos(client)
        elif choice == "4":
            handle_user_profile(client)
        elif choice == "5":
            handle_post_comments(client)
        elif choice == "6":
            handle_export_to_json(client)
        elif choice == "7":
            print("\n👋 ขอบคุณที่ใช้งานโปรแกรม ขอยุติการทำงาน!")
            break
        else:
            print("⚠️ ตัวเลือกไม่ถูกต้อง กรุณาป้อนตัวเลขระหว่าง 1 ถึง 7 เท่านั้น")


if __name__ == "__main__":
    main()
