import requests
import json
import time
from datetime import datetime

class CheckInBot:
    def __init__(self):
        self.url = "https://rhuna-services-x4ige.ondigitalocean.app/api/v1/pulsar/challenges/do-task"
        self.task_guid = "2dd815c1-55a7-41e3-80af-fa4b814f8ed0"
        self.accounts = self.load_accounts()
        
    def load_accounts(self):
        """Membaca token dari file akun.txt"""
        try:
            with open('akun.txt', 'r') as f:
                tokens = [line.strip() for line in f if line.strip()]
            print(f"âœ“ Berhasil memuat {len(tokens)} akun")
            return tokens
        except FileNotFoundError:
            print("âœ— File akun.txt tidak ditemukan!")
            print("  Buat file akun.txt dan masukkan token (satu token per baris)")
            return []
    
    def check_in(self, token, account_num):
        """Melakukan check-in untuk satu akun"""
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        payload = {
            "taskGuid": self.task_guid,
            "extraArguments": [
                json.dumps({
                    "currentStreak": 0,
                    "isStreakInDanger": False,
                    "hasCheckedInToday": False
                })
            ]
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 201:
                data = response.json()
                print(f"âœ“ Akun #{account_num}: Check-in berhasil!")
                return True
            else:
                print(f"âœ— Akun #{account_num}: Gagal ({response.status_code})")
                print(f"  Response: {response.text[:100]}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"âœ— Akun #{account_num}: Error koneksi - {str(e)}")
            return False
    
    def run(self, max_days=8):
        """Menjalankan bot untuk semua akun"""
        if not self.accounts:
            print("\nâœ— Tidak ada akun yang dimuat. Bot berhenti.")
            return
        
        print(f"\n{'='*50}")
        print(f"AUTO CHECK-IN BOT - Target: {max_days} Hari")
        print(f"{'='*50}")
        print(f"Total Akun: {len(self.accounts)}")
        print(f"Mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        for day in range(1, max_days + 1):
            print(f"\nðŸ“… HARI KE-{day} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)
            
            success_count = 0
            for idx, token in enumerate(self.accounts, 1):
                if self.check_in(token, idx):
                    success_count += 1
                time.sleep(2)  
            
            print(f"\nðŸ“Š Ringkasan Hari {day}: {success_count}/{len(self.accounts)} berhasil")
            
            if day < max_days:
                wait_time = 24 * 60 * 60  
                next_time = datetime.now().timestamp() + wait_time
                next_datetime = datetime.fromtimestamp(next_time)
                
                print(f"\nâ° Menunggu 24 jam...")
                print(f"   Check-in berikutnya: {next_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*50}")
                
                time.sleep(wait_time)
        
        print(f"\n{'='*50}")
        print(f"âœ“ SELESAI! Bot telah berjalan selama {max_days} hari")
        print(f"  Selesai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")


if __name__ == "__main__":
    bot = CheckInBot()
    bot.run(max_days=8)
