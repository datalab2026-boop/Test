import os
import requests

# --- [ТОКЕНЫ] ---
DISCORD_TOKEN = os.environ.get("Bottoken")
ROBLOX_API_KEY = os.environ.get("Apitoken")
RESTART_TOKEN = os.environ.get("Restarttoken")

# --- [НАСТРОЙКИ КАНАЛОВ И ДОСТУПА] ---
GROUP_ID = 841435331
ALLOWED_ROLE_ID = 1479884336051388604
LOG_CHANNEL_ID = 1481718190961590392
BUG_LOGS = 1487248340252098770

# --- [ДИНАМИЧЕСКИЕ ДАННЫЕ РОЛЕЙ] ---
RANKS = {}        
VALID_RANKS = []  

MIN_RANK_THRESHOLD = 1
MAX_RANK_THRESHOLD = 200

def load_roblox_ranks():
    """
    Синхронная загрузка ролей. Выводит отчет прямо в консоль (Render Logs).
    """
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles"
    
    print("\n" + "="*50)
    print(f"📡 СИНХРОНИЗАЦИЯ С ROBLOX (Группа: {GROUP_ID})")
    print("="*50)
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            roles = data.get("roles", [])
            
            RANKS.clear()
            VALID_RANKS.clear()
            
            # Сортируем роли по значению ранга (от 255 до 0)
            sorted_roles = sorted(roles, key=lambda x: x['rank'], reverse=True)
            
            print(f"{'STATUS':<8} | {'RANK':<4} | {'ROLE NAME':<25} | {'ROLE ID'}")
            print("-" * 50)

            for role in sorted_roles:
                r_val = role["rank"]
                r_name = role["name"]
                r_id = role["id"]
                
                RANKS[r_val] = {"name": r_name, "id": r_id}
                
                # Помечаем те, которыми бот может управлять
                if MIN_RANK_THRESHOLD <= r_val <= MAX_RANK_THRESHOLD:
                    VALID_RANKS.append(r_val)
                    status = "[ OK ]"
                else:
                    status = "[SKIP]" # Владелец или Гость
                
                # Печать строки в консоль
                print(f"{status:<8} | {r_val:<4} | {r_name[:25]:<25} | {r_id}")
            
            VALID_RANKS.sort()
            print("-" * 50)
            print(f"✅ Успешно загружено ролей: {len(RANKS)}")
            print(f"⚙️ Доступно для команд: {len(VALID_RANKS)}")
            print("="*50 + "\n")
            return True
        else:
            print(f"❌ ОШИБКА API ROBLOX: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"🔥 КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАГРУЗКЕ: {e}")
        return False

# Автоматический запуск при импорте
load_roblox_ranks()
