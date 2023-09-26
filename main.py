import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import keyboard
import win32gui 
# import win32api
import random
import json
# from core4 import cli
import pytesseract
from PIL import ImageGrab
import threading
from chatgpt import chat
# from tongyi import chat 
from tkinter import scrolledtext
import os
import queue
import time

def position_window_left_of_program(program_title, window):
    # 启动 LDPlayer 模拟器，并打开指定应用程序
    ldplayer_cmd = r'D:\LDPlayer\ldconsole.exe launchex --index 0 --packagename com.maimemo.android.momo'
    os.system(ldplayer_cmd)

    max_wait_time = 10  # 最大等待时间，单位为秒
    wait_interval = 1   # 每次等待间隔时间，单位为秒
    waited_time = 0     # 已经等待的时间

    while waited_time < max_wait_time:
        time.sleep(wait_interval)
        program_windows = gw.getWindowsWithTitle(program_title)
        if len(program_windows) > 0:
            break
        else:
            print('Waiting for program window...')
            waited_time += wait_interval
    if len(program_windows) > 0:
        program_window = program_windows[0]
        program_x, program_y = program_window.left, program_window.top

        x = program_x - window.winfo_reqwidth() - 70
        y = program_y

        window.geometry(f"+{x}+{y}")
    else:
        print('Failed to find the program window.')


def save_dict_to_json():
    with open(words_dict_file_path, "w") as json_file:
        json.dump(words_dict, json_file, indent=4)


def read_dict_from_json():
    with open(words_dict_file_path, "r") as json_file:
        words_dict = json.load(json_file)
    return words_dict


def choose_words():
    choices = set()
    remain_word_list = list(words_dict.keys())
    # remain_word_list =  list(words_dict.keys())
    weights = [words_dict[word] for word in remain_word_list]  # 使用字典中单词的值作为权重

    cumulative_prob = [sum(weights[: i + 1]) for i in range(len(weights))]

    while len(choices) < 5:
        r = random.uniform(0, cumulative_prob[-1])

        for i, prob in enumerate(cumulative_prob):
            if r <= prob:
                choices.add(remain_word_list[i])
                break
    # print(choices)
    return choices
def show_next_message():
    # print(message_queue.qsize())
    large_text = message_queue.get()
    show_custom_message_box(large_text, window)
    if not message_queue.empty():
        show_next_message()
def ramdom_rewards():
    global words_dict_renew
    if words_dict_renew > 5 :
        words_dict_renew = 0
        show_content(f"{player.name}找到了一张纸条！")
        new_thread = threading.Thread(target=get_sentence)
        # 启动新线程
        new_thread.start()
    elif not message_queue.empty():
        new_thread = threading.Thread(target=show_next_message)
        # 启动新线程
        new_thread.start()


def show_custom_message_box(large_text, parent):
    def on_hotkey():
        nonlocal close_window
        if close_window==False:
            show_content("阅读纸条，")
            player.restore_health(10)
            label5.config(text=content)
            # 销植 messagebox
            messagebox.destroy()           
            close_window = True
    #关闭窗口
    close_window = False

    # 创建自定义弹窗窗口
    messagebox = tk.Toplevel(parent)
    messagebox.title("小纸条")
    messagebox.attributes("-topmost", True)

    # 设置弹窗的位置
    messagebox.geometry("+0+0")  # 将弹窗显示在 (100, 100) 的位置

    # 创建 ScrolledText 控件
    text_box = scrolledtext.ScrolledText(messagebox, wrap=tk.WORD)
    text_box.pack(fill=tk.BOTH, expand=True)

    # 在文本框中插入文本
    text_box.insert(tk.END, large_text)

    # 设置消息文本的字体和大小
    font = ("黑体", 15)
    text_box.configure(font=font)

    # 禁用窗口的关闭按钮
    messagebox.protocol("WM_DELETE_WINDOW", on_hotkey)
    # keyboard.add_hotkey('x', on_hotkey) # 监听键盘事件
    keyboard.wait("9") # 等待键盘事件
    on_hotkey()
    

def get_sentence():
    global words_dict
    selected_words = choose_words()
    # 根据单词的值进行排序
    words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse=False))
    data = f"""
    {player.name}是英美主流报刊杂志的编辑和作者，{player.name}要写一篇稿件，现在用英语使用以下列表中的单词写一段话。
    要求:
    1.这段话50个单词以内
    2.将这段话翻译成中文
    3.列出单词的意思
    4.先显示单词意思，再显示英文，最后显示中文
    5.在段落中也标出单词
    6.例子:
    ###
    1. methodologically: 以方法论的方式（adv.）
    2. tease: 戏弄，逗乐（v.）
    3. genealogist: 家谱学家（n.）
    4. layoff: 解雇，裁员（n.）
    5. undermine: 破坏，削弱（v.）
    Methodologically, the genealogist would tease out the intricate family connections, tracing lineages back several generations. However, a sudden layoff in the archival department may undermine these efforts, leaving the research unfinished.
    家谱学家会以方法论的方式，揭示错综复杂的家族关系，追溯几代人的血统。然而，档案部门的突然裁员可能会破坏这些努力，使研究无法完成。
    ###
    单词：{','.join(selected_words)}
    """
    # data = f"""
    # 请{player.name}当我万能的老师。用英语使用下列单词中，写一句话。
    # 要求:
    # 1.列出选出的单词的英文释义
    # 2.将这句翻译成中文
    # 3.先显示单词释义，再显示英文句子，最后显示中文句子
    # 4.例子
    # ###
    # 1. chronic(adj.): 慢性的，长期的
    # 2. abiotrophy(n.): 机体退化
    # 3. conspire(v.): 密谋，共谋
    # The chronic illness conspired with genetic abiotrophy to weaken his immune system.
    # 长期的疾病与基因性机体退化相互作用，削弱了他的免疫系统。
    # ###
    # 单词：{','.join(selected_words)}
    # """
    # print(data)
    sentence = chat(data)
    # 定义按钮点击事件处理函数
    # show_custom_message_box(sentence,window)
    message_queue.put(sentence)
def get_word():
    window_title = TITLE  # 要截取的窗口标题
    hwnd = win32gui.FindWindow(None, window_title)  # 根据窗口标题查找窗口句柄

    rect = win32gui.GetWindowRect(hwnd)  # 获取窗口的坐标
    x, y, w, h = rect
    actual_x = int(x*1.5)
    actual_y = int(y*1.5)
    actual_w = int(w*1.5)
    actual_h = int(h*1.5)
    screenshot = ImageGrab.grab(bbox=(actual_x+50, actual_y+70, actual_x +500, actual_y + 140))  # 进行截图
    # 使用Tesseract进行OCR识别
    result = pytesseract.image_to_string(screenshot)
    result = result.replace('\n','').strip()
    # 打印识别结果
    return result
def get_recognized_word():
    global recognized_word
    recognized_word = get_word()
    # print(recognized_word)


def get_words_dict():
    global words_dict, words_dict_renew
    if recognized_word:
        if recognized_word not in words_dict:
            words_dict[recognized_word] = 1
        else:
            words_dict[recognized_word] += 1
    words_dict_renew += 1
    save_dict_to_json()


def check_window(input_key):
    title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    if title == TITLE:
        return True
    else:   
        global wake_key_num
        if input_key == wake_key:
            wake_key_num -= 1
        else:
            #                 # 获取小键盘状态
            # state = win32api.GetKeyState(0x90)

            # # 检查小键盘状态是否启用
            # if state == 1:              # 锁定小键盘
            #     keyboard.press('numlock')
            #     keyboard.release('numlock')
            wake_key_num = 5
        text = f'再按{wake_key_num}次{wake_key}键开始游戏！'
        label5.config(text=text)    
        if wake_key_num <= 0:
            hwnd = win32gui.FindWindow(None, TITLE)
            if hwnd != 0:
                # 设置窗口为前台窗口
                win32gui.SetForegroundWindow(hwnd)
                win32gui.SetActiveWindow(hwnd)
                print(hwnd)
                wake_key_num = 0 
        return False


def show_content(messege):
    global content
    content += '•' + messege+'\n'

def get_word_mean(word):
    data = f"{word} 这个单词是什么意思，举点英语例子，让我记住这个单词"
    
    word_mean = chat(data)
    message_queue.put(word_mean)

class Character:
    def __init__(self, name):
        self.name = name
        self.combo_attack = 0

    def attack_opponent(self, opponent):
        self.generate_random_description()

        attack_damage = self.handle_attack(opponent)
        opponent_take_damage = opponent.take_damage(attack_damage)
        self.combo_attack += 1       
        return opponent_take_damage


    def take_damage(self, damage_received):
        defense_effect = random.randint(1, 3) * self.defense
        take_damage = int((damage_received**2)/(damage_received+defense_effect))
        self.health -= take_damage
        self.health = max(0, self.health)
        self.combo_attack = 0
        label3.config(text=f"{self.name}'s HP -{take_damage} !")
        self.generate_random_description()
        return take_damage


class Player(Character):
    def __init__(self):
        # 提取字典中的单词和对应的概率值
        words = list(words_dict.keys())
        probabilities = list(words_dict.values())
        # 使用权重（概率）进行随机选择
        random_word = random.choices(words, weights=probabilities)[0]
        name = random_word.capitalize()
        super().__init__(name)
        self.level = 1
        self.health_max = 100
        self.health = self.health_max
        self.attack_max = 15
        self.attack = self.attack_max
        self.defense_max = 2
        self.defense = self.defense_max
        self.exp = 0
        self.exp_max = 3
        self.status = {}
        self.upgrade_options = {}
        self.magic_resistance = 1
        self.up_state = False
        # self.backpack = {'HP药水':0}
        self.death_methed = random.choice(hero_data["死亡"]).replace('你', self.name)
        self.attack_methed = 1
        self.defense_methed = 2
        self.attacked_methed = 3
        new_thread = threading.Thread(target=get_word_mean, args=(random_word,))  # 创建线程
        # 启动新线程
        new_thread.start()
    def level_up(self):
        if self.exp >= self.exp_max:
            self.exp = 0
            self.level += 1
            self.health_max += 5
            self.attack += 5
            self.attack_max += 5
            self.defense += 3
            self.defense_max += 3
            self.exp_max += 2 
            self.magic_resistance += 2          
            show_content(f"{player.name}升到了{self.level}级!")
            self.restore_health(50)
            if self.level % 5 == 0:
                self.create_upgrade_options()
                return True


    def create_upgrade_options(self):
        available_options = {
            "最大生命值": 5,
            "攻击力": 3,
            "防御力": 3,
            "恢复生命值": 10,
            '魔抗':3
        }

        selected_options = random.sample(list(available_options.keys()), k=3)

        for i, option in enumerate(selected_options):
            coefficient = available_options[option]
            value = coefficient * self.level*0.5
            value = int(value)

            key = str(i + 4)
            self.upgrade_options[key] = {"attribute": option, "value": value}

        
    def update_player_level(self, user_choice):
        if user_choice in self.upgrade_options:
            option = self.upgrade_options[user_choice]
            attribute = option["attribute"]
            value = option["value"]
            # 根据用户选择更新属性值
            if attribute == "最大生命值":
                self.health_max += value
            elif attribute == "攻击力":
                self.attack_max += value
                self.attack += value
            elif attribute == "防御力":
                self.defense_max += value
                self.defense += value
            elif attribute == "恢复生命值":
                self.restore_health(value)
            elif attribute == "魔抗":
                self.magic_resistance += value           

            show_content(f"{player.name}的{attribute}提升了{value}点！")



    def generate_random_description(self):
        self.attack_methed = random.choice(hero_data["攻击动作"]).replace('你', self.name)
        self.defense_methed = random.choice(hero_data["防御动作"]).replace('你', self.name)
        self.attacked_methed = random.choice(hero_data["被攻击"]).replace('你', self.name)
    
    def restore_health(self,health_num):
        # 将当前的HP加上传入的health_num
        self.health += health_num
        
        # 如果当前HP大于最大HP，则将最大HP设置为当前HP
        if self.health > self.health_max:
            self.health = self.health_max
            message = f"HP恢复满了！"
        # 否则，将当前HP设置为最大HP
        else:
            message = f"HP生命值恢复了{health_num}点"
        # 显示消息
        show_content(message)
        # 显示玩家状态
        display_player_status(self)

    def handle_attack(self,opponent):
        return int((self.attack + self.combo_attack) * random.uniform(0.9, 1.1))
class Enemy(Character):
    def __init__(self, level):
        name = self.get_monster_name()
        super().__init__(name)
        self.level = level
        self.all_point = self.level * 6
        self.num1, self.num2, self.num3,self.num4= self.split_point(self.all_point)
        self.health_max = self.num1 + self.level * 8
        self.health = self.health_max
        self.attack = self.num2 + self.level * 2 + 10
        self.defense = self.num3 + self.level + 1       
        self.magical_power = self.num4 + self.level 
        self.attack_attribute = ""
        self.attack_skills = monster_data[self.name]["攻击方式"]
        self.defense_skills = monster_data[self.name]["防御方式"]

    def split_point(self, number):
        # Generate three random integers
        rand4 = random.randint(0, self.level)
        rand3 = random.randint(0, number - rand4)
        rand2 = random.randint(0, number - rand4 - rand3)

        # Calculate the fourth integer
        rand1 = number - rand4 - rand3 - rand2

        # Output the result
        return rand1, rand2, rand3, rand4


    def get_monster_name(self):
        monster_names = list(monster_data.keys())
        return random.choice(monster_names)

    def generate_random_description(self):
        self.attack_skill = random.choice(self.attack_skills)
        self.defense_skill = random.choice(self.defense_skills)
        
    def handle_attack(self, opponent):
        show_content(f"{self.name}使用了{self.attack_skill}!")
        # effect_number = random.randint(1, 3)
        message = ''
        damage = self.attack

        # 判断攻击技能类型，并根据不同类型效果对对手进行处理
        
        if any(item in self.attack_skill for item in ["火", "焰", "炎", "燃", "烧", "熔"]):
            if "fire" in opponent.status:
                opponent.status["fire"] += int(self.magical_power)
                message += "{player.name}身上的火变大了！"
            else:
                opponent.status["fire"] = int(self.magical_power )
                message += "{player.name}身上着火了！"
            message += f'火焰层数为{opponent.status["fire"]}。'
        elif any(item in self.attack_skill for item in ["冰", "冻", "霜",'寒']):
            ice_original_damage = int(self.magical_power )
            ice_real_damage = int((ice_original_damage**2) / (player.magic_resistance + ice_original_damage))
            if "freezing" in opponent.status:
                opponent.status["freezing"] += ice_real_damage
                message += "身上的冰块变厚了！"
            else:
                opponent.status["freezing"] = ice_real_damage
                message += "{player.name}被冰冻了！"
            message += f'冰块层数为{opponent.status["freezing"]}。'
        elif any(item in self.attack_skill for item in ['毒','酸']):
            poison_original_damage = int(self.magical_power)
            poison_real_damage = int((poison_original_damage**2) / (player.magic_resistance + poison_original_damage))
            if "poison" in opponent.status:
                opponent.status["poison"] += poison_original_damage
                message += "中毒加深了！"
            else:
                opponent.status["poison"] = poison_original_damage
                message += "{player.name}中毒了！"
            message += f'中毒层数为{opponent.status["poison"]}。'
            # 攻击附带的毒素对对手的攻击和防御进行降低
            attack_change = min(poison_real_damage, opponent.attack)
            defense_change = min(poison_real_damage, opponent.defense)
            opponent.attack = max(opponent.attack - poison_real_damage, 0)
            opponent.defense = max(opponent.defense - poison_real_damage, 0)

            message += f"\nAttack -{attack_change}, Defense -{defense_change}!"
        else:
            damage += self.magical_power
        
        # 如果有消息需要显示，就显示消息内容
        if message:
            show_content(message)
        
        return damage


def display_player_status(player):
    status_functions = {
    "fire": "🔥",
    "freezing": "🧊",
    "poison": "🍄"
    }
    statuses = player.status.keys()
    output = [status_functions[status] for status in statuses if status in status_functions]  
    name = player.name + "".join(output)
    label_00.config(text=f"{name}\nHP:{player.health}/{player.health_max}")
    label_10["maximum"] = player.health_max
    label_10["value"] = player.health  
    label_20.config(
        text=f"Level:{player.level}\nAttack:{player.attack}\nDefense:{player.defense}\nMR:{player.magic_resistance}\nCombo:{player.combo_attack}"
    )
    label_40.config(text=f"EXP: {player.exp}/{player.exp_max}")
def display_enemy_status(enemy):
    label_01.config(text=f"{enemy.name}\nHP:{enemy.health}/{enemy.health_max}")
    label_11["maximum"] = enemy.health_max
    label_11["value"] = enemy.health
    label_21.config(
        text=f"Level:{enemy.level}\nAttack:{enemy.attack}\nDefense:{enemy.defense}\nAP:{enemy.magical_power}\nCombo:{enemy.combo_attack}"
    )
    label_41["maximum"] = player.exp_max
    label_41["value"] = player.exp
    
def display_status(player, enemy):
    display_enemy_status(enemy)
    display_player_status(player)




def get_hore_monster_data_json(current_dir):
    hero_data_file_path = os.path.join(current_dir, "hero_data.json")
    monster_data_file_path = os.path.join(current_dir, "monster_data.json")
    
    with open(hero_data_file_path, "r", encoding="utf8") as f:
        hero_data = json.load(f)
    with open(monster_data_file_path, "r", encoding="utf8") as f:
        monster_data = json.load(f)
        
    return hero_data, monster_data


def descriptions_of_multiple_monsters():
    monsters = [ennmy.name for ennmy in enemys_list]
    monster_counts = {}

    # 统计怪物数量
    for monster in monsters:
        if monster in monster_counts:
            monster_counts[monster] += 1
        else:
            monster_counts[monster] = 1

    # 输出怪物信息
    output_text = f"现在有{len(monsters)}只怪物正在攻击{player.name}！"

    count = len(monster_counts)
    # 计算总数量
    if count == 1:
        monster_name = list(monster_counts.keys())[0]
        output_text += f"面对着{monster_name},{player.name}全力以赴地发起攻击！"
    elif count == 2:
        monster_1_name = list(monster_counts.keys())[0]
        monster_2_name = list(monster_counts.keys())[1]
        output_text += f"面对着{monster_counts[monster_1_name]}只{monster_1_name}和{monster_counts[monster_2_name]}只{monster_2_name}的联合攻击！拿起武器,奋勇战斗！"
    elif count == 3:
        monster_1_name = list(monster_counts.keys())[0]
        monster_2_name = list(monster_counts.keys())[1]
        monster_3_name = list(monster_counts.keys())[2]
        output_text += f"{monster_counts[monster_1_name]}只{monster_1_name}、{monster_counts[monster_2_name]}只{monster_2_name}和{monster_counts[monster_3_name]}只{monster_3_name}一起向{player.name}发起猛烈进攻！不要退缩,勇往直前,将它们击败！"
    elif count == 4:
        monster_1_name = list(monster_counts.keys())[0]
        monster_2_name = list(monster_counts.keys())[1]
        monster_3_name = list(monster_counts.keys())[2]
        monster_4_name = list(monster_counts.keys())[3]
        output_text += f"{monster_counts[monster_1_name]}只{monster_1_name}、{monster_counts[monster_2_name]}只{monster_2_name}、{monster_counts[monster_3_name]}只{monster_3_name}和{monster_counts[monster_4_name]}只{monster_4_name}齐心协力地向{player.name}展开攻击！发动{player.name}的绝技,战胜它们吧！"
    elif count == 5:
        monster_1_name = list(monster_counts.keys())[0]
        monster_2_name = list(monster_counts.keys())[1]
        monster_3_name = list(monster_counts.keys())[2]
        monster_4_name = list(monster_counts.keys())[3]
        monster_5_name = list(monster_counts.keys())[4]
        output_text += f"{monster_counts[monster_1_name]}只{monster_1_name}、{monster_counts[monster_2_name]}只{monster_2_name}、{monster_counts[monster_3_name]}只{monster_3_name}、{monster_counts[monster_4_name]}只{monster_4_name}和{monster_counts[monster_5_name]}只{monster_5_name}一同向{player.name}展开猛烈攻势！这是一个真正的生死决战,挺身而战,保卫自己！"
    else:
        monster_info = ", ".join([f"{v}只{i}" for i, v in monster_counts.items()])
        output_text += f"这么多怪物,{monster_info},它们把{player.name}包围了!快想办法找到突破口！"

    return output_text


def create_enemy():
    global enemys_list
    enemy = Enemy(player.level)
    enemys_list.append(enemy)
    show_content(f"一只{enemy.name}正在靠近{player.name}！")


def fire(player, status_messages):
    fire_original_damage = int(player.status["fire"]/2)
    fire_real_damage = int((fire_original_damage**2)/(fire_original_damage+player.magic_resistance))
    player.health -= fire_real_damage
    status_messages.append(f'身上的火在燃烧，火焰层数为{fire_original_damage}。生命值减{fire_real_damage}')
    player.status["fire"] = fire_original_damage
    if player.status["fire"] == 0 or fire_real_damage ==0 :
        player.status.pop("fire")
        status_messages.append('火熄灭了！')
    if player.health <= 0 :
        status_messages.append('{player.name}被烧死了！')

def freezing(player, status_messages):
    freezing_count = player.status["freezing"]
    status_messages.append(f'{player.name}正在被冰冻！当前冰块层数为{freezing_count}！')

def poison(player, status_messages):
    if "poison" in player.status:
        attack_before = player.attack
        defense_before = player.defense

        poison_original_damage = player.status["poison"]-1
        magic_resistance = int((player.magic_resistance**2) /(player.magic_resistance+poison_original_damage))
        
        player.attack = min(player.attack + magic_resistance, player.attack_max)
        player.defense = min(player.defense + magic_resistance, player.defense_max)

        attack_change = player.attack - attack_before
        defense_change = player.defense - defense_before
        status_messages.append(f'{player.name}中毒了，中毒层数为{poison_original_damage}，状态正在恢复。\nAttack +{attack_change}，Defense +{defense_change}')
        player.status["poison"] = poison_original_damage
        if player.attack >= player.attack_max and player.defense >= player.defense_max:
            player.status.pop("poison")
            status_messages.append('体内的毒清除了！')
            

def update_player_status_effects(player):

    if player.status:
        status_functions = {
            "fire": fire,
            "freezing": freezing,
            "poison": poison
        }

        status_messages = []
        for status in player.status.copy():
            status_function = status_functions.get(status)
            status_function(player, status_messages)

        show_content("\n".join(status_messages))



def check_player_health_status(player):
    global playing
    if player.health <= 0:
        # show_content(f"habitica受伤！")
        playing = False
        display_player_status(player)
        # command = "habits down id 45665f20-6a1e-4f48-8276-b7cf51d986ff"
        # new_thread = threading.Thread(target=cli,args=(command,))
        # # 启动新线程
        # new_thread.start()

def remove_dead_enemy(selected_enemy_indices):
    selected_enemy_indices.sort(reverse=True)  # 需要按照逆序排序，以防止索引移位导致删除错误的元素
    for index in selected_enemy_indices.copy():
        enemy = enemys_list[index]
        if enemy.health <= 0:
            enemys_list.remove(enemy) 
            if len(enemys_list) == 0:
                create_enemy() 


def check_enemy_health_status(enemy):
    exp = 0
    if enemy.health <= 0:
        show_content(f"{enemy.name}倒下了!")
        exp = enemy.level
    return exp

def select_enemies(enemy_list, num_selected):
    if len(enemy_list) <= num_selected:
        selected_indices = list(range(len(enemy_list)))
    else:
        selected_indices = random.sample(range(len(enemy_list)), k=num_selected)
    return selected_indices

def inputkey_enter_space(selected_enemy_indices,enemy_index,display_enemy):
    remove_dead_enemy(selected_enemy_indices)
    selected_enemy_indices = select_enemies(enemys_list, 4)
    enemy_index =  selected_enemy_indices[0]
    display_enemy = enemys_list[enemy_index]
    # 创建一个新的线程
    new_thread = threading.Thread(target=get_recognized_word)
    # 启动新线程
    new_thread.start() 
    return selected_enemy_indices,enemy_index,display_enemy

def inputkey_1(display_enemy):
    show_content(f"{player.attack_methed}!")

    if "freezing" in player.status:
        player.status["freezing"] -= player.attack
        freezing_count = player.status["freezing"]
        if freezing_count > 0:
            show_content(f"{player.name}打碎了{player.attack}层冰！当前冰块层数为{freezing_count}！")
        else:
            player.status.pop("freezing")  # 冰块被全部打碎后删除冰冻状态
            show_content("冰块被打碎了！继续战斗！")
    else:
        get_exp = 0
        for attacked_enemy_index in selected_enemy_indices[:2]:
            attacked_enemy = enemys_list[attacked_enemy_index]
            attack_damage= player.attack_opponent(attacked_enemy)
            show_content(
                f"{attacked_enemy.name}使用{attacked_enemy.defense_skill}进行防御!受到了{attack_damage}点伤害。"
            )
            get_exp += check_enemy_health_status(attacked_enemy)
        if get_exp>0:
            show_content(
                f"{player.name}获得了{get_exp}点经验。"
            )
            player.exp += get_exp
            if player.level_up(): # 判断是否升到5级
                player.up_state= True
        display_enemy_status(display_enemy)

        # print('***')
        # print(selected_enemy_indices)
        # print(enemy_index)
        # print(enemys_list)       
def inputkey_3():
    get_words_dict()
    enemy_attack_damage_sum = 0
    for attack_enemy_index in selected_enemy_indices:
        attack_enemy = enemys_list[attack_enemy_index]                       
        enemy_attack_damage = attack_enemy.attack_opponent(player)
        enemy_attack_damage_sum += enemy_attack_damage
    if enemy_attack_damage_sum == 0:
        show_content(f"{player.defense_methed}")
    else:
        attacked_methed_content = player.attacked_methed.replace("但", f"受到了{enemy_attack_damage_sum}点伤害,但")
        show_content(attacked_methed_content)
        if player.health <= 0:  
            show_content(f"{player.death_methed}")    
    
    
# 游戏主循环
def check_keyboard(event):
    global player, content, enemys_list, playing,selected_enemy_indices,enemy_index,confirmed
    input_key = event.name
    # print(input_key)
    if check_window(input_key) and input_key in all_using_key :

        content = ""
        if playing:
            if not selected_enemy_indices:
                selected_enemy_indices = select_enemies(enemys_list, 4)
                enemy_index =  random.choice(selected_enemy_indices)

            display_enemy = enemys_list[enemy_index]
            if input_key in main_options:              
                if confirmed:
                    confirmed = False
                    if input_key == "1":
                        inputkey_1(display_enemy)
                    elif input_key == "2":
                        label3.config(text="Defense!")
                        show_content(f"{player.defense_methed}")
                    elif input_key == "3":
                        inputkey_3()
                    check_player_health_status(player)    
                else:
                    if input_key == "enter" or input_key == "space":
                        selected_enemy_indices,enemy_index,display_enemy = inputkey_enter_space(selected_enemy_indices,enemy_index,display_enemy)
                        confirmed = True
                        update_player_status_effects(player)
                        display_status(player, display_enemy)
                    show_content(descriptions_of_multiple_monsters())       
                ramdom_rewards()
                if random.random() <0.1:
                    create_enemy()
            else:
                if player.up_state and input_key in up_state_options:  
                    # print(input_key)            
                    player.update_player_level(input_key)
                    player.up_state = False
                if player.status.get('freezing'):
                    freezing_count = player.status["freezing"]
                    show_content(f'{player.name}正在被冰冻！当前冰块层数为{freezing_count}！')
                if player.status.get('poison'):
                    show_content(f'{player.name}中毒了！当前中毒层数为{player.status["poison"]}！')
                if player.status.get('fire'):
                    show_content(f'身上的火在燃烧！火焰层数为{player.status["fire"]}')
                show_content(descriptions_of_multiple_monsters())
            display_status(player, display_enemy)

        elif playing == False and input_key == wake_key:
            playing = True 
            show_content("开始游戏！")
            player = Player()
            enemys_list.clear()
            create_enemy()
            selected_enemy_indices = select_enemies(enemys_list, 4)
            enemy_index = random.choice(selected_enemy_indices)      
            display_status(player, enemys_list[enemy_index])


        elif playing == False:
            show_content(f"按{wake_key}键开始！")

        if player.up_state:
            up_reward_content= "请选择升级数值：\n"
            for key, option in player.upgrade_options.items():
                attribute = option["attribute"]
                value = option["value"]
                up_reward_content += f"{key}. {attribute} +{value}\n"
            show_content(up_reward_content)
        label5.config(text=content)
        


content = ""
current_dir = os.path.dirname(os.path.abspath(__file__))
words_dict_file_path = os.path.join(current_dir, "words_dict.json")
if not os.path.exists(words_dict_file_path):
    with open(words_dict_file_path, 'w') as f:
        temp_dict = {"good":1,}
        json.dump(temp_dict, f, indent=4)

hero_data, monster_data = get_hore_monster_data_json(current_dir)
words_dict = read_dict_from_json()
# player = Player() # 创建玩家对象
words_dict_renew = 0
recognized_word = ""
enemys_list = []
selected_enemy_indices = []
enemy_index = 0
message_queue = queue.Queue()
playing = False
confirmed = False
wake_key_num = 5
wake_key = '0'
main_options = ["1", "2", "3","space", "enter"]
up_state_options = ["4", "5", "6"]
all_using_key = main_options + up_state_options+ [wake_key] # 所有按键
TITLE = "雷电模拟器"

# 创建窗口
window = tk.Tk()
window.title("Endless Challenge")

# 上左部分
label_00 = tk.Label(window, text="角色A", font=("黑体", 15))
label_00.grid(row=0, column=0)

# 上右部分
label_01 = tk.Label(window, text="角色B", font=("黑体", 15))
label_01.grid(row=0, column=1)

# 上左部分
label_10 = ttk.Progressbar(window)
label_10.grid(row=1, column=0)

# 上右部分
label_11 = ttk.Progressbar(window)
label_11.grid(row=1, column=1)

# 上左部分
label_20 = tk.Label(window, text="data", font=("黑体", 15))
label_20.grid(row=2, column=0)

# 上右部分
label_21 = tk.Label(window, text="data", font=("黑体", 15))
label_21.grid(row=2, column=1)

# 中间部分
label3 = tk.Label(window, text=f" 按{wake_key}键开始！ ", font=("黑体", 15))
label3.grid(row=3, column=0, columnspan=2)

# # 中间部分
# label4 = tk.Label(window, text=f" Level ",font=("黑体", 15))
# label4.grid(row=4, column=0, columnspan=2)
# 上左部分
label_40 = tk.Label(window, text="EXP", font=("黑体", 15))
label_40.grid(row=4, column=0)

# 上右部分
label_41 = ttk.Progressbar(window)
label_41.grid(row=4, column=1)


# 下部分
label5 = tk.Label(window, text="Event", wraplength=250, justify="left", font=("黑体", 15))
label5.grid(row=5, column=0, columnspan=2)

position_window_left_of_program(TITLE, window)
keyboard.on_press(check_keyboard)

# # 运行游戏

# 启动窗口主循环
window.mainloop()

