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

# --- [ДАННЫЕ РОЛЕЙ (Заполняются автоматически)] ---
ROLE_IDS = {}    # Словарь {'Имя Роли': ID_Роли} как в Config 1
VALID_ROLES = [] # Список имен ролей для команд

# Границы для фильтрации (какие роли бот добавит в VALID_ROLES)
MIN_RANK_THRESHOLD = 1
MAX_RANK_THRESHOLD = 200

def load_roblox_ranks():
    """
    Синхронно загружает роли и формирует структуру под старый формат utils.py
    """
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/roles"
    
    print("\n" + "="*50)
    print(f"📡 СИНХРОНИЗАЦИЯ ROBLOX -> CONFIG (ID: {GROUP_ID})")
    print("="*50)
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            roles = data.get("roles", [])
            
            # Очищаем старые данные перед обновлением
            ROLE_IDS.clear()
            VALID_ROLES.clear()
            
            # Сортируем по рангу для красивого вывода в консоль
            sorted_roles = sorted(roles, key=lambda x: x['rank'], reverse=True)
            
            print(f"{'STATUS':<8} | {'RANK':<4} | {'ROLE NAME':<25}")
            print("-" * 50)

            for role in sorted_roles:
                r_name = role["name"]
                r_id = role["id"]
                r_val = role["rank"]
                
                # Заполняем основной словарь (имя: id)
                ROLE_IDS[r_name] = r_id
                
                # Проверяем, входит ли роль в разрешенный диапазон
                if MIN_RANK_THRESHOLD <= r_val <= MAX_RANK_THRESHOLD:
                    VALID_ROLES.append(r_name)
                    status = "[ OK ]"
                else:
                    status = "[SKIP]"
                
                print(f"{status:<8} | {r_val:<4} | {r_name[:25]}")
            
            # Реверсируем список валидных ролей, чтобы они шли от младшей к старшей (для promote)
            VALID_ROLES.reverse() 
            
            print("-" * 50)
            print(f"✅ ROLE_IDS готов: {len(ROLE_IDS)} записей.")
            print(f"⚙️ VALID_ROLES готов: {len(VALID_ROLES)} ролей.")
            print("="*50 + "\n")
            return True
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return False
    except Exception as e:
        print(f"🔥 Критическая ошибка: {e}")
        return False

# Запуск при импорте
load_roblox_ranks()
            
