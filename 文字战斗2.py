import random

# 怪物列表、形容词列表、武器列表和动词列表
monster_names = [
    "巨魔",
    "恶魔",
    "狼人",
    "僵尸",
    "魔法师",
    "矮人",
    # 更多怪物名称...
]

adjectives = [
    "恐怖的",
    "残暴的",
    "邪恶的",
    "强大的",
    "凶猛的",
    "阴险的",
    # 更多形容词...
]

weapon_names = [
    "剑",
    "战斧",
    "长弓",
    "法杖",
    "投掷斧",
    "法术书",
    # 更多武器名称...
]

verbs = [
    "挥舞",
    "猛击",
    "射出",
    "释放",
    "投掷",
    "施放",
    # 更多动词...
]

# 数值变量
player_health = 100
player_max_health = 100
monster_health = 80

player_attack_min = 20
player_attack_max = 30

monster_attack_min = 15
monster_attack_max = 25

# 战斗地点、环境和战斗策略列表
battle_locations = [
    "在阴暗的森林中",
    "在荒凉的山洞中",
    "在狭窄的城市街道上",
    "在广阔的平原上",
    "在陡峭的山脉中",
    # 更多战斗地点...
]

battle_environments = [
    "大树提供了遮蔽",
    "地面湿滑使行动困难",
    "强风吹拂着战场",
    "充斥着诡异气息",
    # 更多战斗环境...
]

battle_strategies = [
    "保持距离并使用远程攻击",
    "选择近战攻击进行更高伤害",
    "利用环境因素获取战术优势",
    "先发制人并采取控制技能",
    # 更多战斗策略...
]

# 特殊技能和法术列表
special_skills = [
    "闪避攻击",
    "治疗伤口",
    "强化自身能力",
    "提供团队增益效果",
    # 更多特殊技能...
]

spells = [
    "火球术",
    "治疗术",
    "冰冻术",
    "闪电链",
    # 更多法术...
]

# 状态效果列表
status_effects = [
    "中毒",
    "虚弱",
    "眩晕",
    "缠绕",
    # 更多状态效果...
]

# 团队成员列表和胜利奖励
team_members = [
    "骑士",
    "法师",
    "弓箭手",
    "牧师",
    # 更多团队成员...
]

rewards = [
    "经验值",
    "金币",
    "装备物品",
    # 更多奖励...
]

# 特殊事件和战斗事件
special_events = [
    "突然出现了一阵浓雾",
    "地面塌陷，形成了陷阱",
    "大群怪物涌向了战场",
    # 更多特殊事件...
]

battle_events = [
    "怪物的攻击被你成功闪避",
    "你使用法术治疗了自己的伤口",
    "你躲进了一棵大树后藏身躲避怪物的攻击",
    # 更多战斗事件...
]

# 战斗描述生成函数
def generate_battle_description():
    global player_health,monster_health
    monster_name = random.choice(monster_names)
    adjective = random.choice(adjectives)
    weapon_name = random.choice(weapon_names)
    verb = random.choice(verbs)

    battle_location = random.choice(battle_locations)
    battle_environment = random.choice(battle_environments)
    battle_strategy = random.choice(battle_strategies)

    battle_description = f"你{battle_location}{battle_environment}遭遇了一只{adjective}{monster_name}。\n"

    # 模拟多回合战斗
    round_num = 1
    while player_health > 0 and monster_health > 0:
        battle_description =''
        battle_description += f"\n第{round_num}回合：\n"

        # 玩家攻击
        player_damage = random.randint(player_attack_min, player_attack_max)
        monster_health -= player_damage
        battle_description += f"你{verb}了你的{weapon_name}，命中了{adjective}{monster_name}，造成了{player_damage}点伤害。\n"

        # 怪物反击
        if monster_health > 0:
            monster_damage = random.randint(monster_attack_min, monster_attack_max)
            player_health -= monster_damage
            battle_description += f"{adjective}{monster_name}反击了你，造成了{monster_damage}点伤害。\n"

        # 特殊技能和法术
        if random.random() < 0.2:  # 添加使用特殊技能的概率
            special_skill = random.choice(special_skills)
            battle_description += f"\n你使用了特殊技能 - {special_skill}！\n"

        if random.random() < 0.1:  # 添加使用法术的概率
            spell = random.choice(spells)
            battle_description += f"\n你施放了法术 - {spell}！\n"

        # 状态效果
        if random.random() < 0.15:  # 添加状态效果的概率
            status_effect = random.choice(status_effects)
            battle_description += f"{adjective}{monster_name}{status_effect}了！\n"

        player_health_percentage = min(int((player_health / player_max_health) * 100), 100)
        monster_health_percentage = max(int((monster_health / 80) * 100), 0)
        battle_description += f"\n你的生命值：{player_health} ({player_health_percentage}%)\n"
        battle_description += f"{adjective}{monster_name}的生命值：{monster_health} ({monster_health_percentage}%)\n"
        input()
        print(battle_description)
        round_num += 1
    # 检查战斗结果
    battle_description = ''
    if player_health <= 0:
        battle_description += "\n你被击败了，游戏结束。"
    elif monster_health <= 0:
        battle_description += f"\n你成功击败了{adjective}{monster_name}！\n"

        # 团队战斗和胜利奖励
        if random.random() < 0.3:  # 添加团队战斗的概率
            team_member = random.choice(team_members)
            reward = random.choice(rewards)
            battle_description += f"\n你的{team_member}也参与了战斗，并获得了{reward}作为奖励！\n"

        # 特殊事件和战斗事件
        if random.random() < 0.2:  # 添加特殊事件的概率
            special_event = random.choice(special_events)
            battle_description += f"\n在战斗胜利后，{special_event}！\n"

        if random.random() < 0.1:  # 添加战斗事件的概率
            battle_event = random.choice(battle_events)
            battle_description += f"\n在战斗中，{battle_event}\n"
        print(battle_description)
    return battle_description

# 生成战斗描述
description = generate_battle_description()
# print(description)
